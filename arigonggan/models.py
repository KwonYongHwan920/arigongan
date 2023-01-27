from django.db import models
from django.utils import timezone

# Create your models here.
class Seat(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,null=False)
    status = models.CharField(max_length=30,default='activate',null=False)
    floor = models.CharField(max_length=50,null=False)
    time = models.TimeField(null=False)

    class Meta:
        db_table = "Seat"

class User(models.Model):
    userId = models.CharField(primary_key=True,max_length=20,null=False,default='activate')
    status = models.CharField(max_length=10,default='activate',null=False)

    class Meta:
        db_table = "User"

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User,related_name="user",on_delete=models.CASCADE,db_column='userId')
    seatId = models.ForeignKey(Seat,related_name="seat",on_delete=models.CASCADE,db_column='seatId')
    status = models.CharField(max_length=15,default='deactivation',null=False)
    created_at = models.DateTimeField(default=timezone.now())

    class Meta:
        db_table = "Reservation"