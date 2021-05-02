from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Hospital(models.Model):
    name = models.CharField(max_length=20)

class Department(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=600)
    department_image = models.ImageField(upload_to='departments/',blank=True)
    # hospitals = models.ForeignKey(Hospital,on_delete=models.CASCADE)

    def save_department(self):
        self.save()

    def delete_department(self):
        self.delete()

    def __str__(self):
        return self.name

    @classmethod
    def search_departments(cls, search_term):
        return cls.objects.filter(name = search_term)

    def get_department_doctors(self):
        return self.doctors.all


class Doctor(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone_number = models.IntegerField()
    details = models.CharField(max_length=600)
    doctor_image = models.ImageField(upload_to='doctors/',blank=True)
    departments = models.ForeignKey(Department,on_delete=models.CASCADE)

    def save_doctor(self):
        self.save()


    def __str__(self):
        return self.first_name

    
    @classmethod
    def update_doctor(cls, doc_id, first_name, last_name, email, phone_number, details):
        cls.objects.filter(id = doc_id).update(first_name = first_name, last_name = last_name, email = email, phone_number = phone_number, details = details)

class Schedule(models.Model):
    status_choice = (
        ('taken', 'taken'),
        ('available', 'available'),
    )
    app_date = models.DateField("appointment date(mm/dd/yyyy)")
    app_day = models.CharField(max_length=30,blank=True)
    app_hour = models.CharField(max_length=30)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,blank=True)
    status = models.CharField(max_length= 30, choices=status_choice, default='available')
    

    def save_schedule(self):
        self.save()

    def delete_schedule(self):
        self.delete()

    @classmethod
    def get_schedule_by_doctor(cls, doctor_id):
        return cls.objects.filter(doctor = doctor_id, status = 'available').all()

    @classmethod
    def taken_schedule(cls, id):
        cls.objects.filter(id = id).update(status = 'taken')

class Appointment(models.Model):
    status_choice = (
        ('checkedin', 'checked_in'),
        ('unchecked', 'unchecked'),
    )
    first_name = models.CharField(max_length=20,blank=True)
    last_name = models.CharField(max_length=20,blank=True)
    address = models.CharField(max_length=20,blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20,blank=True)
    schedules = models.ForeignKey(Schedule,on_delete=models.CASCADE,default='1')
    status = models.CharField(max_length= 30, choices=status_choice, default='unchecked')

    def save_appointment(self):
        self.save()

    @classmethod
    def checkedin_appointment(cls, id):
        cls.objects.filter(id = id).update(status = 'checkedin')
        

    @classmethod
    def all_checkedin_appointment(cls):
        return cls.objects.filter(status = 'checkedin').all()
        
    
    @classmethod
    def all_unchecked_appointment(cls):
        return cls.objects.filter(status = 'unchecked').all()