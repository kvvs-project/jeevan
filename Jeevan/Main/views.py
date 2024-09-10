import os
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib import messages
from Jeevan import db_connect
from django.shortcuts import redirect
import time

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
    try :
        con = db_connect()
        cur = con.cursor()

        userName = request.POST["uname"]
        userPass = request.POST["pass"]

        query = """
            SELECT * FROM UserLogin 
            WHERE userID = %s AND password = %s
        """
        cur.execute(query, (userName, userPass))

        if cur.rowcount == 0:
            msg = "Invalid User ID or Password"
            return render(request, "login.html", {'message': msg})

        userType = userName[0].upper()

        if userName == "admin":
            return render(request, "adminDash.html")

        if userType == 'H':
            query = """
                SELECT *
                FROM HospitalApproval 
                WHERE id = %s
            """
            cur.execute(query, (userName,))
            records = cur.fetchall()
            print(records, type(records))

            if cur.rowcount == 0:
                msg = "Please wait for Approval"
                return render(request, "login.html", {'message': msg})
            else : 
                if records[0][1] == "No":

                    msg = "Approval Rejected"
                    return render(request, "login.html", {'message': msg})

                query = """
                    SELECT photoName, id, name, place, Location, pin, phone, District, Email, type, hasbloodbank, proofName, regdate
                    FROM Hospital
                    WHERE id = %s
                """
                cur.execute(query, (userName,))
                records = cur.fetchall()

                query = """
                    DELETE FROM UserSession WHERE type = 'H'
                """
                cur.execute(query)
                con.commit()

                query = """
                    INSERT INTO UserSession (ID, type) VALUES (%s, 'H')
                """
                cur.execute(query, (userName,))
                con.commit()

                return render(request, "hospitaldashboard.html", {'records': records})

        elif userType == 'D':
            query = """
                SELECT *
                FROM DonorApproval 
                WHERE id = %s
            """
            cur.execute(query, (userName,))
            records = cur.fetchall()
            print(records, type(records))

            if cur.rowcount == 0:
                msg = "Please wait for Approval"
                return render(request, "login.html", {'message': msg})
            else : 
                if records[0][1] == "No":
                    msg = "Approval Rejected"
                    return render(request, "login.html", {'message': msg})

                query = """
                    SELECT DonorID, HospitalID, Name, Gender, BloodGroup, TypeOfDonation, DOB, Pin, Place, District, Address, Phone, Email, photo, MedicalReport, RegDate
                    FROM Donor
                    WHERE donorid = %s
                """
                cur.execute(query, (userName,))
        
                records = cur.fetchall()
                query = """
                    DELETE FROM UserSession WHERE type = 'D'
                """
                cur.execute(query)
                con.commit()
        
                query = """
                    INSERT INTO UserSession (ID, type) VALUES (%s, 'D')
                """
                cur.execute(query, (userName,))
                con.commit()
        
                return render(request, "donordashboard.html", {'records': records})

        elif userType == 'P':
            query = """
                SELECT *
                FROM PatientApproval 
                WHERE id = %s
            """
            cur.execute(query, (userName,))
            records = cur.fetchall()
            print(records, type(records))

            if cur.rowcount == 0:
                msg = "Please wait for Approval"
                return render(request, "login.html", {'message': msg})
            else : 
                if records[0][1] == "No":
                    msg = "Approval Rejected"
                    return render(request, "login.html", {'message': msg})

                query = """
                    SELECT * FROM Patient
                    WHERE patientid = %s
                """
                cur.execute(query, (userName,))
                records = cur.fetchall()
                query = """
                    DELETE FROM UserSession WHERE type = 'P'
                """
                cur.execute(query)
                con.commit()

                query = """
                    INSERT INTO UserSession (ID, type) VALUES (%s, 'P')
                """
                cur.execute(query, (userName,))
                con.commit()

            return render(request, "patientdashboard.html", {'records': records})

        msg = "Invalid User ID or Password"
        return render(request, "login.html", {'message': msg})
    except BaseException as e: # catch logs all kind of exceptions like db to request
        errorMsg = f'''
        " time {time.strftime('%H:%M:%S')} "," {type(e).__name__}: ", " {str(e)} ",
        '''
        storage = messages.get_messages(request)
        for message in storage:
            print(message) # print old message and clear them
        request.session['has_error'] = True # set a session token to show error page
        messages.error(request, errorMsg)
        return redirect("error") # incase of an exception redirect user to the error page
    finally:
        con.close()


def error_msg(request):
    if not request.session.get('has_error', False):
        return redirect('/')
    request.session['has_error'] = False
    return render(request, "error.html")