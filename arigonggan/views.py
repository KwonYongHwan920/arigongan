from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import pymysql
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os, time, traceback
from arigonggan import models
import bcrypt
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import SECRET_KEY
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
# def index(request):
#     return HttpResponse("replace main")
@method_decorator(csrf_exempt,name='dispatch')
def index(request):
    userId = request.session.get('userId')
    return HttpResponse(userId)

@method_decorator(csrf_exempt, name='dispatch')
def delete(request):
    data = json.loads(request.body)
    id = data['id']
    query = (id)
    try:
        id = models.delete(query)
        if id == 0:
            return JsonResponse({'message': 'Wrong reservation'}, status=300)
        else:
            request.session['id'] = id
            return JsonResponse({'message': 'SUCCESS'}, status=200)
    except:
        return JsonResponse({'message': 'DBERR'}, status=400)

@method_decorator(csrf_exempt,name='dispatch')
def signup(requset):
    data = json.loads(requset.body)
    userId = data['userId']
    query=(userId)
    try:
        models.usernser(query)
        return JsonResponse({'message':'SUCCESS'},status=200)
    except:
        return JsonResponse({'message':'DBERR'},status=400)

@method_decorator(csrf_exempt,name='dispatch')
def login(request):
    data = json.loads(request.body)
    userId = data['userId']
    query = (userId)
    try:
        res = models.login(query)
        if res == 0:
            return JsonResponse({'message': 'Wrong User'}, status=300)
        else:
            request.session['userId'] = userId
            return JsonResponse({'message': 'SUCCESS'}, status=200)
    except:
        return JsonResponse({'message': 'DBERR'}, status=400)

    #     user = authenticate(request, userId=userId, password=password)
    #     password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())
    #     password_crypt = password_crypt.decode('utf-8')
    #     query = (userId, password_crypt)
    #     try:
    #         models.login(query)
    #         if user is not None:
    #             login(request, user)
    #             return JsonResponse({'message': 'SUCCESS'}, status=200)
    #     except:
    #         return JsonResponse({'message': 'DBERR'}, status=400)

