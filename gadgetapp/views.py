from django.shortcuts import render, render_to_response
from django.template import RequestContext, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from datetime import datetime

import json

from models import *
from forms import *

# Create your views here.
def is_requester(user):

	if DTUser.objects.filter(user = user, user_type = 'R'):
		return True
	else:
		return False

def user_login(request):

	next = request.POST.get('next', '')

	if request.method == 'POST':

		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user:
			if user is not None and user.is_active:
				login(request, user)
				if next == "":
					return HttpResponseRedirect('/')
				else:
					return HttpResponseRedirect(next)
			else:
				return HttpResponse("Your GetMyGadGet account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'gadgetapp/login.html', {})

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/login')

def Register(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		c_form = UserCreateForm(data=request.POST)

		if user_form.is_valid() and c_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			c = c_form.save(commit=False)
			c.user = user
			c.save()

			c_form.save_m2m()
			registered = True

		else:
			print user_form.errors, c_form.errors

	else:

		user_form = UserForm()
		c_form = UserCreateForm()

	return render(request, 'gadgetapp/register.html', {'user_form': user_form, 'c_form': c_form, 'registered': registered}, RequestContext(request))


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/login')

def DefaultView(request):
	return render_to_response('gadgetapp/home.html', {'user': request.user})

@login_required
def ShowMenu(request):
	if is_requester(request.user):
		usertype = 'user'
	else:
		usertype = 'restaurant'

	menu_parent = Inventory.objects.all()
	return render_to_response("gadgetapp/menu.html", { 'user': request.user, 'restaurant': menu_parent, 'usertype': usertype }, context_instance=RequestContext(request))

def OrderView(request):
	return render_to_response("gadgetapp/order.html", { 'user': request.user })

def Checkout(request):
	return render_to_response("gadgetapp/checkout.html", { 'user': request.user })

def ConfirmOrder(request):
	return render_to_response("gadgetapp/confirmorder.html", { 'user': request.user })
