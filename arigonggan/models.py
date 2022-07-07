import pymysql



from django.db import models


class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

def userinsert(infoQuery):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = f"insert into User (userId) VALUES ('{infoQuery}')"
    res = cur.execute(sql)
    conn.commit()
    conn.close()
    return res

def selectUser(infoQuery):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "select * from User where userId = %s"
    cur.execute(sql,infoQuery)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res

def selectSeat(floor,name,time):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = f"select id from Seat where floor = '{floor}' and name = '{name}' and time = '{time}';"
    cur.execute(sql)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res

def insertReservation(infoQuery):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "insert into reservation (userId, seatId, userNum, status) VALUES (%s,%s,%s,%s);"
    res = cur.execute(sql,infoQuery)
    conn.commit()
    conn.close()
    return res

def delete(infoQuery):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "update Reservation set status = 'deactivate' where id = %s and status = 'activate'"
    sta = cur.execute(sql, infoQuery)
    conn.commit()
    conn.close()

    return sta