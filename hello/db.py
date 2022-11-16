import pymssql

class DBHelper:
    def __connect__(self):
        self.con = pymssql.connect(host = r'213.140.22.237\SQLEXPRESS', user = r'elsherbini.mohamed',password= r'xxx123##', database= r'elsherbini.mohamed')
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.close()
# send one = True if want to return single row
    def fetch(self, sql,data,one=None):
        self.__connect__()
        self.cur.execute(sql,data)
        if one:
            result=self.cur.fetchone()
        else:
            result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def adddata(self, sql,data):
        self.__connect__()
        self.cur.execute(sql,data)
        self.con.commit()
        self.__disconnect__()

