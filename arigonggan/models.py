import pymysql

conn = pymysql.connect(host='localhost', user='master', password='master', db='arigonggan', charset='utf8')

from django.db import models


class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

def usernser(infoQuery):
    cur = conn.cursor()
    sql = "insert into User (userId) VALUES (%s)"
    res = cur.execute(sql,infoQuery)
    conn.commit()
    conn.close()

    return res

def login(infoQuery):
    cur = conn.cursor()
    sql = "select * from User where userId = %s"
    res = cur.execute(sql,infoQuery)
    conn.commit()
    conn.close()

    return res

def delete(infoQuery):
    cur = conn.cursor()
    sql = "update Reservation set status = 'deactivate' where id = %s"
    sta = cur.execute(sql, infoQuery)
    conn.commit()
    conn.close()

    return sta