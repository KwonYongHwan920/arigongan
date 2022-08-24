import pymysql

def userInsert(userId):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "insert into User (userId) VALUES (%s)"
    res = cur.execute(sql,userId)
    conn.commit()
    conn.close()
    return res

def selectUser(userId):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "select * from User where userId = %s"
    cur.execute(sql,userId)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res

def retrieveAvailavleSeat(seatInfoQuery):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "select id from Seat where floor = %s and name = %s and bookTime = %s and status='activate';"
    cur.execute(sql,seatInfoQuery)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res

def updateSeatStatus(seatId):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "update Seat set status = 'booked' where id = %s;"
    res = cur.execute(sql,seatId)
    conn.commit()
    conn.close()
    return res

def insertReservation(reservationQuery):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "insert into Reservation (userId, seatId,  status) VALUES (%s,%s,%s);"
    res = cur.execute(sql,reservationQuery)
    conn.commit()
    conn.close()
    return res

def retrieveAllSeatStatus():
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "Select name,floor,bookTime,status From Seat;"
    cur.execute(sql)
    seatList = []
    for row in cur:
        seatList.append(row)
    conn.commit()
    conn.close()

    return seatList

def retrieveSeatId(seatInfoQuery):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "select id from Seat where floor = %s and name = %s and bookTime = %s ;"
    cur.execute(sql,seatInfoQuery)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res

def retrieveReserveId(ReserveInfoQuery):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "select id from Reservation where userId=%s and seatId=%s and status='booked';"
    cur.execute(sql,ReserveInfoQuery)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res

def deleteSeatStatus(seatId):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "update Seat set status = 'activate' where id = %s;"
    res = cur.execute(sql,seatId)
    conn.commit()
    conn.close()
    return res

def deleteReservation(reservationId):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "update Reservation set status = 'canceled' where id = %s and status = 'booked'"
    sta = cur.execute(sql, reservationId)
    conn.commit()
    conn.close()

    return sta

def autoDelete(reservationId):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "update Reservation set status = 'deleted' where id = %s and status = 'booked'"
    sta = cur.execute(sql, reservationId)
    conn.commit()
    conn.close()

    return sta



def retrieveReserv(userId):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
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
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "Select name, floor, bookTime From Seat WHERE id=%s;"
    cur.execute(sql,seatId)
    res = cur.fetchone()
    conn.commit()
    conn.close()

    return res

def updateAllSeatDisable():
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "update Seat set status = 'disable' where status is not null;"
    cur.execute(sql)
    conn.commit()
    conn.close()

def updateAllSeatActivate():
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "update Seat set status = 'activate' where status is not null;"
    cur.execute(sql)
    conn.commit()
    conn.close()