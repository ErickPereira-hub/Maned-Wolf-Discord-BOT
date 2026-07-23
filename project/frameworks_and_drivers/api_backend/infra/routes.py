from typing import Dict
from flask_restful import Resource
from project.frameworks_and_drivers.api_backend.controllers.server import Server
from project.frameworks_and_drivers.api_backend.controllers.msg import Msg
from project.frameworks_and_drivers.api_backend.controllers.member import Member
from project.frameworks_and_drivers.api_backend.controllers.channel import Channel
from project.frameworks_and_drivers.api_backend.controllers.member_analysis import MemberAnaysis
from project.frameworks_and_drivers.api_backend.controllers.member_predict import MemberPredict
from project.frameworks_and_drivers.api_backend.controllers.member_poisson import MemberPoisson
from project.frameworks_and_drivers.api_backend.controllers.top_active_ch import TopActiveCh
from project.frameworks_and_drivers.api_backend.controllers.channel_analysis import ChannelAnalysis
from project.frameworks_and_drivers.api_backend.controllers.top_members import TopMembers
from project.frameworks_and_drivers.api_backend.controllers.most_active_member import MostActiveMember
from project.frameworks_and_drivers.api_backend.controllers.message_poisson import MessagePoisson
from project.frameworks_and_drivers.api_backend.controllers.pull_big_data import PullBigData
from project.frameworks_and_drivers.api_backend.controllers.endpoints_for_web_site.download import DownloadMessageAuditLogs
from project.frameworks_and_drivers.api_backend.controllers.endpoints_for_web_site.poisson_msg_on_web import PoissonMessageOnWeb
from project.frameworks_and_drivers.api_backend.controllers.endpoints_for_web_site.poisson_member_on_web import PoissonMemberOnWeb

routes: Dict[Resource, str] = {
    Server : "/server",
    Msg : "/msg",
    Member : "/member",
    Channel: "/channel",
    MemberAnaysis : "/member/analysis",
    MemberPredict : "/member/predict",
    MemberPoisson : "/member/poisson",
    TopActiveCh : "/channel/top_active",
    ChannelAnalysis : "/channel/analysis",
    TopMembers : "/member/top_members",
    MostActiveMember: "/member/most_active_member",
    MessagePoisson: "/msg/poisson",
    PullBigData: "/pull",
    DownloadMessageAuditLogs : "/download/audit_msg",
    PoissonMessageOnWeb : "/msg/poisson_for_web",
    PoissonMemberOnWeb: "/member/poisson_for_web"
}