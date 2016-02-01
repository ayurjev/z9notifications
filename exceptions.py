
""" Исключения """


class BaseServiceException(Exception):
    """ Базовый класс исключений """
    code = 0
    msg = "Неизвестная ошибка"


class InvalidPhoneNumber(BaseServiceException):
    """ Некорректный формат номера телефона """
    code = 1
    msg = "Некорректный формат номера телефона"


class EmailError(BaseServiceException):
    """ Ошибка отправки email """
    code = 2
    msg = "Ошибка отправки email"


class SmsError(BaseServiceException):
    """ Ошибка отправки смс-сообщения """
    code = 3
    msg = "Ошибка отправки смс"