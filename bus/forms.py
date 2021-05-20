from django import forms
from .models import *

class PassengerDetailForm(forms.ModelForm):
	class Meta:
		model = PassengerDetail
		fields = ['firstname','lastname','mobile_number']
		

