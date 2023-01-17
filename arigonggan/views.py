from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import pymysql
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from arigonggan import models
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()
from datetime import timedelta,datetime
import time

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
        try:
            data = json.loads(requset.body)
            userId = data['userId']

            # 로그인 전적이 있는 지 확인
            res = models.selectUser(userId)
            if (res==None):
                # 회원가입
                signup(userId)
            # session에 userId 추가
            requset.session['userId'] = userId
        except:
            result = {'code': '400', 'result': 'DB_ERR', 'message': '데이터 베이스 오류'}
            return JsonResponse(result,status=400)
        result = {'code': '200', 'result': 'SUCCESS', 'message': '성공'}
        return JsonResponse(result, status=200)

# (02) signOut api
    elif requset.method == 'PATCH':
        try:
            del requset.session['userId']
            result = {'code': '200', 'result': 'SUCCESS', 'message': '성공'}
            return JsonResponse(result,status=200)
        except:
            result = {'code': '300', 'result': 'WRONG_USER', 'message': '유저 확인에 실패하였습니다.'}
            return JsonResponse(result,status=300)

# (03) add Reservation api
@method_decorator(csrf_exempt,name='dispatch')
def reservation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        floor = data['floor']
        name = data['name']
        time = data['time']
        timeMinus1 = str(int(time[0:2])-1) + ":00:00"
        timePlus1 = str(int(time[0:2])+1) + ":00:00"

        if(len(timeMinus1)==7):
            timeMinus1 = "0"+timeMinus1

        if(len(timePlus1)==7):
            timePlus1 = "0"+timePlus1


        # Login Check
        userId = request.session.get('userId')
        userStatus = models.retrieveUserStatus(userId)
        reservedSeatQuery = (userId,timeMinus1,timePlus1,time)
        reservedSeat = models.retriveUserSeat(reservedSeatQuery)

        if userId==None:
            result = {'code': '300', 'result': 'WRONG_USER', 'message': '유저 확인에 실패하였습니다.'}
            return JsonResponse(result,status=300)
        elif userStatus[0]=='disable':
            result = {'code': '100', 'result': 'ACCESS_DENIED', 'message': '권한이 없는 유저입니다.'}
            return JsonResponse(result, status=100)
        elif reservedSeat!=None:
            result = {'code': '101', 'result': 'RESERVATION_DENIED', 'message': '연속된 시간으로는 예약할 수 없습니다.'}
            return JsonResponse(result, status=101)
        else:
            try:
                seatInfoQuery = (floor, name, time)
                seat = models.retrieveAvailavleSeat(seatInfoQuery)
                if (seat==None):
                    result = {'code': '201', 'result': 'SUCCESS', 'message': '이미 예약된 좌석 이거나 현재 사용 불가한 좌석입니다.'}
                    return JsonResponse(result,status=201)
                else:
                    infoQuery = ('prebooked', 'deactivation', seat[0], userId)
                    models.updateReservation(infoQuery)
                    models.updateSeatStatus(seat[0])
                    h = datetime.now().hour
                    m = datetime.now().minute
                    if(m>=50 and h==(int(time[0:2])-1)):
                        reservationQuery = (userId, seat[0], "prebooked")
                    else:
                        reservationQuery = (userId,seat[0],"deactivation")
                    models.insertReservation(reservationQuery)
                    result = {'code': '200', 'result': 'SUCCESS', 'message': '성공'}
                return JsonResponse(result, status=200)

            except:
                result = {'code': '400', 'result': 'DB_ERR', 'message': '데이터 베이스 오류'}
                return JsonResponse(result,status=400)

# (04) retrieve all seat status
@method_decorator(csrf_exempt,name='dispatch')
def seatList(requset):
    try:
        res = models.retrieveAllSeatStatus()
        result = {'code': '200', 'result': 'SUCCESS', 'message': '성공','res':res}
        return JsonResponse(result, status=200)
    except:
        result = {'code': '400', 'result': 'DB_ERR', 'message': '데이터 베이스 오류'}
        return JsonResponse(result,status=400)

# (05) delete Reservation api
@method_decorator(csrf_exempt, name='dispatch')
def delete(request):
    userId = request.session.get('userId')
    if userId==None:
        result = {'code': '300', 'result': 'WRONG_USER', 'message': '유저 확인에 실패하였습니다.'}
        return JsonResponse(result,status=300)
    else:
        data = json.loads(request.body)
        floor = data['floor']
        name = data['name']
        time = data['time']
        seatInfo = (floor,name,time)
        try:
            seat = models.retrieveSeatId(seatInfo)
            ReserveInfoQuery = (userId,seat[0])
            reserveId = models.retrievedeleteId(ReserveInfoQuery)
            if reserveId == None:
                result = {'code': '301', 'result': 'WRONG_RESERVATION', 'message': '예약 정보 확인에 실패하였습니다.'}
                return JsonResponse(result, status=301)
            else:
                models.deleteReservation(reserveId[0])
                models.deleteSeatStatus(seat[0])
                afterDeleteStatus = models.getReservationStatus(reserveId[0])
                if(afterDeleteStatus[0]!="delete"):
                    models.deleteReservation(reserveId[0])
                    models.deleteSeatStatus(seat[0])
                    print(afterDeleteStatus,reserveId[0])
                result = {'code': '200', 'result': 'SUCCESS', 'message': '성공'}
                return JsonResponse(result, status=200)
        except:
            result = {'code': '400', 'result': 'DB_ERR', 'message': '데이터 베이스 오류'}
            return JsonResponse(result, status=400)

# (06) auto delete Reservation api
@method_decorator(csrf_exempt, name='dispatch')
def autoDelete(request):

    data = json.loads(request.body)
    userId = data['userId']
    floor = data['floor']
    name = data['name']
    time = data['time']
    try:
        queryInfo = (floor, name, time)
        seat = models.retrieveSeatId(queryInfo)
        ReserveInfoQuery = (userId, seat[0])
        reserveId = models.retrievedeleteId(ReserveInfoQuery)
        if reserveId == None:
            result = {'code': '301', 'result': 'WRONG_RESERVATION', 'message': '예약 정보 확인에 실패하였습니다.'}
            return JsonResponse(result, status=301)
        else:
            models.autoDelete(reserveId[0])
            models.disableUser(userId)

            result = {'code': '200', 'result': 'SUCCESS', 'message': '성공'}
            return JsonResponse(result, status=200)
    except:
        result = {'code': '400', 'result': 'DB_ERR', 'message': '데이터 베이스 오류'}
        return JsonResponse(result, status=400)

# (07) Retrieve User Reservation List
@method_decorator(csrf_exempt, name='dispatch')
def userReservation(request):
    userId = request.session.get('userId')
    if userId==None:
        result = {'code': '300', 'result': 'WRONG_USER', 'message': '유저 확인에 실패하였습니다.'}
        return JsonResponse(result,status=300)
    else:
        try:
            reservationList = models.retrieveReserv(userId)
            if len(reservationList) == 0:
                result = {'code': '202', 'result': 'SUCCESS', 'message': '예약 내역이 없습니다.'}
                return JsonResponse(result, status=202)
            else:
                resLIst = []
                i=0
                for item in reservationList:
                    seatInfo = models.retrieveSeatById(reservationList[i][0])
                    tmp = (reservationList[i]+seatInfo)[1:]
                    i+=1;
                    resLIst.append(tmp)
                result = {'code': '200', 'result': 'SUCCESS', 'message': '성공', 'res': resLIst}
                return JsonResponse(result, status=200)
        except:
            result = {'code': '400', 'result': 'DB_ERR', 'message': '데이터 베이스 오류'}
            return JsonResponse(result, status=400)

# (06) auto delete Reservation api
@method_decorator(csrf_exempt, name='dispatch')
def booked(request):
    data = json.loads(request.body)
    userId = request.session.get('userId')
    floor = data['floor']
    name = data['name']
    time = data['time']

    if userId==None:
        result = {'code': '300', 'result': 'WRONG_USER', 'message': '유저 확인에 실패하였습니다.'}
        return JsonResponse(result,status=300)

    try:
        info = (floor,name,time)
        seat = models.retrieveSeatId(info)
        ReserveInfoQuery = (userId, seat[0],'prebooked')
        reserveId = models.retrieveReserveId(ReserveInfoQuery)
        if reserveId == None:
            return JsonResponse({'message': 'Wrong reservation'}, status=301)
        else:
            reserveInfo = ('booked','prebooked',seat[0],userId)
            models.updateReservation(reserveInfo)
            result = {'code': '200', 'result': 'SUCCESS', 'message': '성공'}
            return JsonResponse(result, status=200)
    except:
        result = {'code': '400', 'result': 'DB_ERR', 'message': '데이터 베이스 오류'}
        return JsonResponse(result, status=400)

# (06) auto delete Reservation api
@method_decorator(csrf_exempt, name='dispatch')
def reserveList(request):

    userId = request.session.get('userId')
    if userId==None:
        result = {'code': '300', 'result': 'WRONG_USER', 'message': '유저 확인에 실패하였습니다.'}
        return JsonResponse(result,status=300)
    try:
        seats = models.checkChangeList(userId)
        result = {'code': '200', 'result': 'SUCCESS', 'message': '성공','res':seats}
        return JsonResponse(result, status=200)
    except:
        result = {'code': '400', 'result': 'DB_ERR', 'message': '데이터 베이스 오류'}
        return JsonResponse(result, status=400)

# (07) disalble seat
@method_decorator(csrf_exempt, name='dispatch')
def disableSeat(request):
    try:
        models.updateAllSeatDisable()
        res = models.retrieveAllSeatStatus()
        result = {'code': '200', 'result': 'SUCCESS', 'message': '성공','res':res}
        return JsonResponse(result, status=200)
    except:
        result = {'code': '400', 'result': 'DB_ERR', 'message': '데이터 베이스 오류'}
        return JsonResponse(result, status=400)

# (08) activate seat
@method_decorator(csrf_exempt, name='dispatch')
def activateSeat(request):
    try:
        models.updateAllSeatActivate()
        res = models.retrieveAllSeatStatus()
        result = {'code': '200', 'result': 'SUCCESS', 'message': '성공','res':res}
        return JsonResponse(result, status=200)
    except:
        result = {'code': '400', 'result': 'DB_ERR', 'message': '데이터 베이스 오류'}
        return JsonResponse(result, status=400)

