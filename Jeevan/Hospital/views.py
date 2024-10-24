import os
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from Jeevan import db_connect, auth_check
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from Main.views import thanks
import time
import pymysql
import json

def hospital_reg(request):
    return render(request, "hospitalSignUp.html")


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
    return thanks(request, userId=hid)


def patient_approval(request):
    con = db_connect()
    cursor = con.cursor()
    hid = request.COOKIES['user-id']
    query = f"select photo,patientid,Name,place,regdate from Patient where patientid not in(select id from PatientApproval) and HospitalID = '{hid}'"
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
    return render(request, "patientdetails.html", {'records': records, 'pid': pid})


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
    return render(request, "patientdetails.html", {'records': records, 'message': msg, 'disabled': "disabled"})

@csrf_exempt
def download_patient_report(request):
    report = request.POST["report"]

    file_path = "./static/data/patient/proof/" + report
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def donor_approval(request):
    con = db_connect()
    cursor = con.cursor()
    hid = request.COOKIES['user-id']
    query = f"select photo,donorid,Name,place,regdate from Donor where HospitalID = '{hid}' and donorid not in(select id from DonorApproval)"
    cursor.execute(query)
    records = cursor.fetchall()
    return render(request, "donorApproval.html", {'records': records})


def show_donor_details(request):
    con = db_connect()
    cursor = con.cursor()
    did = request.POST['donorid']
    query = "select donorID,HospitalID,Name,Gender,BloodGroup,TypeOfDonation,DOB,Pin,Place,District,Address,Phone,Email,photo,MedicalReport,RegDate from Donor where donorid = '" + did + "'"
    cursor.execute(query)
    records = cursor.fetchall()
    print(query, records)
    return render(request, "donorDetails.html", {'records': records, 'did': did})


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
    return render(request, "donorDetails.html", {'records': records, 'message': msg, 'disabled': "disabled"})


@csrf_exempt
def download_donor_report(request):
    report = request.POST["report"]

    file_path = "./static/data/donor/proof/" + report
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def hospital_organ_request_approval(request):
    con = db_connect()
    cur = con.cursor()
    hid = request.COOKIES['user-id']

    query = f"select RequestID,PatientID,OrganName,Request,RequestDate from PatientOrganRequest where HospitalID = '{hid}' and requestID not in (select requestID from PatientOrganRequestApproval )"
    cur.execute(query)
    records = cur.fetchall()
    return render(request, "hospitalOrganRequestApproval.html", {'records': records})


def hospital_show_organ_approval_details(request):
    con = db_connect()
    cur = con.cursor()
    rid = request.POST['rid']
    pid = request.POST['id']

    query = "select patientID,HospitalID,Name,Gender,BloodGroup,DOB,Pin,Place,District,Address,Phone,Email,photo,MedicalReport,RegDate from Patient where patientid = '" + pid + "'"
    cur.execute(query)
    records = cur.fetchall()
    print(query, records)
    return render(request, "hospitalOrganRequestDetail.html", {'records': records, 'RequestID': rid, 'PatientID': pid})


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
    print(cur.fetchall(),"p:", pid)

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
    print(records,pid,query)

    return render(request, "hospitalOrganRequestDetail.html", {'records': records, 'RequestID': rid, 'message': msg, 'disabled': "disabled"})


def hospital_cancel_patient_organ_request(request):
    con = db_connect()
    cur = con.cursor()
    hid = request.COOKIES['user-id']

    query = f"select RequestID,PatientID,OrganName,Request,RequestDate from PatientOrganRequest where HospitalID  = '{hid}' and RequestID in (select RequestID from PatientOrganRequestApproval where status = 'Yes' )"
    cur.execute(query)
    records = cur.fetchall()
    print(records)

    return render(request, "hospitalcancelpatientorganrequest.html", {'records': records})


def validate_hospital_cancel_patient_organ_request(request):
    con = db_connect()
    cur = con.cursor()

    rid = request.POST['rid']
    query = f"update PatientOrganRequestApproval set status = 'No' where RequestID = '{rid}'"
    print(query)
    cur.execute(query)
    con.commit()
    msg = f"successfully canceled the request {rid}"
    query = "select id from UserSession where type = 'H'"
    cur.execute(query)
    records = cur.fetchall()
    hid = request.COOKIES['user-id']

    query = f"select RequestID,PatientID,OrganName,Request,RequestDate from PatientOrganRequest where HospitalID  = '{hid}' and RequestID in (select RequestID from PatientOrganRequestApproval where status = 'Yes' )"
    print(query)
    cur.execute(query)
    records = cur.fetchall()
    print(records)
    return render(request, "hospitalcancelpatientorganrequest.html", {'message': msg, 'records': records})


def hospital_organ_transplantation(request):
    con = db_connect()
    cur = con.cursor()

    hid = request.COOKIES['user-id']

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
            query = f"select * from OrganTransplantation where DonorID = '{did}' and RequestID in ( select RequestID from PatientOrganRequest where organName = '{organName}')"
            print(query)
            cur.execute(query)
            print("row ", cur.rowcount)
            if cur.rowcount == 0:
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
    
    query = f"delete from PatientOrganRequest where requestID = {rid}"
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



def view_users_and_stats(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="H"):
        con = db_connect()
        cur = con.cursor()
        dictCur = con.cursor(pymysql.cursors.DictCursor)

        query = """
            SELECT COUNT(donorid) FROM donor WHERE hospitalID = %s
        """
        cur.execute(query, userId)
        records = cur.fetchall()
        donorCount = records[0][0]
        print(donorCount)

        query = """
            SELECT COUNT(patientid) FROM patient WHERE hospitalID = %s
        """
        cur.execute(query, userId)
        records = cur.fetchall() 
        patientCount = records[0][0]

        query = """
            SELECT CONVERT(date, char) as date, COUNT(BDonationID) as value
            FROM blooddonation
            WHERE hospitalID = %s 
            AND Date >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            GROUP BY DATE(Date) ORDER BY Date DESC;
        """
        dictCur.execute(query, userId)
        records = dictCur.fetchall()
        BloodRecords = json.dumps(records)

        query = """
            SELECT CONVERT(SurgeryDate, char) as date, COUNT(TransplantationID) as value
            FROM organtransplantation 
            WHERE donorID IN ( SELECT donorID FROM Donor WHERE hospitalID = %s ) 
            AND SurgeryDate >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            GROUP BY DATE(SurgeryDate) ORDER BY SurgeryDate DESC;
        """
        dictCur.execute(query, userId)
        records = dictCur.fetchall()
        OrganRecords = json.dumps(records)
        hospitalCount = 0

        return render(request, "hospitalViewUserDetails.html", {'donorCount': donorCount, 'patientCount': patientCount,'BloodRecords': BloodRecords ,'OrganRecords': OrganRecords })
    raise PermissionDenied("403 forbidden")


def donor_list(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="H"):
        con = db_connect()
        cur = con.cursor()
        query = "select * from OrganDonationTypes"
        cur.execute(query)
        records = cur.fetchall()
        return render(request, "hospitalSearchDonors.html", {'organRecords': records})
    raise PermissionDenied("403 forbidden")

    
def validate_donor_list(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="H"):
        con = db_connect()
        cur = con.cursor()

        name = request.POST["name"]
        did = request.POST["did"]
        bloodGroup = request.POST["blood"]
        organName = request.POST["organ"]
        gender = request.POST["gender"]
        donationType = request.POST["type"]

        did = did.upper()
        condition = []
        params = ()

        query = "select * from OrganDonationTypes"
        cur.execute(query)
        organRecords = cur.fetchall()

        base_query = """ 
            SELECT DonorID,photo,Name,Place,District,Phone,Email FROM Donor WHERE hospitalID = %s
        """

        params += (userId,)

        if name is not None and name != '':
            condition.append("MATCH (name)  AGAINST (%s IN NATURAL LANGUAGE MODE)")
            params += (name,)
        if did is not None and did != '':
            condition.append("DonorID = %s")
            params += (did,)
        if bloodGroup is not None and bloodGroup != '':
            condition.append("BloodGroup = %s")
            params += (bloodGroup,)
        if organName is not None and organName != '':
            condition.append("donorID in (select ID from DonorApproval where status = 'Yes') and donorID in ( select ID from DonorOrganStatus where organName = %s and status = 'Y')")
            params += (organName,)
        if gender is not None and gender != '':
            condition.append("Gender = %s")
            params += (gender,)
        if donationType is not None and donationType != '':
            condition.append("TypeOfDonation = %s")
            params += (donationType,)

        if condition:
            query = f"{base_query} AND {' AND '.join(str(c) for c in condition)}"
        else:
            query = base_query

        print(name, query, params)
        cur.execute(query, params)
        records = cur.fetchall()
        return render(request, "hospitalSearchDonors.html", {'records': records,'organRecords': organRecords, 'results': True})
    raise PermissionDenied("403 forbidden")


def view_donor_details(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="H"):
        did = request.POST["id"]
        con = db_connect()
        cur = con.cursor()
        query = """
            SELECT DonorID, HospitalID, Name, Gender, BloodGroup, TypeOfDonation, DOB, Pin, Place, District, Address, Phone, Email, photo, MedicalReport, RegDate
            FROM donor
            WHERE DonorID = %s
        """
        cur.execute(query, (did,))
        records = cur.fetchall()

        query = """
            SELECT Blood.Date, Blood.Time, Blood.UnitOfBlood, Blood.Remarks, Hosp.ID, Hosp.Name, Hosp.Place 
            FROM BloodDonation Blood Join Hospital Hosp 
            WHERE Blood.DonorID = %s
            AND Hosp.Id = Blood.HospitalID order by Blood.Date DESC 
        """
        cur.execute(query, (did,))
        BloodDonationRecords = cur.fetchall()

        query = """
            SELECT OT.TransplantationID, OT.PatientID, OT.SurgeryDate, OT.DonorCondition, OT.OperationStatus, OT.Remarks, PO.OrganName, PO.HospitalID
            FROM organtransplantation OT Join patientorganrequest PO 
            WHERE OT.DonorID = %s
            AND OT.RequestID = PO.RequestID ORDER BY OT.SurgeryDate DESC 
        """
        cur.execute(query, (did,))
        OrganDonationRecords = cur.fetchall()

        return render(request, "adminViewDonorProfile.html", {'records': records, 'BloodDonationRecords': BloodDonationRecords, 'OrganDonationRecords': OrganDonationRecords})
    raise PermissionDenied("403 forbidden")


def patient_list(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="H"):
        con = db_connect()
        cur = con.cursor()
        query = "select * from OrganDonationTypes"
        cur.execute(query)
        records = cur.fetchall()
        return render(request, "hospitalSearchPatients.html", {'organRecords': records})
    raise PermissionDenied("403 forbidden")

    
def validate_patient_list(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="h"):
        con = db_connect()
        cur = con.cursor()

        name = request.POST["name"]
        pid = request.POST["pid"]
        bloodGroup = request.POST["blood"]
        organName = request.POST["organ"]
        gender = request.POST["gender"]

        pid = pid.upper()
        condition = []
        params = ()

        query = "select * from OrganDonationTypes"
        cur.execute(query)
        organRecords = cur.fetchall()

        base_query = """ 
            SELECT patientID,photo,Name,Place,District,Phone,Email FROM patient WHERE hospitalID = %s
        """

        params += (userId,)

        if name is not None and name != '':
            condition.append("MATCH (name)  AGAINST (%s IN NATURAL LANGUAGE MODE)")
            params += (name,)
        if pid is not None and pid != '':
            condition.append("patientID = %s")
            params += (pid,)
        if bloodGroup is not None and bloodGroup != '':
            condition.append("BloodGroup = %s")
            params += (bloodGroup,)
        if organName is not None and organName != '':
            condition.append("patientID IN ( SELECT patientID from patientorganrequest WHERE organName = %s )")
            params += (organName, )
        if gender is not None and gender != '':
            condition.append("Gender = %s")
            params += (gender,)

        if condition:
            query = f"{base_query} AND {' AND '.join(str(c) for c in condition)}"
        else:
            query = base_query

        cur.execute(query, params)
        records = cur.fetchall()
        print(name, query, params)
        return render(request, "hospitalSearchPatients.html", {'records': records,'organRecords': organRecords, 'results': True})
    raise PermissionDenied("403 forbidden")


def view_patient_details(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="H"):
        pid = request.POST["id"]
        con = db_connect()
        cur = con.cursor()
        query = """
            SELECT patientID, HospitalID, Name, Gender, BloodGroup, DOB, Pin, Place, District, Address, Phone, Email, photo, MedicalReport, RegDate
            FROM patient 
            WHERE patientID = %s
        """
        cur.execute(query, (pid,))
        records = cur.fetchall()

        query = """
            SELECT OT.TransplantationID, OT.DonorID, OT.SurgeryDate, OT.PatientCondition, OT.OperationStatus, OT.Remarks, PO.OrganName, PO.HospitalID, HO.Name
            FROM organtransplantation OT JOIN patientorganrequest PO JOIN hospital HO
            WHERE OT.PatientID = %s
            AND HO.ID = PO.HospitalID
            AND OT.RequestID = PO.RequestID ORDER BY OT.SurgeryDate DESC 
        """
        cur.execute(query, (pid,))
        OrganDonationRecords = cur.fetchall()

        query = """
            SELECT PO.RequestID, PO.HospitalID, HO.Name, PO.OrganName, PO.Request, PO.RequestDate
            FROM patientorganrequest PO JOIN hospital HO
            WHERE PatientID = %s
            AND HO.ID = PO.HospitalID
        """
        cur.execute(query, (pid,))
        PendingOrganDonationRecords = cur.fetchall()
        print(query, " :    : ", PendingOrganDonationRecords)

        return render(request, "adminViewPatientProfile.html", {'records': records, 'OrganDonationRecords': OrganDonationRecords, 'PendingOrganDonationRecords': PendingOrganDonationRecords})
    raise PermissionDenied("403 forbidden")
