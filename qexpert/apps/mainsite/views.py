from collections import namedtuple
from django.shortcuts import render
from itertools import groupby
from operator import itemgetter

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.core.serializers import serialize
from django.db.models import F
from django.db.models import Sum
from django.dispatch import receiver
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from users.config import CONFIG

from django.contrib.auth import login as django_login, authenticate, logout as django_logout

from users.forms import AuthenticationForm, RegistrationForm


def home(request):
	ctx = {}
	return render(request,'mainsite/home.jinja', ctx)


def login(request):
	"""
	Log in view
	"""
	form = AuthenticationForm()
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = authenticate(email=request.POST['email'], password=request.POST['password'])
			if user is not None:
				if user.is_active:
					django_login(request, user)
					return redirect('/')
			else:
				form.add_error(None,'Email or Password did not matched')
	return render(request, 'mainsite/login.jinja', {
		'form': form,
	})



def signup(request):
	"""
	User registration view.
	"""
	form = RegistrationForm()
	if request.method == 'POST':
		form = RegistrationForm(data=request.POST)
		if form.is_valid():
			user = form.save()
			
			user = authenticate(email=request.POST['email'], password=request.POST['password1'])
			if user is not None:
				if user.is_active:
					django_login(request, user)
					return redirect('/')
			else:
				form.add_error(None,'Some error occured, cannot create user right now.')
	return render(request, 'mainsite/signup.jinja', {
		'form': form,
	})


def logout(request):
	"""
	Log out view
	"""
	django_logout(request)
	return redirect('/')