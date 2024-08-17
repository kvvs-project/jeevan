import os
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from Jeevan import db_connect
import time


def donor_pre_reg(request):
    return render(request, "donorprereg.html")


def donor_reg(request):
    con = db_connect()
    cur = con.cursor()
    district = request.POST["dist"]
    query = "select Name , ID, Place,District from Hospital where ID in ( select ID from HospitalApproval where status = 'Yes') and District = '" + district + "'"
    cur.execute(query)
    records = cur.fetchall()
    con.commit()

    return render(request, "donorreg.html", {'records': records, 'dist': district})


def validate_donor_reg(request):
    # establish db connectivity
    con = db_connect()
    cur = con.cursor()
    # create fs object
    fs = FileSystemStorage()

    # generate registration date
    date = time.strftime('%Y-%m-%d %H:%M:%S')

    # get data from client
    name = request.POST['name']
    place = request.POST['place']
    gender = request.POST['gender']
    pin = request.POST['pin']
    hid = request.POST['hospital']
    bloodtype = request.POST['blood']
    phone = request.POST['phone']
    district = request.POST['dist']
    DType = request.POST['type']
    email = request.POST['email']
    address = request.POST['address']
    dob = request.POST['dob']

    password = request.POST['pass']

    report = request.FILES["medicalReport"]
    reportName = fs.save("static/data/donor/proof/" + report.name, report)
    reportName = reportName[24:]

    photo = request.FILES["photo"]
    photoName = fs.save("static/data/donor/photo/" + photo.name, photo)
    photoName = photoName[24:]

    did = "D1000"
    query = "select * from Donor order by donorID desc"
    cur.execute(query)
    records = cur.fetchall()
    for row in records:
        did = row[0]
        break

    didNoSuffix = did[1:]
    didNew = int(didNoSuffix)
    didNew = didNew + 1
    did = "D" + str(didNew)

    query = "insert into Donor(DonorID, HospitalID, Name, Gender, BloodGroup, TypeOfDonation, DOB, Pin, Place, District, Address, Phone, Email, photo, MedicalReport, RegDate) values ( '" + did + "','" + hid + "','" + name + "','" + gender + "','" + bloodtype + "','" + DType + "','" + dob + "','" + pin + "','" + place + "','" + district + "','" + address + "','" + phone + "','" + email + "','" + photoName + "','" + reportName + "','"  + date + "')"
    print(query)
    cur.execute(query)
    con.commit()

    query = "insert into UserLogin values ('" + did + "','" + password + "')"
    cur.execute(query)
    con.commit()
    msg = "ok stored"

    query = "select Name , ID, Place,District from Hospital where ID in ( select ID from HospitalApproval where status = 'Yes') and District = '" + district + "'"
    cur.execute(query)
    records = cur.fetchall()
    con.commit()

    return render(request, "donorreg.html", {'message': msg, 'records': records, 'dist': district})


def donor_new_organ_donation(request):
    con = db_connect()
    cur = con.cursor()

    query = "Select * from OrganDonationTypes"
    cur.execute(query)
    records = cur.fetchall()

    return render(request, "donorneworgandonation.html", {'records': records})


def validate_donor_new_organ_donation(request):
    con = db_connect()
    cur = con.cursor()
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    organName = request.POST['name']

    query = "select id from UserSession where type = 'D'"
    cur.execute(query)
    records = cur.fetchall()
    status = "Y"
    did = ""
    for row in records:
        did = row[0]
        break

    query = f"SELECT status FROM DonorOrganStatus WHERE ID = '{did}' AND OrganName = '{organName}'"
    cur.execute(query)
    print(query)
    records = cur.fetchall()
    previousDonationStatus = ""
    for row in records:
        previousDonationStatus = row[0]
        break
    print(records)

    if cur.rowcount == 0:
        query = "insert into DonorOrganStatus values ('" + did + "','" + organName + "','" + status + "','" + date + "')"
        print(query)
        cur.execute(query)
        con.commit()
        query = "Select * from OrganDonationTypes"
        cur.execute(query)
        records = cur.fetchall()
        msg = "Registration successful"
        return render(request, "donorneworgandonation.html", {'records': records, 'message': msg})
    elif previousDonationStatus == 'N':
        query = f"UPDATE DonorOrganStatus SET status = 'Y' WHERE ID = '{did}' AND organName = '{organName}'"
        print(query)
        cur.execute(query)
        con.commit()
        query = "Select * from OrganDonationTypes"
        cur.execute(query)
        records = cur.fetchall()
        msg = "Registration successful"
        return render(request, "donorneworgandonation.html", {'records': records, 'message': msg})
    else:
        msg = f"You have already registered your {organName} for donation"
        query = "Select * from OrganDonationTypes"
        cur.execute(query)
        records = cur.fetchall()
        return render(request, "donorneworgandonation.html", {'records': records, 'message': msg})


def donor_organ_donation_status(request):
    con = db_connect()
    cur = con.cursor()
    did = request.POST['id']
    query = "select OrganName,Date from DonorOrganStatus where ID = '" + did + "' and Status = 'Y'"
    cur.execute(query)
    records = cur.fetchall()
    return render(request, "donororganstatus.html", {'records': records})


def donor_cancel_organ_donation(request):
    con = db_connect()
    cur = con.cursor()
    did = request.POST['id']
    query = "select ID,OrganName,Date from DonorOrganStatus where ID = '" + did + "' and Status = 'Y'"
    cur.execute(query)
    records = cur.fetchall()
    return render(request, "donorcancelorgandonation.html", {'records': records})


def validate_donor_cancel_organ_donation(request):
    con = db_connect()
    cur = con.cursor()
    did = request.POST['donorID']
    organName = request.POST['organ']
    query = "update DonorOrganStatus set Status = 'N' where ID = '" + did + "' and  OrganName = '" + organName + "'"
    cur.execute(query)
    con.commit()
    query = "select ID,OrganName,Date from DonorOrganStatus where ID = '" + did + "' and Status = 'Y'"
    cur.execute(query)
    records = cur.fetchall()
    msg = "Canceled successfully"
    return render(request, "donorcancelorgandonation.html", {'records': records, 'message': msg})
