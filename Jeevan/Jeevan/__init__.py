def db_connect():
    import pymysql
    con = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='JeevanDB',
    )

    return con
