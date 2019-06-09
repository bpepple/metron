from django.forms import CharField, EmailField, Form, Textarea, TextInput


class ContactForm(Form):
    email = EmailField(widget=TextInput(attrs={"class": "input"}), required=True)
    subject = CharField(
        widget=TextInput(attrs={"class": "input"}), max_length=100, required=True
    )
    message = CharField(widget=Textarea(attrs={"class": "textarea"}), required=True)
