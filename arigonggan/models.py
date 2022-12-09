import pymysql
from config.settings import PASSWORD as DBPWD
from config.settings import USER as DBUSER
from config.settings import DATABSE as DB
from config.settings import HOST as DBHOST

def userInsert(userId):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password= DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "insert into User (userId) VALUES (%s)"
    res = cur.execute(sql,userId)
    conn.commit()
    conn.close()
    return res

def selectUser(userId):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "select * from User where userId = %s"
    cur.execute(sql,userId)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res

def retrieveAvailavleSeat(seatInfoQuery):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "select id from Seat where floor = %s and name = %s and time = %s and status='activate';"
    cur.execute(sql,seatInfoQuery)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res

def updateSeatStatus(seatId):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "update Seat set status = 'booked' where id = %s;"
    res = cur.execute(sql,seatId)
    conn.commit()
    conn.close()
    return res

def insertReservation(reservationQuery):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "insert into Reservation (userId, seatId,  status) VALUES (%s,%s,%s);"
    res = cur.execute(sql,reservationQuery)
    conn.commit()
    conn.close()
    return res

def updateReservation(reservationQuery):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "update Reservation set status=%s where status=%s and seatId=%s and userId = %s;"
    res = cur.execute(sql,reservationQuery)
    conn.commit()
    conn.close()
    return res

def retrieveAllSeatStatus():
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "Select name,floor,time,status From Seat;"
    cur.execute(sql)
    seatList = []
    for row in cur:
        seatList.append(row)
    conn.commit()
    conn.close()

    return seatList

def retrieveSeatId(seatInfoQuery):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "select id from Seat where floor = %s and name = %s and Seat.time = %s;"
    cur.execute(sql,seatInfoQuery)
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res

def retrieveReserveId(ReserveInfoQuery):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "select id from Reservation where userId=%s and seatId=%s and status=%s and DATE(Reservation.created_at)=DATE(now());"
    cur.execute(sql,ReserveInfoQuery)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res

def retrievedeleteId(ReserveInfoQuery):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "select id from Reservation where userId=%s and seatId=%s and status in ('prebooked','deactivation');"
    cur.execute(sql,ReserveInfoQuery)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res

def deleteSeatStatus(seatId):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "update Seat set status = 'activate' where id = %s;"
    res = cur.execute(sql,seatId)
    conn.commit()
    conn.close()
    return res

def deleteReservation(reservationId):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "update Reservation set status = 'delete' where id = %s"
    sta = cur.execute(sql, reservationId)
    conn.commit()
    conn.close()

    return sta

def autoDelete(reservationId):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "update Reservation set status = 'canceled' where id = %s"
    sta = cur.execute(sql, reservationId)
    conn.commit()
    conn.close()

    return sta



def retrieveReserv(userId):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "Select seatId,status,created_at From Reservation WHERE userId=%s;"
    cur.execute(sql,userId)
    seatList = []
    for row in cur:
        seatList.append(row)
    conn.commit()
    conn.close()

    return seatList

def retrieveSeatById(seatId):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "Select name, floor, Seat.time From Seat WHERE id=%s;"
    cur.execute(sql,seatId)
    res = cur.fetchone()
    conn.commit()
    conn.close()

    return res

def updateAllSeatDisable():
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "update Seat set status = 'disable' where status is not null;"
    cur.execute(sql)
    conn.commit()
    conn.close()

def updateAllSeatActivate():
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "update Seat set status = 'activate' where status is not null;"
    cur.execute(sql)
    conn.commit()
    conn.close()

def checkChangeList(userId):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "select status ,(select Seat.status from Seat where Seat.id=seatId),(select Seat.floor from Seat where Seat.id=seatId) as seatFloor, (select Seat.name from Seat where Seat.id=seatId) as seatName ,(select Seat.time from Seat where Seat.id=seatId) as seatTime from Reservation where userId=%s and DATE(Reservation.created_at)=DATE(now());"
    cur.execute(sql,userId)
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res

def updateSeatDisable(time):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "update Seat set status = 'disable' where Seat.time=%s;"
    cur.execute(sql,time)
    conn.commit()
    conn.close()

def disableUser(userId):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "update User set status = 'disable' where userId=%s;"
    cur.execute(sql, userId)
    conn.commit()
    conn.close()

def activateUser(userId):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "update User set status = 'activate' where userId=%s;"
    cur.execute(sql, userId)
    conn.commit()
    conn.close()

def retrieveUserStatus(userId):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "select status from User where userId=%s;"
    cur.execute(sql, userId)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res

def retriveUserSeat(query):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = '''select id from Reservation where userId = %s and seatId in (select id from Seat where Seat.time in (%s,%s,%s)) and DATE(Reservation.created_at)=DATE(now()) and DATE(Reservation.created_at)=DATE(now()) and status in ("prebooked","booked","deactivation");'''
    cur.execute(sql, query)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res

def updatePrebooked(time):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = '''update Reservation set status ="prebooked" where Reservation.seatId in (select id from Seat where Seat.time = %s) and DATE(Reservation.created_at)=DATE(now()) and Reservation.status = "deactivation"'''
    cur.execute(sql, time)
    conn.commit()
    conn.close()

def updateCanceled(time):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = '''update Reservation set status ="canceled" where Reservation.seatId in (select id from Seat where Seat.time = %s) and DATE(Reservation.created_at)=DATE(now()) and Reservation.status = "prebooked"'''
    cur.execute(sql, time)
    conn.commit()
    conn.close()

def selectCanceledUser(time):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = '''select userId from Reservation where Reservation.seatId in (select id from Seat where Seat.time = %s) and DATE(Reservation.created_at)=DATE(now()) and Reservation.status = "canceled";'''
    cur.execute(sql, time)
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res

def insertUserDisable(query):
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = '''insert into userdisable (userId, activateDate) VALUES (%s,%s);'''
    cur.execute(sql, query)
    conn.commit()
    conn.close()

def updateUserActivate():
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = '''update User set status = 'activate' where userId in (select userId from userdisable where DATE(activateDate)=DATE(NOW()));'''
    cur.execute(sql)
    conn.commit()
    conn.close()

