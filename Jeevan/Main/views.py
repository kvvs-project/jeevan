import os
from django.http import HttpResponse, Http404
from django.shortcuts import render
from Jeevan import db_connect


def home_page(request):
    return render(request, "home.html")


def signup_page(request):
    return render(request, "signup.html")


def user_login(request):
    return render(request, "login.html")


def serve_favicon(request):
    file_path = "./static/favicon.ico"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="image/x-icon")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    return Http404


def validate_login(request):
    con = db_connect()
    cur = con.cursor()

    userName = request.POST["uname"]
    userPass = request.POST["pass"]

    query = "select * from UserLogin where userID = '" + userName + "' and password ='" + userPass + "'"

    cur.execute(query)

    if cur.rowcount == 0:
        msg = "Invalid UserID or Password"
        return render(request, "login.html", {'message': msg})
    elif userName == "admin":
        return render(request, "adminprocess.html")
    else:
        unSuffix = userName[0]
        if unSuffix == 'H':
            query = " select * from UserLogin where userID ='" + userName + "' and password = '" + userPass + "'"
            cur.execute(query)
            if cur.rowcount == 0:
                msg = "Invalid UserId or Password"
                return render(request, "login.html", {'message': msg})
            else:
                query = "select * from HospitalApproval where id = '" + userName + "'"
                cur.execute(query)
                status = ""
                if cur.rowcount == 0:
                    msg = "Please wait for Approval"
                    return render(request, "login.html", {'message': msg})
                else:
                    records = cur.fetchall()
                    for row in records:
                        status = row[1]
                    print(status)

                    if status == "No":
                        msg = "Your Approval is rejected"
                        return render(request, "login.html", {'message': msg})
                    else:
                        query = "delete from UserSession where type = 'H'"
                        cur.execute(query)
                        con.commit()
                        query = "insert into UserSession values ('" + userName + "','" + unSuffix + "')"
                        cur.execute(query)
                        con.commit()
                        query = "select photoName,id,name,place,Location,pin,phone,District,Email,type,hasbloodbank,proofName,regdate from Hospital where id = '" + userName + "'"
                        cur.execute(query)
                        records = cur.fetchall()
                        return render(request, "hospitaldashboard.html", {'records': records})
        elif unSuffix == 'D':
            query = " select * from UserLogin where userID ='" + userName + "' and password = '" + userPass + "'"
            cur.execute(query)
            if cur.rowcount == 0:
                msg = "Invalid UserId or Password"
                return render(request, "login.html", {'message': msg})
            else:
                query = "select * from DonorApproval where id = '" + userName + "'"
                cur.execute(query)
                status = ""
                if cur.rowcount == 0:
                    msg = "Please wait for Approval"
                    return render(request, "login.html", {'message': msg})
                else:
                    records = cur.fetchall()
                    for row in records:
                        status = row[1]
                    print(status)

                    if status == "No":
                        msg = "Your Approval is rejected"
                        return render(request, "login.html", {'message': msg})
                    else:
                        query = "delete from UserSession where type = 'D'"
                        cur.execute(query)
                        con.commit()
                        query = "insert into UserSession values ('" + userName + "','" + unSuffix + "')"
                        cur.execute(query)
                        con.commit()
                        did = userName
                        query = "select DonorID,HospitalID,Name,Gender,BloodGroup,TypeOfDonation,DOB,Pin,Place,District,Address,Phone,Email,photo,MedicalReport,RegDate from Donor where donorid = '" + did + "'"
                        cur.execute(query)
                        records = cur.fetchall()
                        return render(request, "donordashboard.html", {'records': records})
        elif unSuffix == 'P':
            query = " select * from UserLogin where userID ='" + userName + "' and password = '" + userPass + "'"
            cur.execute(query)
            if cur.rowcount == 0:
                msg = "Invalid serId or Password"
                return render(request, "login.html", {'message': msg})
            else:
                query = "select * from PatientApproval where id = '" + userName + "'"
                cur.execute(query)
                status = ""
                if cur.rowcount == 0:
                    msg = "Please wait for approval"
                    return render(request, "login.html", {'message': msg})
                else:
                    records = cur.fetchall()
                    for row in records:
                        status = row[1]
                    print(status)

                    if status == "No":
                        msg = "Your registration is rejected"
                        return render(request, "login.html", {'message': msg})
                    else:

                        query = "delete from UserSession where type = 'P'"
                        cur.execute(query)
                        con.commit()
                        query = "insert into UserSession values ('" + userName + "','" + unSuffix + "')"
                        cur.execute(query)
                        con.commit()
                        did = userName
                        query = "select * from Patient where patientid = '" + did + "'"
                        cur.execute(query)
                        records = cur.fetchall()
                        return render(request, "patientdashboard.html", {'records': records})
        msg = "Invalid serId or Password"
        return render(request, "login.html", {'message': msg})
