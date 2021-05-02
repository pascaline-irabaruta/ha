from django.shortcuts import render, redirect
from .forms import *
from .models import Department, Doctor, Schedule, Appointment
from django.contrib.auth.decorators import login_required
from .email import send_welcome_email
from .email import send_emergency_email
from django.conf import settings
from django.views.generic.base import TemplateView
from json import dumps
from django.http import HttpResponse

def index(request):
    return render(request, 'patient/index.html')

@login_required(login_url='/accounts/login/')
def all_departments(request):
    departments = Department.objects.all()
    return render(request, 'admin/all-departments.html', context={"departments": departments})

def new_department(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all-departments')
    else:
        form = DepartmentForm()
        return render(request, 'admin/new-department.html',{'form': form})

def update_department(request,pk):
    dep = Department.objects.get(pk = pk)

    if request.method == "POST":
        form = UpdateDepartmentForm(request.POST)
        print(form.errors)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            Department.objects.filter(id = pk).update(name = name, description = description)

            return redirect("all-departments")
    else:
        form = UpdateDepartmentForm()
    return render(request, "admin/update-department.html", context={"form": form, "department":dep})

def department_delete(request,pk):
    department = Department.objects.get(pk=pk)
    department.delete()

    return redirect('all-departments')


# Doctor View Function

def all_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'admin/all-doctors.html', context={"doctors": doctors})

def new_doctor(request):
    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('doctors')
    else:
        form = DoctorForm()
        return render(request, "admin/new-doctor.html", context={"form":form})


def update_doctor(request,pk):
    doc = Doctor.objects.get(pk = pk)

    if request.method == "POST":
        form = UpdateDoctorForm(request.POST)
        print(form.errors)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            details = form.cleaned_data['details']
            Doctor.update_doctor(pk, first_name, last_name, email,phone_number,details)
            return redirect("doctors")
    else:
        form = UpdateDoctorForm()
    return render(request, "admin/update-doctor.html", context={"form": form, "doctor":doc})


def doctor_delete(request,pk):
    doctor = Doctor.objects.get(pk=pk)
    doctor.delete()

    return redirect('doctors')

def search_doc(request):
    if request.method=="GET":
        search_term=request.GET.get("doctor-search")
        searched_doc=Doctor.objects.get(first_name=search_term)
        schedules = Schedule.objects.filter(doctor=searched_doc.id)
        for ap in schedules:
            if ap.status == "taken":
                appointment = []
                appointment.append(Appointment.objects.get(schedules_id=ap.id))
                print(ap.id)
        # appointment = Appointment.objects.filter(schedules = schedules.id)
        return render(request, 'admin/doctor-search.html',context={"searched_doc":searched_doc,"appointment":appointment})
    else:

        return redirect('all-doctors')


def doctor_emergency(request,pk):
    appointments = Appointment.objects.get(pk=pk)
    send_emergency_email(appointments.first_name,appointments.last_name,appointments.schedules,appointments.email)
    searched_doc=Doctor.objects.get(id=appointments.schedules.doctor.id)
    schedules = Schedule.objects.filter(doctor=searched_doc.id)
    for ap in schedules:
        if ap.status == "taken":
            appointment = []
            appointment.append(Appointment.objects.get(schedules_id=ap.id))
            print(ap.id)
        message = "Email to {} {} Was Successfully Sent".format(appointments.first_name,appointments.last_name)
        return render(request, 'admin/doctor-search.html',context={"searched_doc":searched_doc,"appointment":appointment, "message": message})
    else:

        return redirect('all-doctors')


def all_schedules(request):
    schedules = Schedule.objects.all()
    return render(request, 'admin/all-schedules.html', {"schedules": schedules})

def new_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('schedules')
    else:
        form = ScheduleForm()
        return render(request, 'admin/new-schedule.html', {'form': form})

def update_schedule(request, pk):
    schedule = Schedule.objects.get(pk = pk)
    if request.method == 'POST':
        form = UpdateScheduleForm(request.POST)
        print(form.errors)
        if form.is_valid():
            app_date = form.cleaned_data['app_date']
            app_day = form.cleaned_data['app_day']
            app_hour = form.cleaned_data['app_hour']
            Schedule.objects.filter(id = pk).update(app_date = app_date, app_day = app_day, app_hour = app_hour)
            return redirect('schedules')
    else:
        form = UpdateScheduleForm()
        return render(request, 'admin/update-schedule.html', {'form': form, "schedule": schedule})


def schedule_delete(request,pk):
    schedule = Schedule.objects.get(pk=pk)
    schedule.delete()

    return redirect('schedules')


# User View Function


def user_departments(request):
    departments= Department.objects.all()
    return render(request, 'patient/all-departments.html' , context={"departments": departments})

def department_detail(request,id):
    single_department = Department.objects.get(pk= id)
    doctors = Doctor.objects.filter(departments=id)
    return render(request,'patient/department_detail.html',{"single_department":single_department,"doctors":doctors})


def user_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'patient/all-doctors.html', context={"doctors": doctors})


def doctor_detail(request,id):
    single_doctor = Doctor.objects.get(pk= id)
    schedules = Schedule.get_schedule_by_doctor(id)
    return render(request,'patient/doctor_detail.html',{"single_doctor":single_doctor, "schedules":schedules})


def search_doctor(request):
    if request.method=="GET":
        search_term=request.GET.get("searched")
        searched_doct=Doctor.objects.get(first_name=search_term)
        message="{}".format(search_term)
        return render(request, 'patient/doctor-search.html',context={"searched_doct":searched_doct, "message":message})
    else:
        message="You haven't searched for any doctor"
        return render(request, 'patient/doctor-search.html',context={"message":message})


def make_appointment(request,schedule_id):

    if request.method=='POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            schedule = Schedule.objects.get(pk=schedule_id)
            new_appointment = Appointment(first_name = first_name, last_name = last_name, address=address, email = email, phone_number=phone_number, schedules = schedule )
            new_appointment.save()
            Schedule.taken_schedule(schedule_id)
            send_welcome_email(first_name,last_name,schedule,email)
            return render(request, 'patient/appointment-success.html', {"appointment":new_appointment})
    else:
        form = AppointmentForm()
        return render(request, 'patient/appointment.html', {"form":form, "schedule_id":schedule_id})


def all_unchecked_appointments(request):
    appointments= Appointment.all_unchecked_appointment()
    print(appointments)
    return render(request, 'admin/all-appointments.html' , context={"appointments": appointments})

def all_checkedin_appointments(request):
    appointments= Appointment.all_checkedin_appointment()
    return render(request, 'admin/all-checkedin-appointments.html' , context={"appointments": appointments})

def checkin(request,id):
    Appointment.checkedin_appointment(id)
    return redirect('checkedin')


class HomePageView(TemplateView):
    template_name = 'patient/index.html'
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['key'] = settings.RAVE_PUBLIC_KEY
    return context
