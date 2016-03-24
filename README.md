	
### Пример docker-compose
	app:
		...
		links:
			- notifications

	notifications:
  		container_name: notifications
  		image: somerepo/notifications
  		environment:
   			- FROM=
   			- SMTP_LOGIN=
   			- SMTP_PASSWORD=
   			- SMTP_HOST=
   			- SMTP_PORT=

   			- SMS_SENDER=
   			- SMSC_LOGIN=
   			- SMSC_PASSWORD=
   			- SMSC_POST=1
   			- SMSC_HTTPS=1
   			- SMSC_CHARSET=utf-8
   			- SMSC_DEBUG=0


### Пример использования микросервиса
	
	import base64
	from envi import microservice

    def send_email(email, subject, content):
        """
        Отправка email
        :param email:
        :param subject:
        :param content:
        :return:
        """
        return microservice(
            "http://notifications/send_email", {
                "address": email, "subject": subject,
                "base64": base64.b64encode(content).decode()
            }
        )


    @classmethod
    def send_sms(email, content):
        """ Отправка смс
        :param email:
        :param content:
        :return:
        """
        return microservice("http://notifications/send_sms", {"address": email, "text": content})
