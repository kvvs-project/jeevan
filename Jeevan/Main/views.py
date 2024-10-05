import os
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib import messages
from Jeevan import db_connect, auth_check
from django.shortcuts import redirect
import time
import uuid


def home_page(request):
    con = db_connect()
    cur = con.cursor()
    
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if userId != 0 and token != 0:
        query = """
            select type from UserSession where id = %s and token = %s
        """
        cur.execute(query, (userId, token))
        if cur.rowcount != 0 :
            userType = cur.fetchall()[0][0]
            if userType == 'H':
                query = """
                    SELECT photoName, id, name, place, Location, pin, phone, District, Email, type, hasbloodbank, proofName, regdate
                    FROM Hospital
                    WHERE id = %s
                """
                cur.execute(query, (userId,))
                records = cur.fetchall()
                return render(request, "hospitaldashboard.html", {'records': records})
            elif userType == 'D':
                query = """
                    SELECT DonorID, HospitalID, Name, Gender, BloodGroup, TypeOfDonation, DOB, Pin, Place, District, Address, Phone, Email, photo, MedicalReport, RegDate
                    FROM Donor
                    WHERE donorid = %s
                """
                cur.execute(query, (userId,))
                records = cur.fetchall()
                return render(request, "donordashboard.html", {'records': records})
            elif userType == 'P':
                query = """
                    SELECT * FROM Patient
                    WHERE patientid = %s
                """
                cur.execute(query, (userId,))
                records = cur.fetchall()

                return render(request, "patientdashboard.html", {'records': records})

            elif userType == 'A':
                return render(request, "adminDash.html")
    
    return render(request, "home.html")


def signup_page(request):
    return render(request, "signup.html")


def serve_favicon(request):
    file_path = "./static/favicon.ico"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="image/x-icon")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    return Http404


def user_login(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)
    if auth_check(userId, token):
        return redirect("/")
    
    response = render(request, "login.html")
    response.delete_cookie("user-id")
    response.delete_cookie("user-token")
    return response


def validate_login(request):
    con = db_connect()
    cur = con.cursor()

    userName = request.POST["uname"]
    userPass = request.POST["pass"]
    userType = userName[0].upper()
    token = ""

    def successful_login(user, token, usrType ):
        con = db_connect()
        cur = con.cursor()
        query = """
            DELETE FROM UserSession WHERE id = %s
        """
        cur.execute(query, (user))
        con.commit()
        token = str(uuid.uuid4()).split("-")[0]
        query = """
            INSERT INTO UserSession VALUES (%s, %s, %s)
        """
        cur.execute(query, (user,usrType, token))
        con.commit()
        response = redirect("/")
        response.set_cookie('user-id', user, max_age=604800)
        response.set_cookie('user-token', token, max_age=604800)
        con.close()
        return response

    query = """
        SELECT * FROM UserLogin 
        WHERE userID = %s AND password = %s
    """
    cur.execute(query, (userName, userPass))

    if cur.rowcount == 0:
        msg = "Invalid User ID or Password"
        con.close()
        return render(request, "login.html", {'message': msg})
        
    if userName == "admin":
        con.close()
        return successful_login(userName, token, userType)

    approvalQuery = {
        'H' : "SELECT * FROM HospitalApproval WHERE id = %s",
        'D' : "SELECT * FROM DonorApproval WHERE id = %s",
        'P' : "SELECT * FROM PatientApproval WHERE id = %s",
    }

    if userType in approvalQuery:
        cur.execute(approvalQuery[userType], (userName.upper(),))
        records = cur.fetchall()
        print(records, type(records))
        if cur.rowcount == 0:
            msg = "Please wait for Approval"
            con.close()
            return render(request, "login.html", {'message': msg})
        else : 
            if records[0][1] == "No":
                msg = "Approval Rejected"
                con.close()
                return render(request, "login.html", {'message': msg})
            con.close()
            return successful_login(userName.upper(), token, userType)
    con.close()
    return render(request, "login.html", {'message': msg})


def error_msg(request):
    if not request.session.get('has_error', False):
        return redirect('/')
    request.session['has_error'] = False
    return render(request, "error.html")


def user_logout(request):
    response = redirect("/")
    response.delete_cookie("user-id")
    response.delete_cookie("user-token")
    return response


def change_pass(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token):
        return render(request, "changePass.html")
    msg = "auth error"
    request.session['has_error'] = True 
    messages.error(request, msg)
    return redirect("error")


def validate_change_pass(request):
    con = db_connect()
    cur = con.cursor()

    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token):
        newPass = request.POST["n_pass"]
        currentPass = request.POST["c_pass"]
        query = """
            select * from UserLogin where userID = %s and password = %s
        """
        cur.execute(query,(userId, currentPass))
        if cur.rowcount == 0:
            msg = "Invalid existing password"
        else:
            query = """
                update UserLogin set password = %s where userId = %s
            """
            cur.execute(query,(newPass, userId))
            con.commit()
            msg = "password change successful"
            con.close()
            return render(request, "changePass.html", {'message': msg, 'disabled': "disabled"})
        return render(request, "changePass.html", {'message': msg})
    msg = "authentication error"
    request.session['has_error'] = True 
    messages.error(request, msg)
    con.close()
    return redirect("error")


def privacy_policy(request):
    return render(request, "privacyPolicy.html")


def terms_of_service(request):
    return render(request, "termsOfService.html")


def about_us(request):
    return render(request, "about.html")