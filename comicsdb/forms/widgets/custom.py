from django.forms.widgets import ClearableFileInput

class BulmaClearableFileInput(ClearableFileInput):
    template_name = 'comicsdb/BulmaClearableFileInput.html' 
