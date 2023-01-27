from django.shortcuts import render,get_object_or_404,_get_queryset
from django.http import JsonResponse,HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()
from django.contrib.auth import authenticate, login
from .models import User,Seat,Reservation

from config import baseResponse
from django.db import transaction
import datetime
from django.utils import timezone


def signUp(userId):
    user = User(userId=userId)
    user.save()

def getMinMax():
    minMax = {
        "today_min" : datetime.datetime.combine(datetime.datetime.today().date(), datetime.datetime.today().time().min),
        "today_max" : datetime.datetime.combine(datetime.datetime.today().date(), datetime.datetime.today().time().max)
    }
    return minMax

@transaction.atomic()
@method_decorator(csrf_exempt,name='dispatch')
def signIn(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            userId = data['userId']
            try:
                get_object_or_404(User,userId=userId)
            except:
                signUp(userId)
            request.session['userId'] = userId
            return baseResponse.SUCCESS
        except:
            return baseResponse.DB_ERR

    elif request.method == 'PATCH':
        try:
            del request.session['userId']
            return baseResponse.SUCCESS
        except:
            return baseResponse.USER_ERR

@transaction.atomic()
@method_decorator(csrf_exempt,name='dispatch')
def postReservation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        floor = data['floor']
        name = data['name']
        time = data['time']
        userId = request.session.get('userId')

        if(userId==None):
            return baseResponse.USER_ERR

        timeMinus1 = str(int(time[0:2]) - 1) + ":00:00"
        timePlus1 = str(int(time[0:2]) + 1) + ":00:00"
        if(len(timeMinus1)==7):
            timeMinus1 = "0"+timeMinus1
        if(len(timePlus1)==7):
            timePlus1 = "0"+timePlus1

        # 유저 status 확인, 좌석 status 확인
        try:
            user = get_object_or_404(User, userId=userId)
            seat = get_object_or_404(Seat, floor=floor, name=name, time=time)
        except:
            return baseResponse.DB_ERR

        if(user.status=='disable'):
            return baseResponse.NO_AUTH
        elif(seat.status=='disable'or seat.status=='booked'):
            return baseResponse.DISABLE_SEAT

        #  유저 전후 1시간 예약 건 확인
        today_min = datetime.datetime.combine(timezone.now().date(), datetime.datetime.today().time().min)
        today_max = datetime.datetime.combine(timezone.now().date(), datetime.datetime.today().time().max)
        seat1 = Seat.objects.filter(time=timeMinus1)
        seat2 = Seat.objects.filter(time=timePlus1)
        resList = Reservation.objects.filter(userId=user,created_at__range =(today_min,today_max),seatId__in=seat2|seat1)
        if len(resList)!=0:
            return baseResponse.DISABLE_RESERVATION

        # Reservation 데이터 추가 Seat status - > booked 변경
        if(timezone.now().hour==(int(time[0:2])-1) and timezone.now().minute>=50):
            reservation = Reservation(status="prebooked", created_at=timezone.now(), seatId=seat,
                                      userId=user)
            reservation.save()
        else:
            reservation = Reservation(status="deactivation", created_at=timezone.now(), seatId=seat,
                                      userId=user)
            reservation.save()
        seat.status="booked"
        seat.save()

        return baseResponse.SUCCESS

@transaction.atomic()
@method_decorator(csrf_exempt,name='dispatch')
def seatStatusList(request):
    if request.method=='GET':

        try:
            seatList = Seat.objects.all()
            res = []
            for seat in seatList:
                seatInfo = []
                seatInfo.append(seat.name)
                seatInfo.append(seat.floor)
                seatInfo.append("P0DT"+ str(seat.time)[0:2] + "H00M00S")
                seatInfo.append(seat.status)
                res.append(seatInfo)

            baseResponse.setRes(res)
            return baseResponse.SUCCESS_DICT
        except: return baseResponse.DB_ERR

@transaction.atomic()
@method_decorator(csrf_exempt,name='dispatch')
def delete(request):

    if request.method=="POST":
        # 유저 확인
        userId = request.session.get('userId')
        if (userId == None):
            return baseResponse.USER_ERR

        else:

            # 좌석 찾기
            data = json.loads(request.body)
            floor = data['floor']
            name = data['name']
            time = data['time']
            try:
                user = get_object_or_404(User,userId=userId)
                seat = get_object_or_404(Seat, floor=floor, name=name, time=time)
            except:
                return baseResponse.DB_ERR

            reservation = Reservation.objects.filter(userId=user,seatId=seat,status__in=['deactivation','prebooked'],created_at__range =(getMinMax()["today_min"],getMinMax()["today_max"]))
            if len(reservation)!=1:
                return baseResponse.WRONG_RESERVATION

            # Reservation 삭제, Seat activate
            reservation.update(status="delete")
            seat.status = "activate"
            seat.save()
            return baseResponse.SUCCESS

@transaction.atomic()
@method_decorator(csrf_exempt, name='dispatch')
def autoDelete(request):
    if request.method=="POST":
        try:
            data = json.loads(request.body)
            userId = data['userId']
            floor = data['floor']
            name = data['name']
            time = data['time']

            # Seat, User, Reservation 정보 검색
            try:
                user = get_object_or_404(User, userId=userId)
                seat = get_object_or_404(Seat, floor=floor, name=name, time=time)
                reservation = get_object_or_404(Reservation,userId=user,seatId=seat,status__in=['deactivation','prebooked'],created_at__range =(getMinMax()["today_min"],getMinMax()["today_max"]))
            except:
                return baseResponse.WRONG_RESERVATION

            # Cancel Reservation , Disable User
            reservation.status = "canceled"
            user.status = "disable"
            reservation.save()
            user.save()
            return baseResponse.SUCCESS
        except:
            return baseResponse.DB_ERR

@transaction.atomic()
@method_decorator(csrf_exempt, name='dispatch')
def userReservation(request):
    if request.method=="GET":
        try:

            # 유저 확인
            userId = request.session.get('userId')
            if (userId == None):
                return baseResponse.USER_ERR
            else:
                try:
                    user = get_object_or_404(User,userId = userId)
                except: return baseResponse.DB_ERR

                reservationList = Reservation.objects.filter(userId=user)

                result = []
                for reservation in reservationList:
                    seat = Seat.objects.filter(id=reservation.seatId.id)
                    info = []
                    info.append(reservation.status)
                    info.append(reservation.created_at)
                    info.append(seat[0].name)
                    info.append(seat[0].floor)
                    info.append("P0DT" + str(seat[0].time)[0:2] + "H00M00S")
                    result.append(info)
                baseResponse.setRes(result)

                return baseResponse.SUCCESS_DICT
        except:
            return baseResponse.DB_ERR

@transaction.atomic()
@method_decorator(csrf_exempt, name='dispatch')
def booked(request):
    if request.method=="POST":
        try:
            data = json.loads(request.body)
            floor = data['floor']
            name = data['name']
            time = data['time']

            # 유저 확인
            userId = request.session.get('userId')
            if (userId == None):
                return baseResponse.USER_ERR
            else:
                try:
                    user = get_object_or_404(User, userId=userId)
                except:
                    return baseResponse.DB_ERR

            # 좌석 확인
            seat = Seat.objects.filter(name=name,floor=floor,time = time)
            if len(seat)==0:
                return baseResponse.WRONG_RESERVATION

            # Reservation 확인
            try:
                reservation = get_object_or_404(Reservation,seatId=seat[0],userId=user,status='prebooked',created_at__range =(getMinMax()["today_min"],getMinMax()["today_max"]))
            except: return baseResponse.WRONG_RESERVATION

            # Reservation 상태 변경
            reservation.status="booked"
            reservation.save()
            return baseResponse.SUCCESS
        except: return baseResponse.DB_ERR

@transaction.atomic()
@method_decorator(csrf_exempt, name='dispatch')
def reserveList(request):
    if request.method == "GET":

        try:

            # 유저 확인
            userId = request.session.get('userId')
            if (userId == None):
                return baseResponse.USER_ERR
            else:
                try:
                    user = get_object_or_404(User, userId=userId)
                except:
                    return baseResponse.DB_ERR

            reservationList = Reservation.objects.filter(userId=user,created_at__range=(getMinMax()["today_min"],getMinMax()["today_max"]))

            result = []
            for reservation in reservationList:
                seat = Seat.objects.filter(id=reservation.seatId.id)
                info = []
                info.append(reservation.status)
                info.append(seat[0].status)
                info.append(seat[0].floor)
                info.append(seat[0].name)
                info.append("P0DT"+ str(seat[0].time)[0:2] + "H00M00S")
                result.append(info)
            baseResponse.setRes(result)

            return baseResponse.SUCCESS_DICT
        except: return baseResponse.DB_ERR

@transaction.atomic()
@method_decorator(csrf_exempt, name='dispatch')
def allSeatDisable(request):
    if request.method == "POST":
        try:
            seatList = Seat.objects.all()
            seatList.update(status='disable')
            return baseResponse.SUCCESS
        except: return baseResponse.DB_ERR

@transaction.atomic()
@method_decorator(csrf_exempt, name='dispatch')
def allSeatActivate(request):
    if request.method == "POST":
        try:
            seatList = Seat.objects.all()
            seatList.update(status='activate')
            return baseResponse.SUCCESS
        except: return baseResponse.DB_ERR
