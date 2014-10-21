from django.shortcuts import render
from django.template import Context, loader 
from django.http import HttpResponse 
from django.shortcuts import render_to_response
from django import forms
from django.forms.util import ErrorList
from tabapp.models import Variable
from django.template import RequestContext
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect  
from tabapp import models
from tabapp.forms import UserForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required  

from tabapp.forms import CustomActivityForm, CustomVariableForm, CustomTeamForm
from tabapp.models import ScoreForm

#URL to String control functions
def encode_url(url):
    return url.replace(' ', '_')
  
def decode_url(url):
    return url.replace('_', ' ')
  
#Index View
def ListActivities(request):
    context = RequestContext(request)
    activity_list = models.ScoreForm.objects.all()
    context_dict = {'activities': activity_list}
    for activity in activity_list:
        activity.url = encode_url(activity.formname)
    # Render the response and return to the client.
    return render_to_response('tabapp/index.html', context_dict, context)
  
#Custom Activities - Activity, Variable, Team Name
@login_required
def add_customActivity(request):
    context = RequestContext(request)
    created = False
    if request.method == 'POST':
        activity_form = CustomActivityForm(data=request.POST)
        if activity_form.is_valid():
            activity_form.save(commit=True)
            created = True
        else:
            print activity_form.errors
    else:
      activity_form = CustomActivityForm()
    return render_to_response('tabapp/createActivity.html',{'activity_form': activity_form,'created': created}, context)

@login_required
def add_customVariable(request):
    context = RequestContext(request)
    created = False
    if request.method == 'POST':
        variable_form = CustomVariableForm(data=request.POST)
        if variable_form.is_valid():
            variable_form.save(commit=True)
            created = True
        else:
            print variable_form.errors
    else:
      variable_form = CustomVariableForm()
    return render_to_response('tabapp/createVariable.html',{'variable_form': variable_form,'created': created}, context)
  
@login_required
def add_customTeam(request):
    context = RequestContext(request)
    created = False
    if request.method == 'POST':
        tmName_form = CustomTeamForm(data=request.POST)
        if tmName_form.is_valid():
            tmName_form.save(commit=True)
            created = True
        else:
            print tmName_form.errors
    else:
      tmName_form = CustomTeamForm()
    return render_to_response('tabapp/createTeam.html',{'tmName_form': tmName_form,'created': created}, context)
  
@login_required 
def customActivity(request, activity_name_url):
    context = RequestContext(request)
    activity_name = decode_url(activity_name_url)
    context_dict = {'activity_name': activity_name}
    try:
        # Can we find an activity with the right name?
        activity = ScoreForm.objects.filter(formname = activity_name)
        context_dict['activity'] = activity
        context_dict['activity_name_url'] = activity_name_url
    except ScoreForm.DoesNotExist:
        # We get here if we didn't find the specified activity.
        pass
    return render_to_response('tabapp/customForm.html', context_dict, context)

@login_required
def delCustomActivity(request, del_name_url):
    context = RequestContext(request)
    del_name = decode_url(del_name_url)
    context_dict = {'del_name': del_name}
    deleted = False
    try:
        delactivity = ScoreForm.objects.filter(formname = del_name)
        delactivity.delete()
        deleted = True
        context_dict['deleted'] = deleted
    except ScoreForm.DoesNotExist:
        deleted = False
        context_dict['deleted'] = deleted
    return render_to_response('tabapp/deleteTemplate.html', context_dict, context)

  #Prepared Templates - Cookie Eating, Swimming, Debate (HTML heavy so not much code here)
def CookEat2(request):
    return render_to_response('tabapp/CookEat2.html', {}, RequestContext(request))

def swimming(request):
    return render_to_response('tabapp/swimming.html', {}, RequestContext(request))
  
def Debate(request):
    return render_to_response('tabapp/Debate.html',{}, RequestContext(request))
  
#Authentication
def register(request):
    context = RequestContext(request)
    # A boolean value for telling the template whether the registration was successful.
    registered = False
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            # Now we hash the password with the set_password method.
            user.set_password(user.password)
            user.save()
            registered = True
        # Invalid form or forms - mistakes or something else?
        else:
            print user_form.errors
    # These forms will be blank, ready for user input.
    else:
      user_form = UserForm()
    return render_to_response('tabapp/register.html',{'user_form': user_form, 'registered': registered},context)
  
def user_login(request):
    context = RequestContext(request)
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Use Django's machinery to attempt to see if the username/password
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None, no user with matching credentials.
        if user:
            if user.is_active:  # Is the account active? It could have been disabled.
                login(request, user)
                return HttpResponseRedirect('/thetab/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your tabber account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    # The request is not a HTTP POST, so display the login form.
    else:
        return render_to_response('tabapp/login.html', {}, context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    return HttpResponseRedirect('/thetab/') 