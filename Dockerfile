FROM centos:7

RUN yum install -y epel-release
RUN yum update -y && \
	yum install -y httpd sqlite3 python-pip which

RUN pip install --upgrade pip setuptools virtualenv && pip install pipenv

RUN mkdir -p /var/www/webapps/certmanager

ADD . /var/www/webapps/certmanager

RUN cd /var/www/webapps/certmanager/ && pipenv install --system

ENTRYPOINT ["/var/www/webapps/certmanager/docker/entrypoint.sh"]
