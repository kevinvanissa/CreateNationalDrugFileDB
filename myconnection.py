import MySQLdb


class DBconnection(object):

    def __init__(self):
        self.user = "root"
        self.password = ""
        self.host = "localhost"
        self.db = "emr_ndf"
        #self.con = MySQLdb.connect(self.host, self.user, self.password, self.db, unix_socket='/opt/lampp/var/mysql/mysql.sock')
        #self.con = MySQLdb.connect(self.host, self.user, self.password, self.db, unix_socket='/var/run/mysqld/mysqld.sock')
        self.con = MySQLdb.connect(self.host, self.user, self.password, self.db)
        self.cursor = self.con.cursor()
        self.error = MySQLdb.Error
    def getConnection(self):
        return self.con

    def getCursor(self):
        return self.cursor

    def getErrorHandler(self):
        return self.error
