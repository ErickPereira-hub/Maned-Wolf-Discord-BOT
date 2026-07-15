from project.frameworks_and_drivers.databases.mysql_db.dql.messages_dql import MessageDQL
from project.frameworks_and_drivers.databases.mysql_db.dql.member_dql import MemberDQL
from project.frameworks_and_drivers.databases.mysql_db.dql.channel_dql import ChannelDQL
from project.frameworks_and_drivers.api_backend.middlewares.acumulative_freq_middleware import add_acum_freq_middleware
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Any
from project.application.use_cases.predict_poly_reg_use_case import predict_poly_reg_use_case
from project.application.poisson_member_or_msg import PoissonMemberOrMessage

def pull_data_ext(sid: int):

    resp: Dict[str, Any] = {"enough_data": True}

    #Grabbing the member report
    members_qtt: Dict[str, Tuple[int, int, int]] = MemberDQL().get_members_qtt(sid)
    members_qtt_dist: Dict[str, float | Tuple[int, int, int, int]] = add_acum_freq_middleware(members_qtt)
    inter_members_qtt_dist: List[int] = [d[3] for d in members_qtt_dist["data"].values()]
    overall_tot_avg = members_qtt_dist["overall_tot_avg"]
    overall_tot_std_dev = members_qtt_dist["overall_tot_std_dev"]
    overall_var_avg = members_qtt_dist["overall_var_avg"]
    overall_var_std_dev = members_qtt_dist["overall_var_std_dev"]
    new_members_qtt_dist = {
        "data" : inter_members_qtt_dist,
        "overall_tot_avg" : overall_tot_avg,
        "overall_tot_std_dev" : overall_tot_std_dev,
        "overall_var_avg" : overall_var_avg,
        "overall_var_std_dev" : overall_var_std_dev
    }

    if len(members_qtt) < 10: #Less than 10 days of member data
        resp["enough_data"] = False
        return resp, 200
    
    #Most active members on server since a weak ago
    active_members: List[Dict[str, int]] = MemberDQL().get_active_members_on_server_from_db(
        sid = sid,
        from_date = str(datetime.utcnow() - timedelta(days = 7))
        )
    
    #Most active member on server since yesterday
    active_channels: List[Dict[str, int]] = ChannelDQL().get_top_active_ch_from_db(sid)

    #NSFW channels
    nsfw_dist: Dict[str, int] = ChannelDQL().get_ch_nsfw_from_db(sid)

    #Grabbing the Poisson details for messages
    msg_predict_resp: Dict[str, float | int | List[Tuple[int, float]]] | None = None
    msg_vol: List[Dict[str, int]] = MessageDQL().get_msg_volume_per_day(sid)
    if len(msg_vol) >= 7:
        FROM: int = 5
        UNTIL: int = 15
        poisson_msg: PoissonMemberOrMessage = PoissonMemberOrMessage()
        prob: float = poisson_msg.get_poisson_in_range(
            from_qtt = FROM,
            until_qtt = UNTIL,
            incrs = [list(data.values())[0] for data in msg_vol]
        )
        msg_points: List[Tuple[int, float]] = poisson_msg.get_discrete_points(
            incrs = [list(data.values())[0] for data in msg_vol],
            until = UNTIL,
            dist_size = 20
        )
        msg_predict_resp = {
            "probability" : prob,
            "points": msg_points,
            "from" : FROM,
            "until" : UNTIL
        }

    #Grabbing the Poisson details for members
    member_predict_resp: Dict[str, str | List[Tuple[int, float]]] | None = None
    member_vol: Dict[str, Tuple[int, int, int]] = members_qtt
    member_incrs: List[int | float] = [data[0] for data in member_vol.values()]
    if len(member_incrs) >= 7:
        FROM: int = 1
        UNTIL: int = 5
        pm: PoissonMemberOrMessage = PoissonMemberOrMessage()
        member_prob: float = pm.get_poisson_in_range(
            from_qtt = FROM,
            until_qtt = UNTIL,
            incrs = member_incrs
        )
        member_points: List[Tuple[int, float]] = pm.get_discrete_points(
            incrs = member_incrs,
            until = UNTIL,
            dist_size = 20
        )
        member_predict_resp = {
            "probability" : member_prob,
            "points" : member_points,
            "from" : FROM,
            "until" : UNTIL
        }

    #Getting how many members the server will have for the next 3 days
    poly_reg_for_member_resp: Dict[int, int] = dict()
    qtt_arr: List[int] = [d[3] for d in members_qtt_dist['data'].values()]
    qtt_pos: List[int] = [pos + 1 for pos in range(len(qtt_arr))]
    predict_points: List[Tuple[int, int]] = list(zip(qtt_pos, qtt_arr))
    for day in range(1, 4):
        poly_reg_for_member_resp.update({
            day :
            predict_poly_reg_use_case(
                input = max(qtt_pos) + day,
                dataset = predict_points
                ).get("predicted_output")
            }
        )
        if day == 3:
            poly_reg_for_member_resp.update(
                {"ERROR" :
                 predict_poly_reg_use_case(
                    input = -1, #<--- Input value doesn't make a difference when we want to catche the error of the prediction
                    dataset = predict_points
                ).get("error")})

    #Preparing the response
    resp.update({
        "most_active_members" : active_members,
        "most_active_channels" : active_channels,
        "is_nsfw" : nsfw_dist,
        "members_qtt" : new_members_qtt_dist,
        "new_msg_probability" : msg_predict_resp,
        "new_member_probability" : member_predict_resp,
        "member_prediction" : poly_reg_for_member_resp
    })
    return resp