
""" Микро-сервис для email и sms рассылок

"""

from envi import Application as EnviApplication
from controllers import Controller

application = EnviApplication()
application.route("/<action>/", Controller)
application.route("/v1/<action>/", Controller)