def db_connect():
    import pymysql
    con = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='JeevanDB',
    )

    return con

def auth_check(userId, token, **kwargs):
    con = db_connect()
    cur = con.cursor()

    # user type is an optional parameter to check user access control
    userType = kwargs.get("userType" , None)

    try:
        if userId is None or token is None:
            raise TypeError(f"Error: The argument userID or token is missing a value.\nuserId: {userId} token: {token}")

        # Check if userId and token are valid (neither None nor 0)
        if userId and token:
            query = """
                SELECT type FROM UserSession WHERE id = %s AND token = %s
            """
            params = [userId, token]
            if userType:
                query += " AND type = %s"
                params.append(userType)
            cur.execute(query, params)
            return cur.rowcount != 0
    except TypeError as e:
        print(e)
        return False
    finally:
        con.close()
