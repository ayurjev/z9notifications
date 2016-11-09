FROM hub.dev.repaem.ru:5000/base_image_webapp

RUN pip3 install pyzmail

WORKDIR /var/www/
COPY . /var/www/

EXPOSE 80
CMD ["uwsgi", "uwsgi.ini"]