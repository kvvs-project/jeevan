from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from Jeevan import db_connect, auth_check
from django.contrib import messages
from django.shortcuts import redirect
import os
import time
import pymysql
import json


def admin_view_or_edit_organ_list(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="A"):
        return render(request, "adminViewOrAddOrgans.html")

    raise PermissionDenied("403 forbidden")


def admin_organ_list(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="A"):
        con = db_connect()
        cur = con.cursor()

        query = "select * from OrganDonationTypes"
        cur.execute(query)
        records = cur.fetchall()
        con.close()
        return render(request, "adminOrganList.html", {'records': records})

    raise PermissionDenied("403 forbidden")


def admin_add_new_organ(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="A"):
        return render(request, "adminAddNewOrgan.html")
    
    raise PermissionDenied("403 forbidden")


def admin_validate_add_new_organ(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="A"):
        con = db_connect()
        cur = con.cursor()

        organName = request.POST['name']
        organName = organName.capitalize().replace(" ", "")
        DonationType = request.POST['type']

        query = "select * from OrganDonationTypes where organName = %s"
        cur.execute(query, (organName,))

        if cur.rowcount == 0:
            query = "insert into OrganDonationTypes values( %s , %s )"
            cur.execute(query, (organName, DonationType))
            con.commit()

            msg = "Organ added successfully"

            return render(request, "adminAddNewOrgan.html", {'message': msg})
        msg = "organ already exists"
        return render(request, "adminAddNewOrgan.html", {'message': msg})
    
    raise PermissionDenied("403 forbidden")


def hospital_approval(request):

    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="A"):
        con = db_connect()
        cursor = con.cursor()
        query = "select photoName,id,name,place,regdate from Hospital where id not in(select id from HospitalApproval)"
        cursor.execute(query)
        records = cursor.fetchall()
        return render(request, "adminHospitalApproval.html", {'records': records})

    raise PermissionDenied("403 forbidden")



def show_hospital_details(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="A"):
        con = db_connect()
        cursor = con.cursor()
        hid = request.POST['hid']
        query = "select photoName,id,name,place,Location,pin,phone,District,Email,type,hasbloodbank,proofName,regdate from Hospital where id = %s"
        cursor.execute(query, (hid,))
        records = cursor.fetchall()
        return render(request, "adminHospitalDetails.html", {'records': records, 'hid': hid})
    
    raise PermissionDenied("403 forbidden")  


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
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="A"):
        hid = request.POST['hid']
        approve_status = request.POST['approve_status']
        comment = request.POST['comment']
        date = time.strftime('%Y-%m-%d %H:%M:%S')

        print(hid, approve_status, comment)

        con = db_connect()
        cur = con.cursor()

        query = "insert into HospitalApproval values ( %s , %s , %s , %s)"
        print(query)
        cur.execute(query, (hid, approve_status, comment, date))
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
        return render(request, "adminHospitalDetails.html", {'records': records, 'message': msg, 'disabled': 'disabled'})
    raise PermissionDenied("403 forbidden")


def view_users(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="A"):
        con = db_connect()
        cur = con.cursor()
        dictCur = con.cursor(pymysql.cursors.DictCursor)

        query = """
            SELECT COUNT(ID) FROM hospital 
        """
        cur.execute(query)
        records = cur.fetchall()
        hospitalCount = records[0][0]
        print(hospitalCount)

        query = """
            SELECT COUNT(donorid) FROM donor 
        """
        cur.execute(query)
        records = cur.fetchall()
        donorCount = records[0][0]
        print(donorCount)

        query = """
            SELECT COUNT(patientid) FROM patient 
        """
        cur.execute(query)
        records = cur.fetchall() 
        patientCount = records[0][0]

        query = """
            SELECT CONVERT(date, char) as date, COUNT(BDonationID) as value
            FROM blooddonation
            WHERE Date >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            GROUP BY DATE(Date) ORDER BY Date DESC;
        """
        dictCur.execute(query)
        records = dictCur.fetchall()
        BloodRecords = json.dumps(records)

        query = """
            SELECT CONVERT(SurgeryDate, char) as date, COUNT(TransplantationID) as value
            FROM organtransplantation
            WHERE SurgeryDate >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            GROUP BY DATE(SurgeryDate) ORDER BY SurgeryDate DESC;
        """
        dictCur.execute(query)
        records = dictCur.fetchall()
        OrganRecords = json.dumps(records)

        return render(request, "adminViewUserDetails.html", {'hospitalCount': hospitalCount, 'donorCount': donorCount, 'patientCount': patientCount,'BloodRecords': BloodRecords ,'OrganRecords': OrganRecords })
    raise PermissionDenied("403 forbidden")


def hospital_list(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="A"):
        return render(request, "adminSearchHospitals.html")
    raise PermissionDenied("403 forbidden")
    
    
def validate_hospital_list(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="A"):
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
        return render(request, "adminSearchHospitals.html", {'records': records, 'results': True})
    raise PermissionDenied("403 forbidden")


def view_hospital_details(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="A"):
        hid = request.POST["id"]
        con = db_connect()
        cur = con.cursor()
        query = """
            SELECT photoName,id,name,place,Location,pin,phone,District,Email,type,hasbloodbank,proofName,regdate
            FROM Hospital
            WHERE id = %s
        """
        cur.execute(query, (hid,))
        records = cur.fetchall()
        return render(request, "adminViewHospitalProfile.html", {'records': records})
    raise PermissionDenied("403 forbidden")


def donor_list(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="A"):
        con = db_connect()
        cur = con.cursor()
        query = "select * from OrganDonationTypes"
        cur.execute(query)
        records = cur.fetchall()
        return render(request, "adminSearchDonors.html", {'organRecords': records})
    raise PermissionDenied("403 forbidden")

    
def validate_donor_list(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="A"):
        con = db_connect()
        cur = con.cursor()

        name = request.POST["name"]
        dist = request.POST["dist"]
        did = request.POST["did"]
        hid = request.POST["hid"]
        bloodGroup = request.POST["blood"]
        organName = request.POST["organ"]
        gender = request.POST["gender"]
        donationType = request.POST["type"]

        hid = hid.upper()
        did = did.upper()
        condition = []
        params = ()

        query = "select * from OrganDonationTypes"
        cur.execute(query)
        organRecords = cur.fetchall()

        base_query = """ 
            SELECT DonorID,photo,Name,Place,District,Phone,Email FROM Donor
        """

        if name is not None and name != '':
            condition.append("MATCH (name)  AGAINST (%s IN NATURAL LANGUAGE MODE)")
            params += (name,)
        if dist is not None and dist != '':
            condition.append("District = %s")
            params += (dist,)
        if did is not None and did != '':
            condition.append("DonorID = %s")
            params += (did,)
        if hid is not None and hid != '':
            condition.append("HospitalID = %s")
            params += (hid,)
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
            query = f"{base_query} WHERE {' AND '.join(str(c) for c in condition)}"
        else:
            query = base_query

        cur.execute(query, params)
        records = cur.fetchall()
        print(name, query, params)
        return render(request, "adminSearchDonors.html", {'records': records,'organRecords': organRecords, 'results': True})
    raise PermissionDenied("403 forbidden")


def view_donor_details(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="A"):
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

    if auth_check(userId, token, userType="A"):
        con = db_connect()
        cur = con.cursor()
        query = "select * from OrganDonationTypes"
        cur.execute(query)
        records = cur.fetchall()
        return render(request, "adminSearchPatients.html", {'organRecords': records})
    raise PermissionDenied("403 forbidden")

    
def validate_patient_list(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="A"):
        con = db_connect()
        cur = con.cursor()

        name = request.POST["name"]
        dist = request.POST["dist"]
        pid = request.POST["pid"]
        hid = request.POST["hid"]
        bloodGroup = request.POST["blood"]
        organName = request.POST["organ"]
        gender = request.POST["gender"]

        hid = hid.upper()
        pid = pid.upper()
        condition = []
        params = ()

        query = "select * from OrganDonationTypes"
        cur.execute(query)
        organRecords = cur.fetchall()

        base_query = """ 
            SELECT patientID,photo,Name,Place,District,Phone,Email FROM patient
        """

        if name is not None and name != '':
            condition.append("MATCH (name)  AGAINST (%s IN NATURAL LANGUAGE MODE)")
            params += (name,)
        if dist is not None and dist != '':
            condition.append("District = %s")
            params += (dist,)
        if pid is not None and pid != '':
            condition.append("patientID = %s")
            params += (pid,)
        if hid is not None and hid != '':
            condition.append("HospitalID = %s")
            params += (hid,)
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
            query = f"{base_query} WHERE {' AND '.join(str(c) for c in condition)}"
        else:
            query = base_query

        cur.execute(query, params)
        records = cur.fetchall()
        print(name, query, params)
        return render(request, "adminSearchPatients.html", {'records': records,'organRecords': organRecords, 'results': True})
    raise PermissionDenied("403 forbidden")


def view_patient_details(request):
    token = request.COOKIES.get("user-token", 0)
    userId = request.COOKIES.get("user-id", 0)

    if auth_check(userId, token, userType="A"):
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
