from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template

from comicsdb.forms.contact import ContactForm


def EmailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, email, ['brian@pepple.info'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('contact:success')
    return render(request, "comicsdb/contact-us.html", {'form': form})


def SuccessView(request):
    t = get_template('comicsdb/contact-success.html')
    message = 'Success! Thank you for contacting us.'
    html = t.render({'msg': message})
    return HttpResponse(html)
