import cx_Oracle

def getDBconnection(user,password):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', 'xe')
    con = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)
    return con

def shutDownConnection(con):
    con.close()
