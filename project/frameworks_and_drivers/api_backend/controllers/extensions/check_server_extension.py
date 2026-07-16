from typing import List, Dict, Tuple, Any
from project.frameworks_and_drivers.databases.mysql_db.dql.server_dql import ServerDQL
from flask_restful import abort

def dismish_non_servers(sid: int) -> None:

    signal: bool = ServerDQL.check_existence(sid)
    if not signal:
        abort(404, message = "Discord Server Not Found")