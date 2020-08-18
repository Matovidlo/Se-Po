""" This module was created by Martin Vasko
    Contains only runtime analysis commands that are utilized for docker.
"""
import enum


class RunAnalysisCommands(enum.Enum):
    PHP = 'RUN ./vendor/phpstan/phpstan/phpstan analyse -l 8 {files} ||true \n'\
          'RUN ./vendor/phan/phan/phan --allow-polyfill-parser -S '\
          '--analyze-twice -m text -o result.txt {files} || true'
    VAGRANT_CMD = 8*' ' + '{tool} {options} {files}\n'
