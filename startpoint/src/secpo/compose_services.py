""" This module is created by Martin Vasko
    Some of the services are running persistently such as mysql.
    To execute queries it is necessary to compose service instead of
    creating container with running service.
"""


class Mysql:
    COMPOSE = """# Use root/example as user/password credentials
version: '3.1'

services:

    db:
        image: mysql
        command: --default-authentication-plugin=mysql_native_password
        restart: always
        environment:
          MYSQL_ROOT_PASSWORD: example
    
    adminer:
        image: adminer
        restart: always
        ports:
            - 8080:8080"""