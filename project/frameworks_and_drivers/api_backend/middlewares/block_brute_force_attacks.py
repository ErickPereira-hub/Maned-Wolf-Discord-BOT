from project.frameworks_and_drivers.databases.redis_db.rate_limit.block_login_abuse import loginBlocker
from flask_restful import abort

def block_brute_force_attacks(server_id: int) -> None:
    loginBlocker.generate_or_takeout_chance(server_id) #<--- Creating the user or taking out one chance
    if not loginBlocker.check_if_user_has_chances(server_id):
        abort(429, message = "Brute force blocked. Try later!")