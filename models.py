""" Модели """

import os
import re
import pyzmail
import mimetypes
from exceptions import *

from smsc_api import SMSC



class NotificationService(object):
    """ Модель сервиса рассылок """

    @classmethod
    def guess_mimetype(cls, file):
        """ Метод для определения mimetype
        :param file:
        :return:
        """
        guess = mimetypes.guess_type(file)
        if guess[0] is not None:
            return tuple(guess[0].split("/"))
        else:
            return "application", "octet-stream"

    @classmethod
    def send_email(cls, email, subject, html, attachments: list=None, embeddeds: list=None):
        """ Выполняет отправку email
        :param email:
        :param subject:
        :param html:
        :param attachments:
        :param embeddeds:
        :return:
        """
        try:
            mail_attachments = []
            if attachments:
                for attachment in attachments:
                    mimetype, subtype = cls.guess_mimetype(attachment["name"])
                    mail_attachments.append((attachment["bytes"], mimetype, subtype, attachment["name"], None))

            mail_embeddeds = []
            if embeddeds:
                for embedd in embeddeds:
                    mimetype, subtype = cls.guess_mimetype(embedd["name"])
                    mail_embeddeds.append((embedd["bytes"], mimetype, subtype, embedd["name"], None))

            payload, mail_from, rcpt_to, msg_id = pyzmail.compose_mail(
                os.environ.get("FROM"), [email], subject, "Utf-8", None,
                html=(html, "Utf-8"),
                attachments=mail_attachments,
                embeddeds=mail_embeddeds
            )

            result = pyzmail.send_mail(
                payload, os.environ.get("FROM"), rcpt_to, os.environ.get("SMTP_HOST"), os.environ.get("SMTP_PORT"), 'ssl',
                smtp_login=os.environ.get("SMTP_LOGIN"), smtp_password=os.environ.get("SMTP_PASSWORD")
            )
            if isinstance(result, str):
                raise EmailError(result)
            return True if result == {} else False
        except Exception as err:
            raise EmailError(str(err))

    @classmethod
    def send_sms(cls, phone, text):
        """ Выполняет отправку смс-сообщения
        :param phone:
        :param text:
        :return:
        """
        if os.environ.get("SMS_BEFORE"):
            text = "{before}\n{text}".format(before=os.environ.get("SMS_BEFORE"), text=text)
        if os.environ.get("SMS_AFTER"):
            text = "{text}\n{after}".format(after=os.environ.get("SMS_AFTER"), text=text)
        r = SMSC().send_sms(
            normalize_phone_number(phone).replace("+", ""),
            text,
            translit=os.environ.get("SMS_TRANSLIT", 0),
            sender=os.environ.get("SMS_SENDER", False)
        )
        if not r:
            raise SmsError
        return True


def normalize_phone_number(number: str) -> str:
    """ Приводит номер к правильному строковому представлению
    :param number: Номер телефона
    """
    return "+%s" % re.sub("[^\d]", "", str(number))
