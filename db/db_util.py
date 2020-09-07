import os
import sqlite3


def get_connection():
    db_file = os.path.join(os.getcwd(), 'db', 'data.db')
    return sqlite3.connect(db_file, isolation_level=None)

 # todo change name to id
 # add user table