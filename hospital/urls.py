from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
    url('^$',views.index,name = 'index'),
    url('^admin/all-departments',views.all_departments, name = 'all-departments'),
    url('^admin/new-department',views.new_department, name = 'new_department'),
    url('^admin/doctors',views.all_doctors, name = 'doctors'),
    url('^admin/new-doctor',views.new_doctor, name = 'new_doctor'),
    url('^admin/schedules',views.all_schedules, name = 'schedules'),
    url('^admin/new-schedule',views.new_schedule, name = 'new_schedule'),
    url('^admin/department_delete/(?P<pk>\d+)$',views.department_delete, name = 'department_delete'),
    url('^admin/doctor_delete/(?P<pk>\d+)$',views.doctor_delete, name = 'doctor_delete'),
    url('^admin/update_department/(?P<pk>\d+)$',views.update_department, name = 'update_department'),
    url('^admin/update_doctor/(?P<pk>\d+)$',views.update_doctor, name = 'update_doctor'),
    url('^admin/update_schedule/(?P<pk>\d+)$',views.update_schedule, name = 'update_schedule'),
    url('^admin/schedule_delete/(?P<pk>\d+)$',views.schedule_delete, name = 'schedule_delete'),
    url('^admin/unchecked',views.all_unchecked_appointments, name = 'unchecked'),
    url('^admin/checkedin',views.all_checkedin_appointments, name = 'checkedin'),
    url('^admin/checkin/(\d+)$', views.checkin, name='checkin'),
    url('^user_departments',views.user_departments, name = 'user_departments'),
    url('^user_doctors',views.user_doctors, name = 'user_doctors'),
    url('^department_detail/(\d+)$', views.department_detail, name='department_detail'),
    url('^doctor_detail/(\d+)$', views.doctor_detail, name='doctor_detail'),
    url('^searched', views.search_doctor, name='searched'),
    url('^appointment/(\d+)$', views.make_appointment, name='appointment'),
    url('^admin/doctor-search', views.search_doc, name='doctor-search'),
    url('^admin/emergency(?P<pk>\d+)$', views.doctor_emergency, name='emergency'),
    
    
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
