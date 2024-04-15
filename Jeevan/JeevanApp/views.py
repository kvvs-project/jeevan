from django.shortcuts import render
from Jeevan import db_connect


def home_page(request):
    return render(request, "home.html")


def user_login(request):
    return render(request, "login.html")


def validate_login(request):
    con = db_connect()
    cur = con.cursor()

    userName = request.POST["uname"]
    userPass = request.POST["pass"]

    query = "select * from UserLogin where userID = '" + userName + "' and password ='" + userPass + "'"

    cur.execute(query)

    if cur.rowcount == 0:
        msg = "invalid user id or Password"
        return render(request, "login.html", {'message': msg})
    elif userName == "admin":
        return render(request, "adminprocess.html")
    else:
        msg = "other user"
        return render(request, "login.html", {'message': msg})


def admin_change_pass(request):
    return render(request, "adminchangepass.html")


def admin_validate_change_pass(request):
    con = db_connect()
    cur = con.cursor()

    current_pass = request.POST["c_pass"]
    new_pass = request.POST["n_pass"]

    query = "select * from UserLogin where userID = 'admin' and password = '" + current_pass + "'"
    cur.execute(query)

    if cur.rowcount == 0:
        msg = "Invalid existing password"
    else:
        query = "update UserLogin set password ='" + new_pass + "'"
        cur.execute(query)
        con.commit()
        msg = "password change successful"
    return render(request, "adminchangepass.html", {'message': msg})
