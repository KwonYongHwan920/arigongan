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

@method_decorator(csrf_exempt,name='dispatch')
def index(request):
    userId = request.session.get('userId')
    return HttpResponse(userId)

def signup(userId):
    res = models.userinsert(userId)
    return 0

@method_decorator(csrf_exempt,name='dispatch')
def logIn(requset):
    if requset.method == 'POST':
        data = json.loads(requset.body)
        userId = data['userId']

        # 크롤러 성공 설정
        # result = crawler.check_login(userId,password)
        result = 1

        if result==1:
            res = models.selectUser(userId)
            if (res==None):
                signup(userId)
            requset.session['userId'] = userId
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        elif result==0: return JsonResponse({'message':'WRONG_User'},status=300)
    elif requset.method == 'PATCH':
        try:
            del requset.session['userId']
            return JsonResponse({'message':'SUCCESS'},status=200)
        except: return JsonResponse({'message':'WRONG_User'},status=300)

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
def reservation(request):
    userId = request.session.get('userId')
    if userId=="None":
        return JsonResponse({'message':'WRONG_User'},status=300)
    else:
        data = json.loads(request.body)
        floor = data['floor']
        name = data['name']
        time = data['time']
        userNum = data['userNum']
        try:
            seat = models.selectSeat(floor,name,time)
            if (seat!=None):
                reserveInfoQuery = (userId,seat[0],userNum,"loading")
                models.insertReservation(reserveInfoQuery)
                return JsonResponse({'message': 'SUCCESS'}, status=200)
            else:   return JsonResponse({'message':'DB_ERR'},status=400)
        except: return JsonResponse({'message':'DB_ERR'},status=400)
