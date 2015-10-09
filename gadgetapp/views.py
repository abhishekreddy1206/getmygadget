from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
import json
from datetime import datetime
# Create your views here.
from forms import UserForm, UserCreateForm
from models import DTUser, Inventory, Order, OrderDetail


def is_requester(user):
    if DTUser.objects.filter(user=user, user_type='R'):
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

    return render(request, 'gadgetapp/register.html',
                  {'user_form': user_form, 'c_form': c_form, 'registered': registered}, RequestContext(request))


def DefaultView(request):
    return render_to_response('gadgetapp/home.html', {'user': request.user})


@login_required
def ShowMenu(request):
    if is_requester(request.user):
        usertype = 'user'
    else:
        usertype = 'restaurant'

    menu_parent = Inventory.objects.all()
    return render_to_response("gadgetapp/menu.html",
                              {'user': request.user, 'restaurant': menu_parent, 'usertype': usertype},
                              context_instance=RequestContext(request))


def OrderView(request):
    return render_to_response("gadgetapp/order.html", {'user': request.user})


def Checkout(request):
    return render_to_response("gadgetapp/checkout.html", {'user': request.user})


def ConfirmOrder(request):
    return render_to_response("gadgetapp/confirmorder.html", { 'user': request.user })

def PostOrder(request):

    if request.method == 'POST':
        data = request.body
        order_data = json.loads(data)
        total = sum(c['price']*c['quantity'] for c in order_data)

        dtuser = DTUser.objects.get(user = request.user)
        order_save = Order(user = dtuser, total_price = total, update_timestamp = datetime.now())
        order_save.save()

        for i in range(0,len(order_data)):
            x = order_data[i]
            inv = Inventory.objects.get(name = x['name'], parent = x['parent'], level=x['level'])
            order_detail_save = OrderDetail(order = order_save, inventory = inv, quantity = x['quantity'])
            order_detail_save.save()

        # subject = "CloudMellow: Thank you for you Order"

        # plaintext = get_template('bhojanamapp/emailreceived.txt')
        # htmly = get_template('bhojanamapp/emailreceived.html')
        # d = Context({ 'username': request.user.username, 'order_data': order_data, 'total': total })

        # text_content = plaintext.render(d)
        # html_content = htmly.render(d)

        # from_email = settings.EMAIL_HOST_USER
        # to_list = [request.user.email]
        # msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()

    return render_to_response("gadgetapp/confirmorder.html", {'user': request.user})

def PostNotes(request):

    if request.method == 'POST':
        data = request.body
        order_data = json.loads(data)
        notes = order_data['notes']

        order_save = Order.objects.filter(user__user = request.user).order_by('-id')[0]
        order_save.user_notes = notes
        order_save.save()

    return render_to_response("gadgetapp/confirmorder.html", { 'user': request.user })

@login_required
def Dashboard(request):
    if is_requester(request.user):
        return render_to_response("gadgetapp/requesterdashboard.html", { 'user': request.user })
    else:
        return render_to_response("gadgetapp/approverdashboard.html", { 'user': request.user })