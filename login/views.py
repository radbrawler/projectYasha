from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.conf import settings
from django.conf.urls.static import static
from django.utils import timezone
from datetime import timedelta
import json
import socket
from login.models import *
from django.core.exceptions import *
import requests

# Create your views here.


def index(request):
    return render(request, "users/login.html")


class Socket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        else:
            self.sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        sent = self.sock.send(msg)


def user_login(request):
    try:
        if request.session['username']:
            return HttpResponseRedirect('/login/index')
    except KeyError:
        context = RequestContext(request)
        error = False
        if request.method == 'POST' and request.is_ajax():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            # print(user)
            if user is not None:
                if user.is_authenticated():
                    login(request, user)
                    request.session['username'] = username
                    request.session['password'] = password
                    return HttpResponse(json.dumps({'errors': error}), content_type='application/json')
                else:
                    print('in auth')
                    error = True
                    return HttpResponse(json.dumps({'errors': error}), content_type='application/json')
            else:
                error = True
                return HttpResponse(json.dumps({'errors': error}), content_type='application/json')
        return render(request, 'users/login.html')


@login_required
def user_logout(request):
    del request.session['username']
    del request.session['password']
    logout(request)
    return HttpResponseRedirect("/login/login")


@login_required
def index(request):
    if request.session['username']:
        # print(request.session['username'])
        obj = Object.objects.filter(currentOwner=request.session['username'])
        try:
            user = Student.objects.get(username=request.session['username'])
            u_type = 'student'
        except ObjectDoesNotExist:
            try:
                user = Faculty.objects.get(username=request.session['username'])
                u_type = 'faculty'
            except ObjectDoesNotExist:
                user = Admin.objects.get(username=request.session['username'])
                u_type = 'admin'

        nn = 0  # Notification number
        if u_type == 'admin':
            return HttpResponseRedirect('/login/admin')

        elif u_type is 'faculty':
            n = NotificationFaculty.objects.filter(receiver=user, status=False)

            for i in n:
                if i.status is False:
                    nn += 1

            return render(request, 'users/index.html', {'obj': obj, 'user': user, 'nn': nn, 'notifs': n})

        else:
            return render(request, 'users/index.html', {'obj': obj, 'user': user, 'nn': nn})

    else:
        # print('before home')
        return HttpResponseRedirect('/home')


@login_required
def req(request):
    obj = Object.object_verbose()
    user = User.objects.get(username=request.session['username'])
    return render(request, 'users/request.html', {'obj': obj, 'user': user})


@login_required
def val_req(request):  # validate request for user
    try:
        username = request.session['username']
        print(username)
        try:
            user = Student.objects.get(username=request.session['username'])
            u_type = 'student'
            print(user.mentor)
        except ObjectDoesNotExist:
            print('In here')
            user = Faculty.objects.get(username=request.session['username'])
            u_type = 'faculty'
            print(user)

        o_type = request.POST['object']
        qty = request.POST['qty']
        if u_type == 'faculty':
            status = 'A'
        else:
            status = 'P'
        # req_to = user.mentor

        r = Request(r_username=user, r_object=o_type, status=status, number=qty,
                    date_of_request=timezone.now(), requested_to=user.mentor,
                    date_of_completion=timezone.now() + timedelta(days=20))
        r.save()
        msg = 'Request created successfully'

        title = str(user.name)+' has requested '+str(qty)+' '+str(o_type)
        print(title)
        if u_type == 'faculty':
            n = NotificationFaculty(title=title, receiver=user.mentor, request=r, status=True)
        else:
            n = NotificationFaculty(title=title, receiver=user.mentor, request=r, status=False)
        n.save()
        print('after saving both entries in db')

    except KeyError:
        msg = 'Request can\'t be created. Error maybe due empty database values.'
    print(msg)
    return HttpResponse(json.dumps({'errors': msg}), content_type='application/json')


@login_required
def dummy(request):
    msg = 'This is a success message'
    return render(request, 'users/index.html', {'msg': msg})


@login_required()
def approve(request):
    r = request.POST['req']
    id = request.POST['id']

    notif = NotificationFaculty.objects.get(id=id)
    print(type(r), type('app'))
    print(r)
    if str(r) == 'app':
        print("in if")
        notif.status = True
        notif.request.status = 'A'
        notif.request.save()

    elif str(r) == 'rej':
        print("in else")
        notif.status = True
        notif.request.status = 'D'
        notif.request.save()
    notif.save()
    msg = 'saved notif'
    print(notif.request.status)
    return HttpResponse(json.dumps({'msg': msg}), content_type='application/json')


@login_required
def admin(request):
    user = request.session['username']
    r = Request.objects.filter(status='A')
    n = NotificationFaculty.objects.filter(request=r)
    nn = len(n)
    # for i in n:
    #     if i.status is False:
    #         nn += 1
    usr = Student.objects.all().order_by('roll_no')
    fac = Faculty.objects.all()
    obj = Object.objects.all()
    # for t in OBJECT_TYPE:
    #     o = Object.objects.filter(type=t[0])
    #     if o.count():
    #         o[0].quantity = o.count()
    #         print(o[0].quantity, o.count())
    #         obj.append(o[0])

    print(obj)
    return render(request, 'users/admin.html', {'notifs': n, 'nn': nn, 'usr': usr, 'obj': obj})


@login_required
def ass_obj(request):  # called by admin
    r = request.POST['req']
    id = request.POST['id']

    notif = NotificationFaculty.objects.get(id=id)
    req = notif.request
    obj = Object.objects.filter(type=req.r_object)
    print(obj)

    if obj.count() >= req.number:
        req.status = 'C'
        req.date_of_completion = timezone.now()
        req.save()
        for i in range(obj.count()):
            o = obj[i]
            o.currentOwner = req.r_username
            o.save()
        msg = 'Objects Assigned to ' + str(req.r_username.name)
        print(obj)
        return HttpResponse(json.dumps({'msg': msg}), content_type='application/json')

    else:
        msg = 'Inventory doesn\'t have enough resources. Please purchase resources.'
        return HttpResponse(json.dumps({'errors': msg}), content_type='application/json')


@login_required
def obj_form(request):
    obj = Object.object_verbose()
    user = User.objects.get(username=request.session['username'])
    return render(request, 'users/create_object.html', {'obj': obj, 'user': user})


@login_required
def create_obj(request):
    try:
        num = int(request.POST['quantity'])
        print(int(num))
        user = User.objects.get(username=request.session['username'])

        for i in range(num):
            obj = Object(name=request.POST['type'] + str(timezone.now()),
                         dueDate=timezone.now() + timedelta(days=int(request.POST['dueDate'])),
                         currentOwner=user, type=request.POST['type'], cost=float(request.POST['cost']),
                         quantity=1)
            obj.save()

        msg = 'Objects Created Successfully'
        print(msg)
        return HttpResponse(json.dumps({'msg': msg}), content_type='application/json')
    except ObjectDoesNotExist:
        msg = 'Could Not create Objects'
        print(msg)
        return HttpResponse(json.dumps({'errors': msg}), content_type='application/json')

