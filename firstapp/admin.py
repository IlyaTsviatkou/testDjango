import hashlib
from django.contrib import admin
from multiprocessing.pool import ThreadPool
from .models import City,Organisation,Number,Course,Player,Profile,Feedback
from django.core.mail import send_mail, BadHeaderError
from hello.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.utils import timezone, dateformat

class EmailReply(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.email_reply_date = dateformat.format(timezone.now(), 'Y-m-d H:i:s')

        def send(name):
            email = Profile.objects.get(user__username=name).user.email
            sha = hashlib.md5(name.encode())
            obj.email_reply_text = 'http://127.0.0.1:8000/confirmation/' + sha.hexdigest()
            send_mail(obj.email_reply_capt, render_to_string('message/message.txt',{'name': name,
            'email': email, 'text': obj.email_reply_text,'time': str(obj.email_reply_date), }), EMAIL_HOST_USER,[email])

        all_object = []

        if form:
            all_object = form.cleaned_data["email_reply_adress"]

        recipients = [x.user.username for x in all_object]
        executor = ThreadPool(len(recipients) + 1)
        executor.map(send, recipients)
        super().save_model(request, obj, form, change)
        #Profile.objects.get(user__username=x)


# Register your models here.
admin.site.register(Feedback, EmailReply)
admin.site.register(City)
admin.site.register(Organisation)
admin.site.register(Number)
admin.site.register(Course)
admin.site.register(Player)
admin.site.register(Profile)