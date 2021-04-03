from django.db import models

# Create your models here.


class Bots(models.Model):
    comment = models.CharField(max_length=300)
    login = models.CharField(max_length=300)
    password =  models.CharField(max_length=300)
    steamid = models.CharField(max_length=300,unique=True)
    shared_secret = models.CharField(max_length=300)
    steamAPI = models.CharField(max_length=300)
    googleDriveId = models.CharField(max_length=300)
    proxy = models.CharField(max_length=300)
    turn = models.BooleanField(default=False)

class Logs(models.Model):
    bot = models.CharField(max_length=300,default='')
    time = models.CharField(max_length=50)
    proxy = models.CharField(max_length=300)
    request = models.CharField(max_length=1024)
    response = models.CharField(max_length=1024)

    log_type=models.CharField(max_length=300)

from datetime import datetime
class Item(models.Model):
    bot = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    drive_price = models.CharField(max_length=300,blank=True)
    d_time = models.DateTimeField(blank=True,default=datetime.now())
    steam = models.CharField(max_length=300,blank=True)
    s_time = models.CharField(max_length=300,blank=True)
    min_profit = models.CharField(max_length=300,blank=True)
    min_time = models.CharField(max_length=300,blank=True)
    max_profit = models.CharField(max_length=300,blank=True)
    max_time = models.CharField(max_length=300,blank=True)
    hold_off = models.DateField(default=datetime.now)
    status = models.CharField(max_length=300,blank=True)
    place = models.CharField(max_length=300,blank=True)
    assedID = models.CharField(max_length=300,unique=True)
    d_discount = models.CharField(max_length=300,blank=True)
    ru_link = models.CharField(max_length=350,blank=True)
    en_link = models.CharField(max_length=350,blank=True)

class Profit(models.Model):
    min_p = models.IntegerField()
    max_p = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)


class SteamItem(models.Model):
    name = models.CharField(max_length=300)
    price = models.IntegerField()
    time = models.DateTimeField(blank=True,auto_now_add=True)
#class SteamItem(models.Model):
