from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import pymysql
import json
from config import baseResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from arigonggan.models import Seat,Reservation,User
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()
import datetime
from django.db import transaction
from django.utils import timezone


def timeSet():
    timeSet = {
        "minTime" : timezone.datetime.combine(timezone.now().today().date(),timezone.now().today().time().min),
        "maxTime" : timezone.datetime.combine(timezone.now().today().date(),timezone.now().today().time().max),
        "now" : timezone.now()
    }
    return timeSet

@transaction.atomic()
@method_decorator(csrf_exempt, name='dispatch')
def ntest(request):
    seat = Seat.objects.all()
    seat.update(status='activate')
    user = User.objects.all()
    user.update(status='activate')
    return baseResponse.SUCCESS


# Scheduler - Disable (09:00-18:00)

@transaction.atomic()
@sched.scheduled_job('cron',hour='9-18', minute = '00',name = 'disable')
def disableSeat():
    stime = f'{timeSet()["now"].hour}:00:00'
    seatList = Seat.objects.filter(time=stime)
    seatList.update(status='disable')


# Scheduler - Canceled(09:10-18:10)

@transaction.atomic()
@sched.scheduled_job('cron',hour='9-18', minute = '10',name = 'cancel')
def cancelReservation():
    stime = f'{timeSet()["now"].hour}:00:00'
    seatList = Seat.objects.filter(time=stime)
    cancelList = Reservation.objects.filter(seatId__in=seatList, status="prebooked",
                                            created_at__range=(timeSet()["minTime"], timeSet()["maxTime"]))
    userList = []
    for item in cancelList:
        userList.append(item.userId.userId)
    cancelList.update(status='canceled')
    user = User.objects.filter(userId__in=userList)
    user.update(status='disable')


# Scheduler - Prebooked(08:50-17:50)

@transaction.atomic()
@sched.scheduled_job('cron',hour='8-17', minute = '50',name='prebook')
def prebookReservation():
    prebookedTime = f'{timeSet()["now"].hour+1}:00:00'
    seatList = Seat.objects.filter(time=prebookedTime)
    bookList = Reservation.objects.filter(seatId__in=seatList, status="deactivation",
                                          created_at__range=(timeSet()["minTime"], timeSet()["maxTime"]))
    bookList.update(status='prebooked')


# Scheduler - Activate(00:00)

@transaction.atomic()
@sched.scheduled_job('cron',hour='00', minute = '00',name = 'activate')
def activateSeat():
    seat = Seat.objects.all()
    seat.update(status='activate')
    user = User.objects.all()
    user.update(status='activate')

sched.start()



