from project.frameworks_and_drivers.api_backend.infra.api_singleton import KERNEL_API
from flask import Flask

api_app: Flask = KERNEL_API.app
api_app.run(debug = True)