FROM centos:7

ENV WORKON_HOME=/var/www/webapps/envs/

ENV PYCURL_SSL_LIBRARY=nss

RUN yum install -y epel-release

RUN yum update -y && \
	yum install -y httpd sqlite3 python-pip which mysql-devel gcc python-devel mod_wsgi libcurl-devel

RUN pip install --upgrade pip setuptools virtualenv && pip install pipenv

RUN rm -rf /etc/httpd/conf.d

ADD docker/application.conf /etc/httpd/conf.d/application.conf

RUN mkdir -p /var/www/webapps/envs

RUN mkdir -p /var/www/webapps/certmanager

ADD . /var/www/webapps/certmanager

RUN cd /var/www/webapps/certmanager/ && pipenv install

RUN chown -R apache:apache /var/www/webapps/

ENTRYPOINT ["/var/www/webapps/certmanager/docker/entrypoint.sh"]
