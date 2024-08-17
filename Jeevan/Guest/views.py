from django.shortcuts import render
from Jeevan import db_connect


def find_donors(request):
    return render(request, "find.html")


def guest_find_organ_donor(request):
    con = db_connect()
    cur = con.cursor()
    query = "select * from OrganDonationTypes"
    cur.execute(query)
    records = cur.fetchall()
    return render(request, "guestsearchorgandonor.html", {'organRecords': records})


def guest_get_organ_hospital_list(request):
    con = db_connect()
    cur = con.cursor()

    district = request.POST['dist']
    organ = request.POST['organ']
    bloodGroup = request.POST['blood']
    gender = request.POST['gender']

    query = f"select PhotoName,Name,Place,District,Phone,Email,Location,Pin from Hospital where ID in ( select HospitalID from Donor where District = '{district}' and Gender = '{gender}' and BloodGroup = '{bloodGroup}' and donorID in (select ID from DonorApproval where status = 'Yes') and donorID in ( select ID from DonorOrganStatus where organName = '{organ}' and status = 'Y') )"
    print(query)
    cur.execute(query)
    records = cur.fetchall()
    print(records)

    query = "select * from OrganDonationTypes"
    cur.execute(query)
    organRecords = cur.fetchall()
    return render(request, "guestsearchorgandonor.html",
                  {'organRecords': organRecords, 'records': records, 'results': True})


def guest_find_blood_donor(request):
    return render(request, "guestsearchblooddonor.html")


def guest_get_blood_donor_list(request):
    con = db_connect()
    cur = con.cursor()

    district = request.POST['dist']
    bloodGroup = request.POST['blood']
    gender = request.POST['gender']

    query = f"select PhotoName,Name,Place,District,Phone,Email,Location,Pin from Hospital where ID in ( select HospitalID from Donor where District = '{district}' and Gender = '{gender}' and BloodGroup = '{bloodGroup}' and donorID in (select ID from DonorApproval where status = 'Yes') )"

    print(query)
    cur.execute(query)
    records = cur.fetchall()
    print(records)
    return render(request, "guestsearchblooddonor.html", {'records': records, 'results': True})

