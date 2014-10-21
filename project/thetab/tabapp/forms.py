from django import forms
from django.core.exceptions import ValidationError
from tabapp.models import Variable, ScoreForm, UserProfile, User, teamName

def custCheckForm(string):
  allowedStr = False
  if "_" in string:
    allowedStr = False
    raise ValidationError("Underscores are not allowed in score sheet names.")
  elif "." in string:
    allowedStr = False
    raise ValidationError("Full stops are not allowed in score sheet names.")
  else:
    allowedStr = True

class UserForm(forms.ModelForm):
  username = forms.CharField(label="Username:")
  email = forms.EmailField(label="Email:")
  password = forms.CharField(widget=forms.PasswordInput(), label="Password:")
  class Meta:
    model = User
    fields = ['username', 'email', 'password']
    
class CustomActivityForm(forms.ModelForm):
  formname = forms.CharField(label="Title:", validators=[custCheckForm])
  groupNames = forms.ModelMultipleChoiceField(teamName.objects.all(), label="Teams:")
  components = forms.ModelMultipleChoiceField(Variable.objects.all(), label="Criteria:")
  timer = forms.BooleanField(initial=False, label="Timer:", required=False)
  
  class Meta:
    model = ScoreForm
    fields = ['formname', 'groupNames', 'components', 'timer']
    
class CustomVariableForm(forms.ModelForm):
  title = forms.CharField(max_length=50, label="Name of Criteria:")
  maxMarks = forms.IntegerField(label="Maximum marks:")
  minMarks = forms.IntegerField(label="Minimum marks:")
    
  class Meta:
    model = Variable
    fields = ['title', 'maxMarks', 'minMarks']
      
class CustomTeamForm(forms.ModelForm):
    name = forms.CharField(max_length=50, label="Team Name:")
    
    class Meta:
        model = teamName
        fields = ['name']