from project.frameworks_and_drivers.api_backend.infra.api_singleton import KERNEL_API
from flask import Flask
import project.frameworks_and_drivers.databases.mysql_db.infra.run_db #Calls a script that creates the MySQL database and its tables if such database doesn't exist.

api_app: Flask = KERNEL_API.app
api_app.run(debug = True)