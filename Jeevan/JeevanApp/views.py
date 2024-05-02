import os

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from Jeevan import db_connect
import time


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
        unSufix = userName[0]
        if unSufix == 'H':
            query = " select * from UserLogin where userID ='"+ userName + "' and password = '" + userPass + "'"
            cur.execute(query)
            if cur.rowcount == 0:
                msg = "invalid Username / Id or password"
                return render(request, "login.html", {'message': msg})
            else:
                query = "select * from HospitalApproval where id = '" + userName + "'"
                cur.execute(query)
                if cur.rowcount == 0:
                    msg = "please wait for approval"
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
                        return render(request,"hospitaldashboard.html")
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


def hospital_reg(request):
    return render(request, "hospitalreg.html")


def validate_hospital_reg(request):
    # establish db connectivity
    con = db_connect()
    cur = con.cursor()
    # create fs object
    fs = FileSystemStorage()

    # get registration date
    date = time.strftime('%Y-%m-%d %H:%M:%S')

    # get data from client
    name = request.POST['h_name']
    place = request.POST['h_place']
    location = request.POST['h_loc']
    pin = request.POST['h_pin']
    phone = request.POST['h_phone']
    district = request.POST['h_dist']
    hType = request.POST['h_type']
    email = request.POST['h_email']
    hasBloodBank = request.POST['h_bb']
    password = request.POST['h_pass']

    # get proof file and photo from client and save in static folder
    proofFile = request.FILES["h_proof"]  # get file
    proofName = fs.save("./static/data/hospital/proof/" + proofFile.name, proofFile)  # save() returns file name with path after saving file to disk
    proofName = proofName[27:]  # remove path from file name
    photoFile = request.FILES["h_photo"]
    photoName = fs.save("./static/data/hospital/photo/" + photoFile.name, photoFile)
    photoName = photoName[27:]

    # generate hospital ID
    hid = "H1000"
    query = "select * from Hospital order by ID desc"
    cur.execute(query)
    records = cur.fetchall()
    for row in records:
        hid = row[0]
        break

    hidNoSuffix = hid[1:]
    hidNew = int(hidNoSuffix)
    hidNew = hidNew + 1
    hid = "H" + str(hidNew)

    query = "insert into Hospital values ( '" + hid + "','" + name + "','" + place + "','" + location + "','" + pin + "','" + phone + "','" + district + "','" + email + "','" + hType + "','" + proofName + "','" + photoName + "','" + hasBloodBank + "','" + date + "')"
    cur.execute(query)
    con.commit()

    query = "insert into UserLogin values ('" + hid +"','" + password + "')"
    cur.execute(query)
    con.commit()
    msg = "ok stored"
    return render(request, "hospitalreg.html", {'message': msg})


def hospital_approval(request):
    con = db_connect()
    cursor = con.cursor()
    query = "select id,name,place,regdate from Hospital where id not in(select id from HospitalApproval)"
    cursor.execute(query)
    records = cursor.fetchall()
    return render(request, "hospitalapproval.html", {'records': records})


def show_hospital_details(request):
    con = db_connect()
    cursor = con.cursor()
    hid = request.POST['hid']
    query = "select photoName,id,name,place,Location,pin,phone,District,Email,type,hasbloodbank,proofName,regdate from Hospital where id = '" + hid + "'"
    cursor.execute(query)
    records = cursor.fetchall()
    return render(request, "hospitaldetails.html", {'records': records})


def download_hospital_proof(request):
    proof = request.POST["h_proof"]

    file_path = "./static/data/hospital/proof/" + proof
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def validate_hospital_approval(request):
    hid = request.POST['hid']
    approve_status = request.POST['approve_status']
    comment = request.POST['comment']
    date = time.strftime('%Y-%m-%d %H:%M:%S')

    print(hid, approve_status, comment)

    con = db_connect()
    cur = con.cursor()

    query = "insert into HospitalApproval values ('" + hid + "','" + approve_status + "','" + comment + "','" + date + "')"
    print(query)
    cur.execute(query)
    con.commit()

    query = "select photoName,id,name,place,Location,pin,phone,District,Email,type,hasbloodbank,proofName,regdate from Hospital where id = '" + hid + "'"
    cur.execute(query)
    records = cur.fetchall()
    msg = ""
    if approve_status == 'Yes':
        msg = "Successfully approved hospital"
    else:
        msg = "Hospital not approved"
    print(records, msg)
    return render(request, "hospitaldetails.html", {'records': records, 'message': msg})

