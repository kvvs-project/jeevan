import os
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from Jeevan import db_connect
import time


def home_page(request):
    return render(request, "home.html")


def find_donors(request):
    return render(request, "find.html")


def signup_page(request):
    return render(request, "signup.html")


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
        unSuffix = userName[0]
        if unSuffix == 'H':
            query = " select * from UserLogin where userID ='" + userName + "' and password = '" + userPass + "'"
            cur.execute(query)
            if cur.rowcount == 0:
                msg = "invalid Username / Id or password"
                return render(request, "login.html", {'message': msg})
            else:
                query = "select * from HospitalApproval where id = '" + userName + "'"
                cur.execute(query)
                status = ""
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
                msg = "invalid Username / Id or password"
                return render(request, "login.html", {'message': msg})
            else:
                query = "select * from DonorApproval where id = '" + userName + "'"
                cur.execute(query)
                status = ""
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
                msg = "invalid Username / Id or password"
                return render(request, "login.html", {'message': msg})
            else:
                query = "select * from PatientApproval where id = '" + userName + "'"
                cur.execute(query)
                status = ""
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

    query = "insert into UserLogin values ('" + hid + "','" + password + "')"
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


# noinspection PyUnusedLocal
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


def hospital_organ_request_approval(request):
    con = db_connect()
    cur = con.cursor()
    hid = request.POST['id']

    query = f"select RequestID,PatientID,OrganName,Request,RequestDate from PatientOrganRequest where HospitalID = '{hid}' and requestID not in (select requestID from PatientOrganRequestApproval )"
    cur.execute(query)
    records = cur.fetchall()
    return render(request, "hospitalorganrequestapproval.html", {'records': records})


def hospital_show_organ_approval_details(request):
    con = db_connect()
    cur = con.cursor()
    rid = request.POST['rid']
    pid = request.POST['id']

    query = "select patientID,HospitalID,Name,Gender,BloodGroup,DOB,Pin,Place,District,Address,Phone,Email,photo,MedicalReport,RegDate from Patient where patientid = '" + pid + "'"
    cur.execute(query)
    records = cur.fetchall()
    print(query, records)
    return render(request, "hospitalorganrequestdetail.html", {'records': records, 'RequestID': rid})


# noinspection PyUnusedLocal
def hospital_validate_organ_request_approval(request):
    con = db_connect()
    cur = con.cursor()

    rid = request.POST['rid']
    pid = request.POST['pid']
    status = request.POST['status']
    comment = request.POST['comment']
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    msg = ""

    query = f"select RequestID from PatientOrganRequestApproval where RequestID = '{rid}' "
    print(query)
    cur.execute(query)
    print(cur.fetchall())

    if cur.rowcount == 0:
        query = "insert into PatientOrganRequestApproval values ('" + rid + "','" + status + "','" + comment + "','" + date + "')"
        print(query)
        cur.execute(query)
        con.commit()
    else:
        query = f"update PatientOrganRequestApproval set status = '{status}', comment = '{comment}', date = '{date}' where RequestID = '{rid}'"
        print(query)
        cur.execute(query)
        con.commit()

    if status == "Yes":
        msg = "Approved Successfully"
    else:
        msg = "Request not Approved"

    query = "select patientID,HospitalID,Name,Gender,BloodGroup,DOB,Pin,Place,District,Address,Phone,Email,photo,MedicalReport,RegDate from Patient where patientid = '" + pid + "'"
    cur.execute(query)
    records = cur.fetchall()

    return render(request, "hospitalorganrequestdetail.html", {'records': records, 'RequestID': rid, 'message': msg})


def hospital_cancel_patient_organ_request(request):
    con = db_connect()
    cur = con.cursor()
    hid = request.POST['id']

    query = f"select RequestID,PatientID,OrganName,Request,RequestDate from PatientOrganRequest where HospitalID  = '{hid}' and RequestID in (select RequestID from PatientOrganRequestApproval where status = 'Yes' )"
    cur.execute(query)
    records = cur.fetchall()
    print(records)

    return render(request, "hospitalcancelpatientorganrequest.html", {'RequestDetails': records})


def validate_hospital_cancel_patient_organ_request(request):
    con = db_connect()
    cur = con.cursor()

    rid = request.POST['rid']
    query = f"update PatientOrganRequestApproval set status = 'No' where RequestID = '{rid}'"
    print(query)
    cur.execute(query)
    con.commit()
    msg = "successfully canceled the request"
    query = "select id from UserSession where type = 'H'"
    cur.execute(query)
    records = cur.fetchall()
    hid = ""
    for row in records:
        hid = row[0]
        break

    query = f"select RequestID,PatientID,OrganName,Request,RequestDate from PatientOrganRequest where HospitalID  = '{hid}' and RequestID in (select RequestID from PatientOrganRequestApproval where status = 'Yes' )"
    print(query)
    cur.execute(query)
    records = cur.fetchall()
    print(records)
    return render(request, "hospitalcancelpatientorganrequest.html", {'message': msg, 'RequestDetails': records})


def hospital_organ_transplantation(request):
    con = db_connect()
    cur = con.cursor()

    hid = request.POST['id']

    query = f"select RequestID,PatientID,OrganName,Request,RequestDate from PatientOrganRequest where HospitalID  = '{hid}' and RequestID in (select RequestID from PatientOrganRequestApproval where status = 'Yes' )"

    cur.execute(query)
    records = cur.fetchall()

    return render(request, "hospitalorgantransplantation.html", {'records': records, 'HospitalID': hid})


def hospital_organ_transplantation_details(request):
    con = db_connect()
    cur = con.cursor()

    query = "delete from OrganDonorListCache"
    cur.execute(query)
    con.commit()

    currentDate = str(time.strftime('%Y-%m-%d'))

    hid = request.POST['hid']
    rid = request.POST['rid']
    pid = request.POST['pid']

    query = f"select patientID, HospitalID, Name, Gender, BloodGroup, DOB, Pin, Place, District, Address, Phone, Email, Photo, MedicalReport from Patient where patientID = '{pid}'"
    cur.execute(query)
    PatientDetails = cur.fetchall()

    query = f"select RequestID, PatientID, HospitalID, OrganName, Request, RequestDate from PatientOrganRequest where requestID = '{rid}'"
    cur.execute(query)
    RequestDetails = cur.fetchall()
    organName = ""
    for row in RequestDetails:
        organName = row[3]
        break

    query = f"select Donorid,Name,Place,DOD,RegDate from Donor where HospitalID = '{hid}' and DonorID in (select ID from DonorApproval where Status = 'Yes') and donorID in ( select id from DonorOrganStatus where OrganName = '{organName}' and Status = 'Y') "
    print("fetch list : ", query)
    cur.execute(query)
    DonorDetails = cur.fetchall()
    print("before loop : ", DonorDetails)

    for row in DonorDetails:
        did = row[0]
        query = f"select DonationType from OrganDonationTypes where organName = '{organName}'"
        cur.execute(query)
        records = cur.fetchall()
        status = ""
        print("inside loop : ", row)
        for r in records:
            status = r[0]
            break
        if status == 'A':
            query = f"insert into OrganDonorListCache+ values ('{row[0]}','{row[1]}','{row[2]}','{row[3]}','{row[4]}')"
            print("if alive : ", query)
            cur.execute(query)
            con.commit()
        elif status == 'P':
            query = f"select * from OrganTransplantation where did = '{did}' and RequestID in ( select RequestID from PatientOrganRequest where organName = '{organName})'"
            cur.execute(query)
            if cur.rowcount(0):
                query = f"insert into OrganDonorListCache values ('{row[0]}','{row[1]}','{row[2]}','{row[3]}','{row[4]}')"
                print("if partial : ", query)
                cur.execute(query)
                con.commit()
        else:
            dateOfDeath = str(row[3])
            print("dod : ", dateOfDeath, "\nc date : ", currentDate, "\nquery : ", query)
            if currentDate == dateOfDeath:
                query = f"select requestID from PatientOrganRequest where requestId in (select requestID from OrganTransplantation where DonorID = '{did}') and organName = '{organName}'"
                print("if freshly dead : ", query)
                cur.execute(query)
                print("values",cur.fetchall())
                if cur.rowcount == 0:
                    query = f"insert into OrganDonorListCache values ('{row[0]}','{row[1]}','{row[2]}','{row[3]}','{row[4]}')"
                    print("if dead : ", query)
                    cur.execute(query)
                    con.commit()

    query = "select * from OrganDonorListCache"
    cur.execute(query)
    DonorDetails = cur.fetchall()
    print("final : ", DonorDetails)
    return render(request, "hospitalorgantransplantationentry.html", {'PatientDetails': PatientDetails, 'RequestDetails': RequestDetails, 'DonorDetails': DonorDetails,  'organ': organName})


def hospital_organ_transplantation_entry(request):
    con = db_connect()
    cur = con.cursor()

    rid = request.POST['rid']
    pid = request.POST['pid']
    did = request.POST['did']
    organName = request.POST['organ']

    query = f"select patientID, HospitalID, Name, Gender, BloodGroup, DOB, Pin, Place, District, Address, Phone, Email, Photo, MedicalReport from Patient where patientID = '{pid}'"
    cur.execute(query)
    PatientDetails = cur.fetchall()

    query = f"select RequestID, PatientID, HospitalID, OrganName, Request, RequestDate from PatientOrganRequest where requestID = '{rid}'"
    cur.execute(query)
    RequestDetails = cur.fetchall()

    query = f"select donorID,HospitalID,Name,Gender,BloodGroup,DOB,Pin,Place,District,Address,Phone,Email,photo,MedicalReport from Donor where DonorID = '{did}'"
    print(query, did)
    cur.execute(query)
    DonorDetails = cur.fetchall()

    return render(request, "hospitalorgantransplantationdetails.html", {'PatientDetails': PatientDetails, 'RequestDetails': RequestDetails, 'DonorDetails': DonorDetails, 'rid': rid, 'did': did, 'pid': pid, 'organ': organName})


def validate_hospital_organ_transplantation_entry(request):
    con = db_connect()
    cur = con.cursor()

    tid = "T1000"
    query = "select * from OrganTransplantation order by TransplantationID desc"
    cur.execute(query)
    records = cur.fetchall()
    for row in records:
        tid = row[0]
        break
    tidNoSuffix = tid[1:]
    tidNew = int(tidNoSuffix)
    tidNew = tidNew + 1
    tid = "T" + str(tidNew)

    rid = request.POST['rid']
    pid = request.POST['pid']
    did = request.POST['did']
    organName = request.POST['organ']
    doctorName = request.POST['doctorName']
    patientCondition = request.POST['patientCondition']
    donorCondition = request.POST['donorCondition']
    operationStatus = request.POST['operationStatus']
    operationResult = request.POST['operationResult']
    surgeryDate = request.POST['surgeryDate']
    remarks = request.POST['Remarks']
    date = time.strftime('%Y-%m-%d %H:%M:%S')

    query = f"select DonationType from OrganDonationTypes where organName = '{organName}'"
    cur.execute(query)
    records = cur.fetchall()
    organStatus = ""
    for row in records:
        organStatus = row[0]
        break

    query = f"update DonorOrganStatus set status = '{organStatus}' where ID = '{did}'"
    cur.execute(query)
    con.commit()

    query = f"insert into OrganTransplantation values ('{tid}','{rid}','{did}','{pid}','{surgeryDate}','{patientCondition}','{donorCondition}','{operationStatus}','{operationResult}','{doctorName}','{remarks}','{date}')"
    cur.execute(query)
    con.commit()

    query = f"select patientID, HospitalID, Name, Gender, BloodGroup, DOB, Pin, Place, District, Address, Phone, Email, Photo, MedicalReport from Patient where patientID = '{pid}'"
    cur.execute(query)
    PatientDetails = cur.fetchall()

    query = f"select RequestID, PatientID, HospitalID, OrganName, Request, RequestDate from PatientOrganRequest where requestID = '{rid}'"
    cur.execute(query)
    RequestDetails = cur.fetchall()

    query = f"select donorID,HospitalID,Name,Gender,BloodGroup,DOB,Pin,Place,District,Address,Phone,Email,photo,MedicalReport from Donor where DonorID = '{did}'"
    print(query, did)
    cur.execute(query)
    DonorDetails = cur.fetchall()

    return render(request, "hospitalorgantransplantationdetails.html", {'PatientDetails': PatientDetails, 'RequestDetails': RequestDetails, 'DonorDetails': DonorDetails, 'rid': rid, 'did': did, 'pid': pid, 'organ': organName})


def hospital_find_blood_donor(request):
    hid = request.POST['id']
    return render(request, "hospitalsearchblooddonor.html", {'hid': hid})


def hospital_get_blood_donor_list(request):
    con = db_connect()
    cur = con.cursor()

    searchType = request.POST['searchType']
    hid = request.POST['id']
    district = request.POST['dist']
    bloodGroup = request.POST['blood']
    gender = request.POST['gender']

    if searchType == "Local":
        query = f"select DonorID,Name,Place,District,Phone,Email from Donor where Hospitalid = '{hid}' and BloodGroup = '{bloodGroup}' and Gender = '{gender}' and District = '{district}' and (TypeOfDonation = 'Both' or TypeOfDonation = 'Blood') and DOD is null"
        print("in local : "+ query)
        cur.execute(query)
        records = cur.fetchall()
        print(records)
    else:
        query = f"select DonorID,Name,Place,District,Phone,Email from Donor where BloodGroup = '{bloodGroup}' and Gender = '{gender}' and District = '{district}' and (TypeOfDonation = 'Both' or TypeOfDonation = 'Blood') and DOD is null"
        print("in global : "+ query)
        cur.execute(query)
        records = cur.fetchall()
        print(records)

    return render(request, "hospitalsearchblooddonorlist.html", {'records': records})


def hospital_get_blood_donor_details(request):
    con = db_connect()
    cur = con.cursor()

    did = request.POST['did']
    currentDate = time.strftime('%Y-%m-%d')
    lastDate = ""

    query = f"select donorID,HospitalID,Name,Gender,BloodGroup,DOB,Pin,Place,District,Address,Phone,Email,photo,MedicalReport from donor where donorID = '{did}'"
    cur.execute(query)
    DonorDetails = cur.fetchall()

    query = f"select Blood.Date, Blood.Time, Blood.UnitOfBlood, Blood.Remarks, Hosp.ID, Hosp.Name, Hosp.Place From BloodDonation Blood Join Hospital Hosp where Blood.DonorID = '{did}' and Hosp.Id = Blood.HospitalID order by Blood.Date desc "
    cur.execute(query)
    DonationRecords = cur.fetchall()

    if cur.rowcount != 0:
        for row in DonationRecords:
            lastDate = str(row[0])
            break

        currentTime = time.mktime(time.strptime(currentDate, '%Y-%m-%d'))
        lastTime = time.mktime(time.strptime(lastDate, '%Y-%m-%d'))
        diffInSec = currentTime - lastTime
        diffInDays = str(int(diffInSec / (60 * 60 * 24)))
        print(diffInDays, lastDate)

        return render(request, "hospitalgetblooddonordetails.html", {'DonorDetails': DonorDetails, 'DonationRecords': DonationRecords, 'Date': lastDate, 'Day': diffInDays, 'did': did})
    msg = "Donor doesnt have any previous donation history"
    print(msg)
    return render(request, "hospitalgetblooddonordetails.html", {'DonorDetails': DonorDetails, 'DonationRecords': DonationRecords, 'did': did, 'message': msg})


def hospital_validate_blood_donation(request):
    con = db_connect()
    cur = con.cursor()

    bid = "B1000"
    query = "select * from BloodDonation order by BDonationID desc"
    cur.execute(query)
    records = cur.fetchall()
    for row in records:
        bid = row[0]
        break

    bidNoSuffix = bid[1:]
    bidNew = int(bidNoSuffix)
    bidNew = bidNew + 1
    bid = "B" + str(bidNew)

    did = request.POST['did']
    unit = request.POST['unit']
    remarks = request.POST['remarks']
    msg = "Successfully "
    btnStatus = "Disabled"

    query = "select id from UserSession where type = 'H'"
    cur.execute(query)
    records = cur.fetchall()
    hid = ""
    for row in records:
        hid = row[0]
        break

    currentDate = time.strftime('%Y-%m-%d')
    currentTime = time.strftime('%H:%M:%S')
    lastDate = ""

    query = f"insert into BloodDonation values('{bid}','{did}','{hid}','{currentDate}','{currentTime}','{unit}','{remarks}')"
    print(query)
    cur.execute(query)
    con.commit()

    query = f"select donorID,HospitalID,Name,Gender,BloodGroup,DOB,Pin,Place,District,Address,Phone,Email,photo,MedicalReport from donor where donorID = '{did}'"
    cur.execute(query)
    DonorDetails = cur.fetchall()

    query = f"select Blood.Date, Blood.Time, Blood.UnitOfBlood, Blood.Remarks, Hosp.ID, Hosp.Name, Hosp.Place From BloodDonation Blood Join Hospital Hosp where Blood.DonorID = '{did}' and Hosp.Id = Blood.HospitalID order by Blood.Date desc "
    cur.execute(query)
    DonationRecords = cur.fetchall()

    if cur.rowcount != 0:
        for row in DonationRecords:
            lastDate = str(row[0])
            break

        currentTime = time.mktime(time.strptime(currentDate, '%Y-%m-%d'))
        lastTime = time.mktime(time.strptime(lastDate, '%Y-%m-%d'))
        diffInSec = currentTime - lastTime
        diffInDays = int(diffInSec / (60 * 60 * 24))

        return render(request, "hospitalgetblooddonordetails.html", {'DonorDetails': DonorDetails, 'DonationRecords': DonationRecords, 'Date': lastDate, 'Day': diffInDays, 'message': msg, 'btnStatus': btnStatus})

    return render(request, "hospitalgetblooddonordetails.html", {'DonorDetails': DonorDetails, 'message': msg, 'btnStatus': btnStatus})


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

    query = "insert into Donor(DonorID, HospitalID, Name, Gender, BloodGroup, TypeOfDonation, DOB, Pin, Place, District, Address, Phone, Email, photo, MedicalReport, RegDate) values ( '" + did + "','" + hid + "','" + name + "','" + gender + "','" + bloodtype + "','" + DType + "','" + dob + "','" + pin + "','" + place + "','" + district + "','" + address + "','" + phone + "','" + email + "','" + photoName + "','" + reportName + "','" + "','" + date + "')"
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


def donor_approval(request):
    con = db_connect()
    cursor = con.cursor()
    hid = request.POST['id']
    query = f"select donorid,Name,place,regdate from Donor where HospitalID = '{hid}' and donorid not in(select id from DonorApproval)"
    cursor.execute(query)
    records = cursor.fetchall()
    return render(request, "donorapproval.html", {'records': records})


def show_donor_details(request):
    con = db_connect()
    cursor = con.cursor()
    did = request.POST['donorid']
    query = "select donorID,HospitalID,Name,Gender,BloodGroup,TypeOfDonation,DOB,Pin,Place,District,Address,Phone,Email,photo,MedicalReport,RegDate from Donor where donorid = '" + did + "'"
    cursor.execute(query)
    records = cursor.fetchall()
    print(query, records)
    return render(request, "donordetails.html", {'records': records})


# noinspection PyUnusedLocal
def validate_donor_approval(request):
    did = request.POST['donorID']
    approve_status = request.POST['approve_status']
    comment = request.POST['comment']
    date = time.strftime('%Y-%m-%d %H:%M:%S')

    print(did, approve_status, comment)

    con = db_connect()
    cur = con.cursor()

    query = "insert into DonorApproval values ('" + did + "','" + approve_status + "','" + comment + "','" + date + "')"
    print(query)
    cur.execute(query)
    con.commit()

    query = "select donorID,HospitalID,Name,Gender,BloodGroup,TypeOfDonation,DOB,Pin,Place,District,Address,Phone,Email,photo,MedicalReport,RegDate from Donor where donorid = '" + did + "'"
    cur.execute(query)
    records = cur.fetchall()
    msg = ""
    if approve_status == 'Yes':
        msg = "Successfully approved Donor"
    else:
        msg = "Donor not approved"
    print(records, msg)
    return render(request, "donordetails.html", {'records': records, 'message': msg})


def download_donor_report(request):
    report = request.POST["report"]

    file_path = "./static/data/donor/proof/" + report
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def donor_new_organ_Donation(request):
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

    query = f"SELECT id FROM DonorOrganStatus WHERE ID = '{did}' AND OrganName = '{organName}'"
    cur.execute(query)
    print(query)
    records = cur.fetchall()
    print(records)

    if cur.rowcount == 0:
        query = "insert into DonorOrganStatus values ('" + did + "','" + organName + "','" + status + "','" + date + "')"
        print(query)
        cur.execute(query)
        con.commit()
        query = "select donorID,HospitalID,Name,Gender,BloodGroup,TypeOfDonation,DOB,Pin,Place,District,Address,Phone,Email,photo,MedicalReport,RegDate from Donor where donorid = '" + did + "'"
        cur.execute(query)
        records = cur.fetchall()

        return render(request, "donordashboard.html", {'records': records})
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


def admin_organ_list(request):
    con = db_connect()
    cur = con.cursor()
    query = "select * from OrganDonationTypes"
    cur.execute(query)
    records = cur.fetchall()
    return render(request, "adminorganlist.html", {'records': records})


def admin_add_new_organ(request):
    return render(request, "adminaddneworgan.html")


def admin_validate_add_new_organ(request):
    con = db_connect()
    cur = con.cursor()

    organName = request.POST['name']
    organName = organName.replace(" ", "")
    DonationType = request.POST['type']

    query = "insert into OrganDonationTypes values('" + organName + "','" + DonationType + "')"
    cur.execute(query)
    con.commit()

    msg = "Organ added successfully"

    return render(request, "adminaddneworgan.html", {'message': msg})


def patient_pre_reg(request):
    return render(request, "patientprereg.html")


def patient_reg(request):
    con = db_connect()
    cur = con.cursor()
    district = request.POST["dist"]
    query = "select Name , ID, Place,District from Hospital where ID in ( select ID from HospitalApproval where status = 'Yes') and District = '" + district + "'"
    cur.execute(query)
    records = cur.fetchall()
    con.commit()

    return render(request, "patientreg.html", {'records': records})


def validate_patient_reg(request):
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
    email = request.POST['email']
    address = request.POST['address']
    dob = request.POST['dob']

    password = request.POST['pass']

    report = request.FILES["medicalReport"]
    reportName = fs.save("static/data/patient/proof/" + report.name, report)
    reportName = reportName[26:]

    photo = request.FILES["photo"]
    photoName = fs.save("static/data/patient/photo/" + photo.name, photo)
    photoName = photoName[26:]

    pid = "P1000"
    query = "select * from Patient order by patientID desc"
    cur.execute(query)
    records = cur.fetchall()
    for row in records:
        pid = row[0]
        break

    pidNoSuffix = pid[1:]
    pidNew = int(pidNoSuffix)
    pidNew = pidNew + 1
    pid = "P" + str(pidNew)

    query = "insert into Patient values ( '" + pid + "','" + hid + "','" + name + "','" + gender + "','" + bloodtype + "','" + dob + "','" + pin + "','" + place + "','" + district + "','" + address + "','" + phone + "','" + email + "','" + photoName + "','" + reportName + "','" + date + "')"
    print(query)
    cur.execute(query)
    con.commit()

    query = "insert into UserLogin values ('" + pid + "','" + password + "')"
    cur.execute(query)
    con.commit()
    msg = "ok stored"

    return render(request, "patientreg.html", {'message': msg})


def patient_approval(request):
    con = db_connect()
    cursor = con.cursor()
    hid = request.POST['id']
    query = f"select patientid,Name,place,regdate from Patient where patientid not in(select id from PatientApproval) and HospitalID = '{hid}'"
    cursor.execute(query)
    records = cursor.fetchall()
    return render(request, "patientapproval.html", {'records': records})


def show_patient_details(request):
    con = db_connect()
    cursor = con.cursor()
    pid = request.POST['patientid']
    query = "select * from Patient where patientid = '" + pid + "'"
    cursor.execute(query)
    records = cursor.fetchall()
    print(query, records)
    return render(request, "patientdetails.html", {'records': records})


# noinspection PyUnusedLocal
def validate_patient_approval(request):
    pid = request.POST['patientID']
    approve_status = request.POST['approve_status']
    comment = request.POST['comment']
    date = time.strftime('%Y-%m-%d %H:%M:%S')

    print(pid, approve_status, comment)

    con = db_connect()
    cur = con.cursor()

    query = "insert into PatientApproval values ('" + pid + "','" + approve_status + "','" + comment + "','" + date + "')"
    print(query)
    cur.execute(query)
    con.commit()

    query = "select * from Patient where patientid = '" + pid + "'"
    cur.execute(query)
    records = cur.fetchall()
    msg = ""
    if approve_status == 'Yes':
        msg = "Successfully approved Patient"
    else:
        msg = "Patient not approved"
    print(records, msg)
    return render(request, "patientdetails.html", {'records': records, 'message': msg})


def download_patient_report(request):
    report = request.POST["report"]

    file_path = "./static/data/patient/proof/" + report
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def patient_make_new_organ_request(request):
    con = db_connect()
    cur = con.cursor()
    query = "select * from OrganDonationTypes"
    cur.execute(query)
    records = cur.fetchall()
    return render(request, "patientorgansearch.html", {'records': records})


def patient_get_organ_hospital_list(request):
    con = db_connect()
    cur = con.cursor()

    district = request.POST['dist']
    organ = request.POST['organ']
    bloodGroup = request.POST['blood']
    gender = request.POST['gender']

    query = f"select ID,Name,Place,Location,Pin,Phone,District,Email from Hospital where ID in ( select HospitalID from Donor where District = '{district}' and Gender = '{gender}' and BloodGroup = '{bloodGroup}' and donorID in (select ID from DonorApproval where status = 'Yes') and donorID in ( select ID from DonorOrganStatus where organName = '{organ}' and status = 'Y') )"
    cur.execute(query)
    records = cur.fetchall()

    return render(request, "patientgetorganhospitallist.html", {'records': records, 'organ': organ})


def patient_make_organ_donation_request(request):
    con = db_connect()
    cur = con.cursor()

    hid = request.POST['hid']
    organ = request.POST['organ']
    query = "select ID,photoName,id,name,place,Location,pin,phone,District,Email,type from Hospital where id = '" + hid + "'"
    cur.execute(query)
    records = cur.fetchall()

    return render(request, "patientmakeneworganrequest.html", {'records': records, 'organ': organ})


def patient_validate_organ_donation_request(request):
    con = db_connect()
    cur = con.cursor()
    date = time.strftime('%Y-%m-%d %H:%M:%S')

    rid = "R1000"
    query = "select RequestID from PatientOrganRequest order by RequestID desc"
    cur.execute(query)
    records = cur.fetchall()
    for row in records:
        rid = row[0]
        break

    ridNoSuffix = rid[1:]
    ridNew = int(ridNoSuffix)
    ridNew = ridNew + 1
    rid = "R" + str(ridNew)

    query = "select id from UserSession where type = 'P'"
    cur.execute(query)
    records = cur.fetchall()
    pid = ""
    for row in records:
        pid = row[0]
        break

    hid = request.POST['hid']
    organ = request.POST['organ']
    comment = request.POST['comment']

    query = f"insert into PatientOrganRequest values ('{rid}','{pid}','{hid}','{organ}','{comment}','{date}')"
    cur.execute(query)
    con.commit()

    query = "select ID,photoName,id,name,place,Location,pin,phone,District,Email,type from Hospital where id = '" + hid + "'"
    cur.execute(query)
    records = cur.fetchall()
    msg = "Request successfully. Please wait for approval"

    return render(request, "patientmakeneworganrequest.html", {'records': records, 'organ': organ, 'message': msg})


def guest_find_organ_donor(request):
    con = db_connect()
    cur = con.cursor()
    query = "select * from OrganDonationTypes"
    cur.execute(query)
    records = cur.fetchall()
    return render(request, "guestsearchorgandonor.html", {'records': records})


def guest_get_organ_hospital_list(request):
    con = db_connect()
    cur = con.cursor()

    district = request.POST['dist']
    organ = request.POST['organ']
    bloodGroup = request.POST['blood']
    gender = request.POST['gender']

    query = f"select Name,Place,Location,Pin,Phone,District,Email from Hospital where ID in ( select HospitalID from Donor where District = '{district}' and Gender = '{gender}' and BloodGroup = '{bloodGroup}' and donorID in (select ID from DonorApproval where status = 'Yes') and donorID in ( select ID from DonorOrganStatus where organName = '{organ}' and status = 'Y') )"
    print(query)
    cur.execute(query)
    records = cur.fetchall()
    print(records)
    return render(request, "guestsearchorganhospitallist.html", {'records': records})


def guest_find_blood_donor(request):
    return render(request, "guestsearchblooddonor.html")


def guest_get_blood_donor_list(request):
    con = db_connect()
    cur = con.cursor()

    district = request.POST['dist']
    bloodGroup = request.POST['blood']
    gender = request.POST['gender']

    query = f"select Name,Place,District,Phone,Email from Donor where BloodGroup = '{bloodGroup}' and Gender = '{gender}' and District = '{district}' and (TypeOfDonation = 'Both' or TypeOfDonation = 'Blood') and DOD is null"

    print(query)
    cur.execute(query)
    records = cur.fetchall()
    print(records)
    return render(request, "guestsearchblooddonorlist.html", {'records': records})


def patient_organ_request_status(request):
    con = db_connect()
    cur = con.cursor()
    pid = request.POST['id']
    print(pid)
    query = f"select RequestID,OrganName,RequestDate from PatientOrganRequest where PatientID = '{pid}'"
    cur.execute(query)
    records = cur.fetchall()
    return render(request, "patientorganrequeststatus.html", {'records': records})


# noinspection PyUnusedLocal
def patient_organ_request_details(request):
    con = db_connect()
    cur = con.cursor()
    rid = request.POST['id']
    print(rid)
    query = f"select PatientID,OrganName,Request,RequestDate from PatientOrganRequest where RequestID = '{rid}'"
    cur.execute(query)
    RequestDetails = cur.fetchall()
    query = f"select ID,name,place,Location,pin,phone,District,Email,type from Hospital where id in (select HospitalID from PatientOrganRequest where requestID = '{rid}')"
    cur.execute(query)
    HospitalDetails = cur.fetchall()
    query = f"select status,comment,Date from PatientOrganRequestApproval where RequestID = '{rid}'"
    cur.execute(query)
    ApprovalDetails = cur.fetchall()
    msg = ""
    print(RequestDetails, "\n\n", HospitalDetails, "\n\n", ApprovalDetails)
    if cur.rowcount == 0:
        msg = "Waiting for approval..."
    else:
        status = ""
        for row in ApprovalDetails:
            status = row[0]
        if status == "Yes":
            msg = "Your Request has been approved"
        else:
            msg = "Your request was denied"

    return render(request, "patientshoworganrequestdetails.html", {'RequestDetails': RequestDetails, 'HospitalDetails': HospitalDetails, 'ApprovalDetails': ApprovalDetails, 'message': msg})


def patient_cancel_organ_request(request):
    con = db_connect()
    cur = con.cursor()
    pid = request.POST['pid']

    query = f"select RequestID,HospitalID,OrganName,Request,RequestDate from PatientOrganRequest where PatientID  = '{pid}' and RequestID not in (select RequestID from PatientOrganRequestApproval )"
    cur.execute(query)
    records = cur.fetchall()
    print(records)

    return render(request, "patientcancelorganrequest.html", {'RequestDetails': records, 'pid': pid})


def validate_patient_cancel_organ_request(request):
    con = db_connect()
    cur = con.cursor()
    rid = request.POST['rid']
    pid = request.POST['pid']

    print(request, "\ntest\n", request.POST)

    query = f"delete from PatientOrganRequestApproval where RequestID = '{rid}'"
    print(query)
    cur.execute(query)
    con.commit()

    query = f" delete from PatientOrganRequest where RequestID = '{rid}'"
    print(query)
    cur.execute(query)
    con.commit()

    query = f"select RequestID,HospitalID,OrganName,Request,RequestDate from PatientOrganRequest where PatientID  = '{pid}' and RequestID not in (select RequestID from PatientOrganRequestApproval )"
    cur.execute(query)
    records = cur.fetchall()
    print(records)
    msg = 'successfully cancelled'
    return render(request, "patientcancelorganrequest.html", {'RequestDetails': records, 'pid': pid, 'message': msg, })


def serve_favicon(request):
    file_path = "./static/favicon.ico"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="image/x-icon")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    return Http404