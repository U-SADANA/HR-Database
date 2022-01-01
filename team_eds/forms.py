from django import forms
 
# creating a form
class InputForm(forms.Form):
    email = forms.EmailField(required=True)
    