from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_welcome_email(first_name,last_name,schedule,receiver):
    # Creating message subject and sender
    subject = 'Welcome to the Heath Care Hospital'
    sender = 'hospitalheathcare@gmail.com'

    #passing in the context vairables
    text_content = render_to_string('patient/email/newsemail.txt',{"first_name": first_name,"last_name":last_name,"schedule":schedule})
    html_content = render_to_string('patient/email/newsemail.html',{"first_name": first_name,"last_name":last_name,"schedule":schedule})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()


def send_emergency_email(first_name,last_name,schedule,receiver):
    # Creating message subject and sender
    subject = 'Heath Care Hospital Emergency'
    sender = 'hospitalheathcare@gmail.com'

    #passing in the context vairables
    text_content = render_to_string('admin/email/newsemail.txt',{"first_name": first_name,"last_name":last_name,"schedule":schedule})
    html_content = render_to_string('admin/email/newsemail.html',{"first_name": first_name,"last_name":last_name,"schedule":schedule})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()