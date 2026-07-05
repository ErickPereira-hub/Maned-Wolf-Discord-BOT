import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from time import sleep
from project.frameworks_and_drivers.api_backend.infra.api_singleton import KERNEL_API
from flask import Flask

if __name__ == "__main__":
    print("Waiting the database...")
    sleep(15)
    import project.frameworks_and_drivers.databases.mysql_db.infra.run_db #Calls a script that creates the MySQL database and its tables if such database doesn't exist.
    api_app: Flask = KERNEL_API.app
    api_app.run(host = "0.0.0.0", port = 5000, debug = True)