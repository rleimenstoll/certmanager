FROM centos:7

RUN yum install -y epel-release
RUN yum update -y && \
	yum install -y httpd sqlite3 python-pip which mysql-devel gcc

RUN pip install --upgrade pip setuptools virtualenv && pip install pipenv

RUN rm -rf /etc/httpd/conf.d

ADD docker/application.conf /etc/httpd/conf.d/application.conf

RUN mkdir -p /var/www/webapps/certmanager

ADD . /var/www/webapps/certmanager


RUN cd /var/www/webapps/certmanager/ && pipenv install --system

ENTRYPOINT ["/var/www/webapps/certmanager/docker/entrypoint.sh"]
