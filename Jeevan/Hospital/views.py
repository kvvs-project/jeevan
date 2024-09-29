import os
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from Jeevan import db_connect
import time


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
