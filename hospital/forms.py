from django import forms
from .models import Hospital, Doctor, Schedule, Department, Appointment
from tinymce.widgets import TinyMCE

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ("name","description", "department_image")
        widgets = {
            "name":forms.TextInput(attrs={"class":"form-control mb-4"}),
            "description":TinyMCE(attrs={'cols': 116, 'rows': 15}),
        }

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'
        exclude = ['status']

class UpdateDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ("name","description")

class UpdateDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        exclude = ['doctor_image', 'departments']


class UpdateScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        exclude = ['doctor', 'status']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['doctors','schedules', 'status']
