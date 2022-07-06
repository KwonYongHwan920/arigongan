import pymysql



from django.db import models


class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

def usernser(infoQuery):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "insert into User (userId) VALUES (%s)"
    res = cur.execute(sql,infoQuery)
    conn.commit()
    conn.close()

    return res

def login(infoQuery):
    conn = pymysql.connect(host='localhost', user='master', password='master', db='goorm', charset='utf8')
    cur = conn.cursor()
    sql = "select * from User where userId = %s"
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