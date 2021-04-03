from celery import shared_task
from main.models import Item

from celery.decorators import periodic_task
from celery.schedules import crontab

from .models import *

import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

import urllib
import json
import datetime as dt


@periodic_task(run_every=(crontab(minute='*/1')),name="my_third_task")
def my_third_task():
    bots = Bots.objects.filter()
    for b in bots:
        steamID = b.steamid
        steam = urllib.request.urlopen('https://steamcommunity.com/profiles/%s/inventory/json/730/2'%(steamID)).read().decode('UTF-8')
        JSON_object = json.loads(steam)
        notAt = 0
        for i in Item.objects.filter(bot=b.login):
            if JSON_object.get('rgInventory').get(i.assedID) == None:
                i.status = 'NotAtInventory'
                i.save()
                notAt += 1
        Logs.objects.create(time=str(dt.datetime.now()),log_type='others',bot='',proxy='',request='Check inventory for '+ b.login +' NotAtInventory('+str(notAt)+')',response='sucsess')
        addTo = 0
        for i in JSON_object.get('rgInventory'):
            try:
                items = Item.objects.get(bot=b.login,assedID=i)
            except:
                try:
                    class_id = JSON_object.get('rgInventory')[i].get('classid')
                    instance_id = JSON_object.get('rgInventory')[i].get('instanceid')
                    q = class_id + '_' + instance_id

                    instanc = JSON_object.get('rgDescriptions').get(q)
                    name =instanc.get('market_hash_name')
                    ru_name = instanc.get('market_name')
                    en_link = 'https://market.csgo.com/?s=price&r=&q=&search='+name
                    ru_link = 'https://market.csgo.com/?s=price&r=&q=&search='+ru_name
                    try:
                        d_time = instanc.get(cache_expiration)
                    except:
                        d_time = dt.datetime.now()
                    try:
                        steam_p = SteamItem.objects.get(name=name).price
                    except:
                        steam_p = 'Wait'
                    status = 'New'
                    d_discount = '0%(0)'
                    place = 'NotDetermined'
                    try:
                        min_p = str(Profit.objects.get(pk=1).min_p)
                        max_p = str(Profit.objects.get(pk=1).max_p)
                        time_p = str(Profit.objects.get(pk=1).time)
                    except:
                        p = Profit.objects.create(min_p=100,max_p=100)
                        min_p = str(100)
                        max_p = str(100)
                        time_p = str(p.time)
                    a = Item.objects.create(assedID=i,bot=b.login,name=name,drive_price=steam_p,place = 'NotDetermined',d_discount=d_discount,d_time=d_time,status=status,en_link=en_link,ru_link=ru_link,min_profit=min_p,max_profit=max_p,min_time=time_p,max_time=time_p)
                    addTo += 1
                except Exception as e:
                    print('Либо в другом аккаунте либо ошибка: ',e)
        Logs.objects.create(time=str(dt.datetime.now()),log_type='others',bot='',proxy='',request='Check for admin inventory items in admin for  '+ b.login +' AddedItems('+str(addTo)+')',response='sucsess')

@periodic_task(run_every=(crontab(minute='*/1')),name="my_second_task")
def my_second_task():
    steam = urllib.request.urlopen('https://api.steamapis.com/market/items/730?api_key=bmyRVmF1HOQ9IH5LmSInrD8FgV4&format=comact').read().decode('UTF-8')
    JSON_object = json.loads(steam)
    items = Item.objects.all()
    for i in items:
        try:
            a = SteamItem.objects.get(name=i.name)
            a.price = int(JSON_object.get(i.name))
            a.save()
            i.steam = JSON_object.get(i.name)
            i.save()
        except:
            s = SteamItem.objects.create(name=i.name,price = int(JSON_object.get(i.name)))
            s.save()
            i.steam = JSON_object.get(i.name)
            if i.place == 'NotDetermined':
                i.drive_price = JSON_object.get(i.name)
            i.s_time = str(dt.datetime.now())
            i.save()

    Logs.objects.create(time=str(dt.datetime.now()),log_type='others',bot='',proxy='',request='Steam All Parsing ' +'('+str(len(items))+')',response='sucsess')


@periodic_task(run_every=(crontab(minute='*/1')),name="my_first_task")
def my_first_task():
    bots = Bots.objects.all()

    CREDENTIALS_FILE = 'main/by David-a6013fe2ec30.json'  # имя файла с закрытым ключом

    for b in bots:
        spreadsheets_id= b.googleDriveId  #'1XIfaox14sadvI2CWXPJ29pTgbDsHdZr8a0dBD8jfHhc'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                                                          'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)

        k = 0
        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheets_id,
            range='A:H',
            majorDimension='ROWS'
        ).execute()
        for i in values.get("values")[1::]:
            # print(JSON_object.get(i[0]))
            try:
                try:
                    min_p = str(Profit.objects.get(pk=1).min_p)
                    max_p = str(Profit.objects.get(pk=1).max_p)
                    time_p = str(Profit.objects.get(pk=1).time)
                except:
                    p = Profit.objects.create(min_p=100,max_p=100)
                    min_p = str(100)
                    max_p = str(100)
                    time_p = str(p.time)
                Item.objects.create(bot=b.login,name=i[0],drive_price=i[1],d_time=str(dt.datetime.now()),hold_off=i[3],status='New',assedID=i[4],d_discount=i[2],s_time=steam_time,steam='',min_profit=min_p,max_profit=max_p,min_time=time_p,max_time=time_p)
                k+=1
                # Logs.objects.create(time=str(dt.datetime.now()),log_type='others',bot=b.login,proxy=b.proxy,request='Добавление предмета'+i[4],response='sucsess')
            except:
                pass
                # Logs.objects.create(time=str(dt.datetime.now()),log_type='others',bot=b.login,proxy=b.proxy,request='Добавление предмета'+i[4],response='Предмет уже существует')
        Logs.objects.create(time=str(dt.datetime.now()),log_type='others',bot=b.login,proxy=b.proxy,request='Google Parsing '+ b.login +'('+str(k)+')',response='sucsess')

    print('This is my first task')


#
# @shared_task
# def add(x, y):
#     return x + y
#
#
# @shared_task
# def mul(x, y):
#     return x * y
#
#
# @shared_task
# def xsum(numbers):
#     return sum(numbers)
#
#
# @shared_task
# def count_widgets():
#     return Items.objects.count()
#
#
# @shared_task
# def rename_widget(widget_id, name):
#     w = Items.objects.get(id=widget_id)
#     w.name = name
#     w.save()
