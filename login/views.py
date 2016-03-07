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
from datetime import *
import json
import socket
from login.models import User, Object
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
            print('before this')
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
                return HttpResponse(json.dumps({'errors': error}), content_type='application.json')
        print('before return')
        return render(request, 'users/login.html')


@login_required
def index(request):
    if request.session['username']:
        # print(request.session['username'])
        obj = Object.objects.filter(currentOwner=request.session['username'])
        user = User.objects.get(username=request.session['username'])
        print(user)
        return render(request, 'users/index.html', {'obj': obj, 'user': user})

    else:
        print('before home')
        return HttpResponseRedirect('/home')


@login_required
def req(request):
    obj = Object.object_verbose()
    print(obj)
    return render(request, 'users/request.html', {'obj': obj})

