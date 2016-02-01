""" Контроллеры сервиса """

import json
import base64
from envi import Controller as BaseController, Request
from models import NotificationService
from exceptions import BaseServiceException

service = NotificationService()


def response_format(func):
    """ Декоратор для форматирования ответа
    :param func:
    """
    def wrapper(*args, **kwargs):
        """ wrapper
        :param args:
        :param kwargs:
        """
        try:
            return json.dumps(func(*args, **kwargs))
        except BaseServiceException as e:
            return json.dumps({"error": {"code": e.code, "message": e.msg}})
    return wrapper


class Controller(BaseController):
    """ Контроллер """

    @classmethod
    @response_format
    def send_email(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        html = base64.b64decode(request.get("base64").replace(" ", "+").encode()).decode()
        return service.send_email(request.get("address"), request.get("subject"), html)

    @classmethod
    @response_format
    def send_sms(cls, request: Request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        return service.send_sms(request.get("address"), request.get("text"))