from django.contrib.auth import authenticate, login
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from django.conf import settings
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .filters import PatientFilter

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/index.html")


# for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/adminclick.html")


def updateFiche(request):
    print("here we go ")
    ficheId = request.GET.get("ficheId")
    poids = request.GET.get("poids")
    fiche = models.Fiche.objects.get(id=ficheId)
    fiche.poids = poids
    fiche.save()
    context = {
        "ficheId": fiche.id,
        "first_name": fiche.first_name,
        "last_name": fiche.last_name,
        "date": fiche.date,
        "poids": fiche.poids,
    }
    print("hhhhhhh", context)
    return render(request, "hospital/form.html", context=context)


def infirmier_list(request):
    patientId = request.GET.get("id", "")
    fiche = models.Fiche.objects.get(patientId=patientId)
    context = {
        "ficheId": fiche.id,
        "first_name": fiche.first_name,
        "last_name": fiche.last_name,
        "date": fiche.date,
        "poids": fiche.poids,
    }
    print(context)
    return render(request, "hospital/form.html", context=context)


# for showing signup/login button for doctor(by sumit)
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/doctorclick.html")


# for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/patientclick.html")


def receptionisteclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/receptionisteclick.html")


def admin_signup_view(request):
    form = forms.AdminSigupForm()
    if request.method == "POST":
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name="ADMIN")
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect("adminlogin")
    return render(request, "hospital/adminsignup.html", {"form": form})


def doctor_signup_view(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {"userForm": userForm, "doctorForm": doctorForm}
    if request.method == "POST":
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor = doctor.save()
            my_doctor_group = Group.objects.get_or_create(name="DOCTOR")
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect("doctorlogin")
    return render(request, "hospital/doctorsignup.html", context=mydict)


def infirmier_signup_view(request):
    userForm = forms.InfirmierUserForm()
    infirmierForm = forms.InfirmierForm()
    mydict = {"userForm": userForm, "infirmierForm": infirmierForm}
    if request.method == "POST":
        userForm = forms.InfirmierUserForm(request.POST)
        infirmierForm = forms.InfirmierForm(request.POST, request.FILES)
        if userForm.is_valid() and infirmierForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            infirmier = infirmierForm.save(commit=False)
            infirmier.user = user
            infirmier = infirmier.save()
            my_infirmier_group = Group.objects.get_or_create(name="INFIRMIER")
            my_infirmier_group[0].user_set.add(user)
        return HttpResponseRedirect("infirmierlogin")
    return render(request, "hospital/infirmiersignup.html", context=mydict)


def patient_signup_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient = patient.save()
            my_patient_group = Group.objects.get_or_create(name="PATIENT")
            my_patient_group[0].user_set.add(user)
            print("status", type(patient))
        return HttpResponseRedirect("patientlogin")
    return render(request, "hospital/patientsignup.html", context=mydict)


def doctor_signup_view(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {"userForm": userForm, "doctorForm": doctorForm}
    if request.method == "POST":
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor = doctor.save()
            my_doctor_group = Group.objects.get_or_create(name="DOCTOR")
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect("doctorlogin")
    return render(request, "hospital/doctorsignup.html", context=mydict)


def receptioniste_signup_view(request):

    userForm = forms.ReceptionisteUserForm()
    receptionisteForm = forms.ReceptionisteForm()
    mydict = {"userForm": userForm, "doctorForm": receptionisteForm}
    if request.method == "POST":
        userForm = forms.ReceptionisteUserForm(request.POST)
        receptionisteForm = forms.ReceptionisteForm(request.POST, request.FILES)
        if receptionisteForm.is_valid():
            print(
                "new receptioniste created",
                userForm.is_valid(),
                receptionisteForm.is_valid(),
            )
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            receptioniste = receptionisteForm.save(commit=False)
            receptioniste.user = user
            receptioniste = receptioniste.save()
            my_receptioniste_group = Group.objects.get_or_create(name="RECEPTIONISTE")
            my_receptioniste_group[0].user_set.add(user)
            print("new receptioniste created")
        return HttpResponseRedirect("receptionistelogin")
    return render(request, "hospital/receptionistesignup.html", context=mydict)


# -----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name="ADMIN").exists()


def is_doctor(user):
    return user.groups.filter(name="DOCTOR").exists()


def is_patient(user):
    return user.groups.filter(name="PATIENT").exists()


def is_infirmier(user):
    return user.groups.filter(name="INFIRMIER").exists()


def is_receptioniste(user):
    return user.groups.filter(name="RECEPTIONISTE").exists()


# ---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):

    if is_admin(request.user):
        return redirect("admin-dashboard")
    elif is_doctor(request.user):
        accountapproval = models.Doctor.objects.all().filter(
            user_id=request.user.id, status=True
        )
        if accountapproval:
            return redirect("doctor-dashboard")
        else:
            return render(request, "hospital/doctor_wait_for_approval.html")
    elif is_infirmier(request.user):
        accountapproval = models.Infirmier.objects.all().filter(
            user_id=request.user.id, status=True
        )
        if accountapproval:
            return redirect("infirmier-dashboard")
        else:
            return render(request, "hospital/doctor_wait_for_approval.html")

    elif is_patient(request.user):
        accountapproval = models.Patient.objects.all().filter(
            user_id=request.user.id, status=True
        )
        if accountapproval:
            return redirect("patient-dashboard")
        else:
            return render(request, "hospital/patient_wait_for_approval.html")
    elif is_receptioniste(request.user):
        accountapproval = models.Receptioniste.objects.all().filter(
            user_id=request.user.id, status=True
        )

        if accountapproval:

            return redirect("receptioniste-dashboard")
        else:
            return render(request, "hospital/doctor_wait_for_approval.html")


# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    # for both table in admin dashboard
    doctors = models.Doctor.objects.all().order_by("-id")
    patients = models.Patient.objects.all().order_by("-id")
    # for three cards
    doctorcount = models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount = models.Doctor.objects.all().filter(status=False).count()
    infirmiers = models.Infirmier.objects.all().order_by("-id")
    infirmiercount = models.Infirmier.objects.all().filter(status=True).count()
    receptionistes = models.Receptioniste.objects.all().order_by("-id")
    receptionistescount = len(models.Receptioniste.objects.all())
    pendinginfirmiercount = models.Infirmier.objects.all().filter(status=False).count()
    appointmentcount = models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount = (
        models.Appointment.objects.all().filter(status=False).count()
    )
    mydict = {
        "doctors": doctors,
        "patients": patients,
        "infirmiers": infirmiers,
        "receptionistes": receptionistes,
        "receptionistescount": receptionistescount,
        "doctorcount": doctorcount,
        "pendingdoctorcount": pendingdoctorcount,
        "pendinginfirmiercount": pendinginfirmiercount,
        "appointmentcount": appointmentcount,
        "pendingappointmentcount": pendingappointmentcount,
        "infirmiercount": infirmiercount,
    }
    return render(request, "hospital/admin_dashboard.html", context=mydict)


# this view for sidebar click on admin page
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request, "hospital/admin_doctor.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(request, "hospital/admin_view_doctor.html", {"doctors": doctors})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect("admin-view-doctor")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def update_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)

    userForm = forms.DoctorUserForm(instance=user)
    doctorForm = forms.DoctorForm(request.FILES, instance=doctor)
    mydict = {"userForm": userForm, "doctorForm": doctorForm}
    if request.method == "POST":
        userForm = forms.DoctorUserForm(request.POST, instance=user)
        doctorForm = forms.DoctorForm(request.POST, request.FILES, instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.status = True
            doctor.save()
            return redirect("admin-view-doctor")
    return render(request, "hospital/admin_update_doctor.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {"userForm": userForm, "doctorForm": doctorForm}
    if request.method == "POST":
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.status = True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name="DOCTOR")
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect("admin-view-doctor")
    return render(request, "hospital/admin_add_doctor.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    # those whose approval are needed
    doctors = models.Doctor.objects.all().filter(status=False)
    return render(request, "hospital/admin_approve_doctor.html", {"doctors": doctors})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def approve_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    doctor.status = True
    doctor.save()
    return redirect(reverse("admin-approve-doctor"))


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def reject_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect("admin-approve-doctor")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(
        request, "hospital/admin_view_doctor_specialisation.html", {"doctors": doctors}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request, "hospital/admin_patient.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approuver_infirmier_view(request):
    # those whose approval are needed
    infirmiers = models.Infirmier.objects.all().filter(status=False)
    return render(
        request, "hospital/admin_approuver_infirmier.html", {"infirmiers": infirmiers}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_infirmier_view(request):
    infirmiers = models.Infirmier.objects.all().filter(status=True)
    return render(
        request, "hospital/admin_view_infirmier.html", {"infirmiers": infirmiers}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_infirmier_view(request):
    return render(request, "hospital/admin_infirmier.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, "hospital/admin_view_patient.html", {"patients": patients})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect("admin-view-patient")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def update_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)

    userForm = forms.PatientUserForm(instance=user)
    patientForm = forms.PatientForm(request.FILES, instance=patient)
    mydict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST, instance=user)
        patientForm = forms.PatientForm(request.POST, request.FILES, instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.status = True
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient.save()
            return redirect("admin-view-patient")
    return render(request, "hospital/admin_update_patient.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            patient = patientForm.save(commit=False)
            patient.user = user
            patient.status = True
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient.save()

            my_patient_group = Group.objects.get_or_create(name="PATIENT")
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect("admin-view-patient")
    return render(request, "hospital/admin_add_patient.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def supprimer_infirmier_view(request, pk):
    infirmier = models.Infirmier.objects.get(id=pk)
    user = models.User.objects.get(id=infirmier.user_id)
    user.delete()
    infirmier.delete()
    return redirect("admin-view-infirmier")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def modifier_infirmier_view(request, pk):
    infirmier = models.Infirmier.objects.get(id=pk)
    user = models.User.objects.get(id=infirmier.user_id)

    userForm = forms.InfirmierUserForm(instance=user)
    infirmierForm = forms.InfirmierForm(request.FILES, instance=infirmier)
    mydict = {"userForm": userForm, "infirmierForm": infirmierForm}
    if request.method == "POST":
        userForm = forms.InfirmierUserForm(request.POST, instance=user)
        infirmierForm = forms.InfirmierForm(
            request.POST, request.FILES, instance=infirmier
        )
        if userForm.is_valid() and infirmierForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            infirmier = infirmierForm.save(commit=False)
            infirmier.status = True
            infirmier.save()
            return redirect("admin-view-infirmier")
    return render(request, "hospital/admin_update_patient.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_ajouter_infirmier_view(request):
    userForm = forms.InfirmierUserForm()
    infirmierForm = forms.InfirmierForm()
    mydict = {"userForm": userForm, "infirmierForm": infirmierForm}
    if request.method == "POST":
        userForm = forms.InfirmierUserForm(request.POST)
        infirmierForm = forms.InfirmierForm(request.POST, request.FILES)
        if userForm.is_valid() and infirmierForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            infirmier = infirmierForm.save(commit=False)
            infirmier.user = user
            infirmier.status = True
            infirmier.save()

            my_infirmier_group = Group.objects.get_or_create(name="INFIRMIER")
            my_infirmier_group[0].user_set.add(user)

        return HttpResponseRedirect("admin-view-infirmier")
    print(infirmierForm)
    return render(request, "hospital/admin_ajouter_infirmier.html", context=mydict)


# ------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    # those whose approval are needed
    patients = models.Patient.objects.all().filter(status=False)
    return render(
        request, "hospital/admin_approve_patient.html", {"patients": patients}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def approve_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    patient.status = True
    patient.save()
    return redirect(reverse("admin-approve-patient"))


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def reject_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect("admin-approve-patient")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def approuver_infirmier_view(request, pk):
    infirmier = models.Infirmier.objects.get(id=pk)
    infirmier.status = True
    infirmier.save()
    return redirect(reverse("admin-approuver-infirmier"))


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def decliner_infirmier_view(request, pk):
    infirmier = models.Infirmier.objects.get(id=pk)
    user = models.User.objects.get(id=infirmier.user_id)
    user.delete()
    infirmier.delete()
    return redirect("admin-approuver-infirmier")


# --------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(
        request, "hospital/admin_discharge_patient.html", {"patients": patients}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def discharge_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    days = date.today() - patient.admitDate  # 2 days, 0:00:00
    assignedDoctor = models.User.objects.all().filter(id=patient.assignedDoctorId)
    d = days.days  # only how many day that is 2
    patientDict = {
        "patientId": pk,
        "name": patient.get_name,
        "mobile": patient.mobile,
        "address": patient.address,
        "symptoms": patient.symptoms,
        "admitDate": patient.admitDate,
        "todayDate": date.today(),
        "day": d,
        "assignedDoctorName": assignedDoctor[0].first_name,
    }
    if request.method == "POST":
        feeDict = {
            "roomCharge": int(request.POST["roomCharge"]) * int(d),
            "doctorFee": request.POST["doctorFee"],
            "medicineCost": request.POST["medicineCost"],
            "OtherCharge": request.POST["OtherCharge"],
            "total": (int(request.POST["roomCharge"]) * int(d))
            + int(request.POST["doctorFee"])
            + int(request.POST["medicineCost"])
            + int(request.POST["OtherCharge"]),
        }
        patientDict.update(feeDict)
        # for updating to database patientDischargeDetails (pDD)
        pDD = models.PatientDischargeDetails()
        pDD.patientId = pk
        pDD.patientName = patient.get_name
        pDD.assignedDoctorName = assignedDoctor[0].first_name
        pDD.address = patient.address
        pDD.mobile = patient.mobile
        pDD.symptoms = patient.symptoms
        pDD.admitDate = patient.admitDate
        pDD.releaseDate = date.today()
        pDD.daySpent = int(d)
        pDD.medicineCost = int(request.POST["medicineCost"])
        pDD.roomCharge = int(request.POST["roomCharge"]) * int(d)
        pDD.doctorFee = int(request.POST["doctorFee"])
        pDD.OtherCharge = int(request.POST["OtherCharge"])
        pDD.total = (
            (int(request.POST["roomCharge"]) * int(d))
            + int(request.POST["doctorFee"])
            + int(request.POST["medicineCost"])
            + int(request.POST["OtherCharge"])
        )
        pDD.save()
        return render(request, "hospital/patient_final_bill.html", context=patientDict)
    return render(request, "hospital/patient_generate_bill.html", context=patientDict)


# --------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return


def download_pdf_view(request, pk):
    dischargeDetails = (
        models.PatientDischargeDetails.objects.all()
        .filter(patientId=pk)
        .order_by("-id")[:1]
    )
    dict = {
        "patientName": dischargeDetails[0].patientName,
        "assignedDoctorName": dischargeDetails[0].assignedDoctorName,
        "address": dischargeDetails[0].address,
        "mobile": dischargeDetails[0].mobile,
        "symptoms": dischargeDetails[0].symptoms,
        "admitDate": dischargeDetails[0].admitDate,
        "releaseDate": dischargeDetails[0].releaseDate,
        "daySpent": dischargeDetails[0].daySpent,
        "medicineCost": dischargeDetails[0].medicineCost,
        "roomCharge": dischargeDetails[0].roomCharge,
        "doctorFee": dischargeDetails[0].doctorFee,
        "OtherCharge": dischargeDetails[0].OtherCharge,
        "total": dischargeDetails[0].total,
    }
    return render_to_pdf("hospital/download_bill.html", dict)


# -----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request, "hospital/admin_appointment.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments = models.Appointment.objects.all().filter(status=True)
    return render(
        request, "hospital/admin_view_appointment.html", {"appointments": appointments}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm = forms.AppointmentForm()
    mydict = {
        "appointmentForm": appointmentForm,
    }
    if request.method == "POST":
        appointmentForm = forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get("doctorId")
            appointment.patientId = request.POST.get("patientId")
            appointment.doctorName = models.User.objects.get(
                id=request.POST.get("doctorId")
            ).first_name
            appointment.patientName = models.User.objects.get(
                id=request.POST.get("patientId")
            ).first_name
            appointment.status = True
            appointment.save()
        return HttpResponseRedirect("admin-view-appointment")
    return render(request, "hospital/admin_add_appointment.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    # those whose approval are needed
    appointments = models.Appointment.objects.all().filter(status=False)
    return render(
        request,
        "hospital/admin_approve_appointment.html",
        {"appointments": appointments},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def approve_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.status = True
    appointment.save()
    return redirect(reverse("admin-approve-appointment"))


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def reject_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect("admin-approve-appointment")


# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------
#### Accueil####
def accueil(request):
    patientAffected = len(models.Patient.objects.filter(isAffected=True))
    patientNonAffected = len(models.Patient.objects.filter(isAffected=False))
    patientAll = patientAffected + patientNonAffected
    doctorsAll = len(models.Doctor.objects.all())
    doctors = models.Doctor.objects.filter(presence=True)
    doctorsPresent = len(doctors)
    infirmiersALL = len(models.Infirmier.objects.all())
    receptionistesALL = len(models.Receptioniste.objects.all())
    context = {
        "patientAll": patientAll,
        "patientAffected": patientAffected,
        "patientNonAffected": patientNonAffected,
        "doctorsAll": doctorsAll,
        "doctorsPresent": doctorsPresent,
        "infirmiersALL": infirmiersALL,
        "receptionistesALL": receptionistesALL,
        "doctors": doctors,
    }
    print(context)
    return render(request, "hospital/accueil.html", context=context)


# ---------------------------------
# ---------------- Receptioniste
# ---------------------------------
@login_required(login_url="receptionistelogin")
@user_passes_test(is_receptioniste)
def receptioniste_dashboard_view(request):
    patientAffected = len(models.Patient.objects.filter(isAffected=True))
    patientNonAffected = len(models.Patient.objects.filter(isAffected=False))
    patientAll = patientAffected + patientNonAffected
    doctorsAll = len(models.Doctor.objects.all())
    doctors = models.Doctor.objects.filter(presence=True)
    doctorsPresent = len(doctors)
    infirmiers = len(models.Doctor.objects.all())
    receptionistes = len(models.Receptioniste.objects.all())
    context = {
        "patientAll": patientAll,
        "patientAffected": patientAffected,
        "patientNonAffected": patientNonAffected,
        "doctorsAll": doctorsAll,
        "doctorsPresent": doctorsPresent,
        "infirmiers": infirmiers,
        "receptionistes": receptionistes,
        "doctors": doctors,
    }
    print(context)
    return render(request, "hospital/receptioniste_dashboard.html", context=context)


def receptioniste_stats(request):
    return render(request, "hospital/receptioniste_dashboard.html")


# @login_required(login_url="receptionistelogin")
# @user_passes_test(is_receptioniste)
def registerpatient(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():

            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient.save()
            print("hi", patient.id)
            fiche = models.Fiche(
                patientId=patient.id,
                first_name=user.first_name,
                last_name=user.last_name,
            )
            fiche = fiche.save()
            my_patient_group = Group.objects.get_or_create(name="PATIENT")
            my_patient_group[0].user_set.add(user)
        return redirect("/receptioniste-dashboard")
    return render(request, "hospital/patientsignup.html", context=mydict)


# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    # for three cards
    patientcount = (
        models.Patient.objects.all()
        .filter(status=True, assignedDoctorId=request.user.id)
        .count()
    )
    appointmentcount = (
        models.Appointment.objects.all()
        .filter(status=True, doctorId=request.user.id)
        .count()
    )
    patientdischarged = (
        models.PatientDischargeDetails.objects.all()
        .distinct()
        .filter(assignedDoctorName=request.user.first_name)
        .count()
    )

    # for  table in doctor dashboard
    appointments = (
        models.Appointment.objects.all()
        .filter(status=True, doctorId=request.user.id)
        .order_by("-id")
    )
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = (
        models.Patient.objects.all()
        .filter(status=True, user_id__in=patientid)
        .order_by("-id")
    )
    appointments = zip(appointments, patients)
    mydict = {
        "patientcount": patientcount,
        "appointmentcount": appointmentcount,
        "patientdischarged": patientdischarged,
        "appointments": appointments,
        "doctor": models.Doctor.objects.get(user_id=request.user.id),
        "service": models.Doctor.objects.get(user_id=request.user.id).presence,
        "id": request.user.id
        # for profile picture of doctor in sidebar
    }
    return render(request, "hospital/doctor_dashboard.html", context=mydict)


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict = {
        "doctor": models.Doctor.objects.get(user_id=request.user.id),
        "doctor": models.Doctor.objects.get(user_id=request.user.id),
        "service": models.Doctor.objects.get(user_id=request.user.id).presence,
        "id": request.user.id,  # for profile picture of doctor in sidebar
    }
    return render(request, "hospital/doctor_patient.html", context=mydict)


@login_required(login_url="infirmierlogin")
@user_passes_test(is_infirmier)
def infirmier_dashboard_view(request):
    patients = models.Patient.objects.all().order_by("-id")
    patientComplet = []
    for patient in patients:
        if patient.isAffected == True:
            patientComplet.append(
                [
                    patient,
                    models.Doctor.objects.get(user_id=patient.assignedDoctorId),
                    models.Bed.objects.get(patientId=patient.id),
                ]
            )

    myFilter = PatientFilter(request.GET, queryset=patients)
    patients = myFilter.qs

    # patientcomplet=[[patient,models.Doctor.objects.get(user_id=3)] for patient in patients]

    mydict = {
        "infirmier": models.Infirmier.objects.get(user_id=request.user.id),
        "patientComplet": patientComplet,
        #'patientcomplet':patientcomplet,
        "patients": patients,
        "myFilter": myFilter,
    }

    return render(request, "hospital/infirmier_dashboard.html", context=mydict)


def show_bloc_occupation(request):
    return render(request, "hospital/show_bloc_occupation.html")


@csrf_exempt
def affectation(request):
    print("before", len(models.Bed.objects.filter(status="free")))
    patientId = request.POST.get("patientId")
    bedId = request.POST.get("bedId")
    print("hi", patientId, bedId)
    patient = models.Patient.objects.get(id=int(patientId))
    bed = models.Bed.objects.get(id=int(bedId))
    patient.isAffected = True
    bed.patientId = patientId
    bed.status = "occupied"
    patient.save()
    bed.save()
    print("after", len(models.Bed.objects.filter(status="free")))
    return JsonResponse({})


@csrf_exempt
def blockComponents(request):
    blocks = list(models.Block.objects.all())
    blockNames = [block.blockName for block in blocks]
    response = request.POST.get("roomId")

    if response != "":
        print("h")
        print(response)
        room = models.Room.objects.get(id=int(response))
        beds = models.Bed.objects.filter(room=room, status="free")
        beds = [[bed.id, "Lit" + str(bed.id)] for bed in beds]
        print("beds ", beds)
        blockComponents = {
            "beds": beds,
            "selectroomId": request.POST.get("selectroomId"),
        }
        return JsonResponse(blockComponents)
    return JsonResponse({"beds": [], "selectroomId": request.POST.get("selectroomId")})


@csrf_exempt
def bloc_occupation(request):
    # departments = [
    #    ("Cardiologie", "Cardiologie"),
    #    ("Dermatologie", "Dermatologie"),
    #    ("Médecine d'urgence", "Médecine d'urgence"),
    #    ("Allergologie/Immunologie", "Allergologie/Immunologie"),
    #    ("Anesthésiologistes", "Anesthésiologistes"),
    #    ("Chirurgie du côlon et du rectum", "Chirurgie du côlon et du rectum"),
    # ]
    # for department, ignored in departments:
    #    block = models.Block(blockName=department)
    #    block.save()
    #    for i in range(1, 7):
    #        room = models.Room(block=block, number=i)
    #        room.save()
    #        for j in range(1, 4):
    #            bed = models.Bed(room=room, number=j)
    #            bed.save()
    #    print("new block is full")
    # print("done")
    response = request.POST.get("blockName")
    blockRequested = models.Block.objects.get(blockName=response)
    rooms = models.Room.objects.filter(block=blockRequested)

    beds = []
    for room in list(rooms):
        beds = beds + list(models.Bed.objects.filter(room=room))

    rooms = [[room.id, "room" + str(room.number)] for room in rooms]
    requestedBeds = []
    for bed in beds:
        try:
            patient = models.Patient.objects.get(id=bed.patientId)
            requestedBeds.append(
                [
                    bed.id,
                    bed.room.id,
                    bed.status,
                    patient.get_name,
                    patient.cin,
                    patient.id,
                ]
            )

        except:
            requestedBeds.append(
                [
                    bed.id,
                    bed.room.id,
                    bed.status,
                    "Aucun Patient",
                    "Pas encore renseignée",
                    "None",
                ]
            )
    beds = requestedBeds
    blocks = list(models.Block.objects.all())
    blockNames = [block.blockName for block in blocks]
    print(beds)
    blockData = {
        "blockNames": blockNames,
        "rooms": rooms,
        "beds": beds,
    }
    return JsonResponse(blockData)


@csrf_exempt
def updateservice(request):
    response = request.POST.get("service")
    id = int(request.POST.get("id"))
    doctor = models.Doctor.objects.get(user_id=id)
    doctor.date = request.POST.get("date")
    doctor.horaire = request.POST.get("horaire")
    if response == "true":
        doctor.presence = True
    else:
        doctor.presence = False
    doctor.save()
    print("operation is success")
    return JsonResponse({})


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients = models.Patient.objects.all().filter(
        status=True, assignedDoctorId=request.user.id, isAffected=True
    )
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    print(len(patients))
    return render(
        request,
        "hospital/doctor_view_patient.html",
        {"patients": patients, "doctor": doctor},
    )


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def search_view(request):
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET["query"]
    patients = (
        models.Patient.objects.all()
        .filter(status=True, assignedDoctorId=request.user.id)
        .filter(Q(symptoms__icontains=query) | Q(user__first_name__icontains=query))
    )
    return render(
        request,
        "hospital/doctor_view_patient.html",
        {"patients": patients, "doctor": doctor},
    )


@login_required(login_url="infirmierlogin")
@user_passes_test(is_infirmier)
def search1_view(request):
    infirmiers = models.Infirmier.objects.get(user_id=request.user.id)
    query = request.GET["query"]
    patients = models.Patient.objects.all().filter(
        Q(cin__icontains=query)
        | Q(user__first_name__icontains=query)
        | Q(user__last_name__icontains=query)
    )

    patientComplet = [
        [patient, models.Doctor.objects.get(user_id=patient.assignedDoctorId)]
        for patient in patients
    ]
    return render(
        request,
        "hospital/infirmier_dashboard.html",
        {"infirmiers": infirmiers, "patientComplet": patientComplet},
    )


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    patients = models.Patient.objects.all().filter(
        status=True, assignedDoctorId=request.user.id, isAffected=False
    )
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    blockRequested = models.Block.objects.get(blockName=doctor.department)
    rooms = models.Room.objects.filter(block=blockRequested)
    rooms = [["room " + str(room.number), room.id] for room in rooms]
    blocks = list(models.Block.objects.all())
    blockNames = [block.blockName for block in blocks]
    print(rooms)
    return render(
        request,
        "hospital/doctor_view_discharge_patient.html",
        {
            "dischargedpatients": patients,
            "doctor": doctor,
            "blocks": blockNames,
            "rooms": rooms,
        },
    )


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    return render(request, "hospital/doctor_appointment.html", {"doctor": doctor})


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id
    )
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(
        request,
        "hospital/doctor_view_appointment.html",
        {"appointments": appointments, "doctor": doctor},
    )


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id
    )
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(
        request,
        "hospital/doctor_delete_appointment.html",
        {"appointments": appointments, "doctor": doctor},
    )


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def delete_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id
    )
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(
        request,
        "hospital/doctor_delete_appointment.html",
        {"appointments": appointments, "doctor": doctor},
    )


# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------------------ PATIENT RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    doctor = models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict = {
        "patient": patient,
        "doctorName": doctor.get_name,
        "doctorMobile": doctor.mobile,
        "doctorAddress": doctor.address,
        "symptoms": patient.symptoms,
        "doctorDepartment": doctor.department,
        "admitDate": patient.admitDate,
    }
    return render(request, "hospital/patient_dashboard.html", context=mydict)


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    return render(request, "hospital/patient_appointment.html", {"patient": patient})


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm = forms.PatientAppointmentForm()
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    message = None
    mydict = {
        "appointmentForm": appointmentForm,
        "patient": patient,
        "message": message,
    }
    if request.method == "POST":
        appointmentForm = forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get("doctorId"))
            desc = request.POST.get("description")

            doctor = models.Doctor.objects.get(user_id=request.POST.get("doctorId"))

            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get("doctorId")
            appointment.patientId = (
                request.user.id
            )  # ----user can choose any patient but only their info will be stored
            appointment.doctorName = models.User.objects.get(
                id=request.POST.get("doctorId")
            ).first_name
            appointment.patientName = (
                request.user.first_name
            )  # ----user can choose any patient but only their info will be stored
            appointment.status = False
            appointment.save()
        return HttpResponseRedirect("patient-view-appointment")
    return render(request, "hospital/patient_book_appointment.html", context=mydict)


def patient_view_doctor_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    return render(
        request,
        "hospital/patient_view_doctor.html",
        {"patient": patient, "doctors": doctors},
    )


def search_doctor_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar

    # whatever user write in search box we get in query
    query = request.GET["query"]
    doctors = (
        models.Doctor.objects.all()
        .filter(status=True)
        .filter(Q(department__icontains=query) | Q(user__first_name__icontains=query))
    )
    return render(
        request,
        "hospital/patient_view_doctor.html",
        {"patient": patient, "doctors": doctors},
    )


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    appointments = models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(
        request,
        "hospital/patient_view_appointment.html",
        {"appointments": appointments, "patient": patient},
    )


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    dischargeDetails = (
        models.PatientDischargeDetails.objects.all()
        .filter(patientId=patient.id)
        .order_by("-id")[:1]
    )
    patientDict = None
    if dischargeDetails:
        patientDict = {
            "is_discharged": True,
            "patient": patient,
            "patientId": patient.id,
            "patientName": patient.get_name,
            "assignedDoctorName": dischargeDetails[0].assignedDoctorName,
            "address": patient.address,
            "mobile": patient.mobile,
            "symptoms": patient.symptoms,
            "admitDate": patient.admitDate,
            "releaseDate": dischargeDetails[0].releaseDate,
            "daySpent": dischargeDetails[0].daySpent,
            "medicineCost": dischargeDetails[0].medicineCost,
            "roomCharge": dischargeDetails[0].roomCharge,
            "doctorFee": dischargeDetails[0].doctorFee,
            "OtherCharge": dischargeDetails[0].OtherCharge,
            "total": dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict = {
            "is_discharged": False,
            "patient": patient,
            "patientId": request.user.id,
        }
    return render(request, "hospital/patient_discharge.html", context=patientDict)


# ------------------------ PATIENT RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request, "hospital/aboutus.html")


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == "POST":
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data["Email"]
            name = sub.cleaned_data["Name"]
            message = sub.cleaned_data["Message"]
            send_mail(
                str(name) + " || " + str(email),
                message,
                settings.EMAIL_HOST_USER,
                settings.EMAIL_RECEIVING_USER,
                fail_silently=False,
            )
            return render(request, "hospital/contactussuccess.html")
    return render(request, "hospital/contactus.html", {"form": sub})


# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# Developed By : sumit kumar
# facebook : fb.com/sumit.luv
# Youtube :youtube.com/lazycoders
