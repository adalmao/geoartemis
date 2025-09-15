from django.conf import settings
import requests
import json
def create_zoom_room(title,start_time):
    body={   
        "topic": title,
        "type": 2,
        "start_time": start_time,
        "duration": 40,
        "timezone": "America/Lima",
        "password": "1234",
        "settings": {
        "host_video": False,
        "participant_video": False,
        "cn_meeting": False,
        "in_meeting": False,
        "join_before_host": True,
        "mute_upon_entry": False,
        "watermark": False,
        "use_pmi": False,
        "approval_type": 2,
        "audio": "both",
        "auto_recording": "",
        "enforce_login": False,
        "enforce_login_domains": "",
        "alternative_hosts": "",
        "global_dial_in_countries": [
          ""
        ],
        "registrants_email_notification": True
        }
    }
    token='Bearer '+settings.ZOOM_JWT_TOKEN
    headers={'Content-Type':'application/json','Authorization':token}
    request_url='https://api.zoom.us/v2/users/'+settings.ZOOM_USERID+'/meetings'
    r = requests.post(request_url, data=json.dumps(body), headers=headers)
    if r.status_code ==201:
        r=r.json()
        return r['join_url']
    else:
        return False

# def send_email(from_name, from_email, to_email, subject, text_content, html_content, attachment=None):
#     # sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_KEY)
#     mail = Mail(to_email=Email(to_email),
#                 from_email=Email(from_email, from_name),
#                 subject=subject,
#                 content=Content("text/plain", text_content))
#
#     mail.add_content(Content("text/html", html_content))
#
#     if attachment is not None and isinstance(attachment, Attachment):
#         mail.add_attachment(attachment)
#
#     data = mail.get()
#     sg.client.mail.send.post(request_body=data)
#     return True


def add_form_control_class(fields):
    for f in fields:
        fields[f].widget.attrs.update({'class': 'form-control'})

# def add_class(form, fields):
#     for field in fields:
#         form.fields[field].widget.attrs.update(
#             {
#                 "class": 'form-control',
#                 # 'placeholder' : form.fields[field].label
#             }
#         )


def add_form_control_datepicker_class(form, fields):
    for f in fields:
        form.fields[f].widget.attrs.update({'class': 'form-control datepicker'})


def add_form_text(form, fields):
    for f in fields:
        form.fields[f].widget.attrs.update({'type': 'text'})


def add_form_onlyread(form, fields):
    for f in fields:
        form.fields[f].widget.attrs.update({'readonly': 'true'})


def add_form_required(fields):
    for f in fields:
        fields[f].widget.attrs.update({'required': 'true'})


def add_class_time_picker(form, fields):
    for field in fields:
        form.fields[field].widget.attrs.update(
            {
                "class": 'form-control timepicker timepicker-default edited',
                'placeholder': '00:00:00'
            }
        )
