import configparser
import MySQLdb.cursors
import sys
sys.path.append('..')
config = configparser.ConfigParser()
config.read('.config/config.ini')

def connect():
    return MySQLdb.connect(host = config['mysqlDB']['host'],
                           user = config['mysqlDB']['user'],
                           passwd = config['mysqlDB']['pass'],
                           db = config['mysqlDB']['db'])
