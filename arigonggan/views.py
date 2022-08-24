from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import pymysql
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from arigonggan import models
from arigonggan import cralwer
from django.conf import settings
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import register_events, DjangoJobStore
import time

def seatChangeDisable():
    scheduler=BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    @scheduler.scheduled_job('cron',hour='19', minute = '0', name = 'disable')
    def changedisable():
        disableSeat()
        print("disable complete")
    scheduler.start()

def seatChangeActivate():
    scheduler=BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    @scheduler.scheduled_job('cron',hour='0', minute = '0', name = 'activate')
    def changeActivate():
        activateSeat()
        print("activate complete")
    scheduler.start()

def disableSeat():
    try:
        models.updateAllSeatDisable()
        res = models.selectAllSeat()
        return JsonResponse({'message': 'SUCCESS','res':res}, status=200)
    except:
        return JsonResponse({'message': 'DBERR'}, status=400)

def activateSeat():
    try:
        models.updateAllSeatActivate()
        res = models.selectAllSeat()
        return JsonResponse({'message': 'SUCCESS','res':res}, status=200)
    except:
        return JsonResponse({'message': 'DBERR'}, status=400)

def signup(userId):
    res = models.userInsert(userId)
    return 0

# (00) session check api
@method_decorator(csrf_exempt,name='dispatch')
def index(request):
    if request.method == 'GET':
        userId = request.session.get('userId')
        return HttpResponse(userId)

# (01) signUp & signIn api
@method_decorator(csrf_exempt,name='dispatch')
def logIn(requset):
    if requset.method == 'POST':
        data = json.loads(requset.body)
        userId = data['userId']

        # 로그인 전적이 있는 지 확인
        res = models.selectUser(userId)
        if (res==None):
            # 회원가입
            signup(userId)

        # session에 userId 추가
        requset.session['userId'] = userId
        return JsonResponse({'message': 'SUCCESS'}, status=200)

# (02) signOut api
    elif requset.method == 'PATCH':
        try:
            del requset.session['userId']
            return JsonResponse({'message':'SUCCESS'},status=200)
        except: return JsonResponse({'message':'WRONG_User'},status=300)

# (03) add Reservation api
@method_decorator(csrf_exempt,name='dispatch')
def reservation(request):
    if request.method == 'POST':

        # Login Check
        userId = request.session.get('userId')
        if userId=="None":
            return JsonResponse({'message':'WRONG_User'},status=300)
        else:
            data = json.loads(request.body)
            floor = data['floor']
            name = data['name']
            time = data['time']
            seatInfoQuery = (floor,name,time)
            try:
                seat = models.retrieveAvailavleSeat(seatInfoQuery)
                if (seat!=None):
                    models.updateSeatStatus(seat[0])
                    reservationQuery = (userId,seat[0],"booked")
                    models.insertReservation(reservationQuery)
                    return JsonResponse({'message': 'SUCCESS'}, status=200)
                else:   return JsonResponse({'message':'이미 예약된 자석입니다.'},status=200)
            except: return JsonResponse({'message':'DB_ERR'},status=400)

# (04) retrieve all seat status
@method_decorator(csrf_exempt,name='dispatch')
def seatList(requset):
    try:
        res = models.retrieveAllSeatStatus()
        return JsonResponse({'message': 'SUCCESS','res':res}, status=200)
    except: return JsonResponse({'message':'DB_ERR'},status=400)

# (05) delete Reservation api
@method_decorator(csrf_exempt, name='dispatch')
def delete(request):
    userId = request.session.get('userId')
    if userId==None:
        return JsonResponse({'message':'WRONG_User'},status=300)
    else:
        data = json.loads(request.body)
        floor = data['floor']
        name = data['name']
        time = data['time']
        seatInfo = (floor,name,time)
        try:
            seat = models.retrieveSeatId(seatInfo)
            ReserveInfoQuery = (userId,seat[0])
            reserveId = models.retrieveReserveId(ReserveInfoQuery)
            if reserveId == None:
                return JsonResponse({'message': 'Wrong reservation'}, status=300)
            else:
                models.deleteReservation(reserveId[0])
                models.deleteSeatStatus(seat[0])
                return JsonResponse({'message': 'SUCCESS'}, status=200)
        except:
            return JsonResponse({'message': 'DBERR'}, status=400)

# (06) auto delete Reservation api
@method_decorator(csrf_exempt, name='dispatch')
def autoDelete(request):

    data = json.loads(request.body)
    userId = data['userId']
    floor = data['floor']
    name = data['name']
    time = data['time']
    try:
        seat = models.retrieveSeatId(floor, name, time)
        ReserveInfoQuery = (userId, seat[0])
        reserveId = models.retrieveReserveId(ReserveInfoQuery)
        if reserveId == None:
            return JsonResponse({'message': 'Wrong reservation'}, status=300)
        else:
            models.autoDelete(reserveId[0])
            models.deleteSeat(seat[0])
            return JsonResponse({'message': 'SUCCESS'}, status=200)
    except:
        return JsonResponse({'message': 'DBERR'}, status=400)

# (07) Retrieve User Reservation List
@method_decorator(csrf_exempt, name='dispatch')
def userReservation(request):
    userId = request.session.get('userId')
    if userId==None:
        return JsonResponse({'message':'WRONG_User'},status=300)
    else:
        try:
            reservationList = models.retrieveReserv(userId)
            if len(reservationList) == 0:
                return JsonResponse({'message': '예약 내역이 없습니다'}, status=200)
            else:
                resLIst = []
                i=0
                for item in reservationList:
                    seatInfo = models.retrieveSeatById(reservationList[i][0])
                    tmp = (reservationList[i]+seatInfo)[1:]
                    i+=1;
                    resLIst.append(tmp)
                return JsonResponse({'message': 'SUCCESS','res':resLIst}, status=200)
        except:
            return JsonResponse({'message': 'DBERR'}, status=400)
