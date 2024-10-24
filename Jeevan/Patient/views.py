from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from Jeevan import db_connect
from Main.views import thanks
import time


def patient_pre_reg(request):
    return render(request, "patientPreSignUp.html")


def patient_find_hospital(request):
    con = db_connect()
    cur = con.cursor()
    name = request.POST["search"]
    dist = request.POST["dist"]

    condition = []
    params = ()

    base_query = """ 
        SELECT ID,PhotoName,Name,Place,District,Phone,Email FROM hospital
    """
    if name is not None and name != '':
        condition.append("MATCH (name)  AGAINST (%s IN NATURAL LANGUAGE MODE)")
        params += (name,)
    if dist is not None and dist != '':
        condition.append("District = %s")
        params += (dist,)

    if condition:
        query = f"{base_query} WHERE {' AND '.join(str(c) for c in condition)}"
    else:
        query = base_query

    cur.execute(query, params)
    records = cur.fetchall()
    print(name, query, params)
    return render(request, "patientPreSignUp.html", {'records': records, 'results': True})


def patient_reg(request):
    con = db_connect()
    cur = con.cursor()
    hid = request.POST["id"]
    return render(request, "patientSignUp.html", {'hid': hid})


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
    query = "select * from Patient order by patientID desc limit 1"
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

    return thanks(request, userId=pid)


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
