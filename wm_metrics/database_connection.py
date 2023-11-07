"""Connection to the database."""

import os

import MySQLdb


def get_commons_db():
    """Returns an instance of MySQLdb.connect() to tool labs SQL for Wikimedia Commons"""
    return MySQLdb.connect(host="commonswiki.labsdb",
                           db="commonswiki_p",
                           read_default_file=os.path.expanduser("~/replica.my.cnf"),
                           charset='utf8')
