from django.shortcuts import render,redirect
from django.template import Context, Template
from django.contrib.auth import logout
from main.serializers import BotsSerializer,BotsShowSerializer
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import viewsets
from rest_framework import permissions

from .models import Bots,Logs,Item,Profit


#import sys
import json


import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials



#import steam.client

# Ready class

#import steam.client
import logging
#import aiohttp
import datetime as dt

from aiohttp_socks import ProxyConnector, ProxyType, ProxyError

# import apiclient
import datetime as dt
from asgiref.sync import async_to_sync


#from gevent import monkey
#monkey.patch_all(thread=False, select=False,ssl=False)

#from gevent import monkey as curious_george
#curious_george.patch_all(thread=False, select=False,ssl=False)
import requests
import urllib.request


def resolve_proxy(proxy_string):
    host, port, login, password = proxy_string.split(':')
    return host, int(port), login, password


class SteamClient():

    def __init__(self, *args, database=None, proxy_info=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxy_info = proxy_info
#        self.database = database
        self.is_connected = False

    def __eq__(self, other):
        return self.login == other.login

    async def on_connect(self):
        self.is_connected = True

        await self.database.logs.insert_one({
            "date": dt.datetime.now(),
            "type": "steam",
            "login": self.username,
            "proxy": self.proxy_info,
            "request": "login",
            "response": "Success"
        })

    async def on_disconnect(self):
        self.is_connected = False

        await self.database.logs.insert_one({
            "date": dt.datetime.now(),
            "type": "steam",
            "login": self.username,
            "proxy": self.proxy_info,
            "request": "logout",
            "response": "Success"
        })

    async def on_error(self, event: str, error: Exception, *args, **kwargs):
        await self.log_error(event, error, *args, **kwargs)

    async def on_ready(self):
        logging.info(f"{self.user.name} started!")

    async def close(self, *args, **kwargs):
        await super().close(*args, **kwargs)

    async def login(self, *args, **kwargs):
        if self.http._session is not None:
            await self.http._session.close()

        if self.proxy_info:
            try:
                host, port, login, password = resolve_proxy(self.proxy_info)
            except Exception:
                raise ProxyError("Invalid proxy")

            proxy_connector = ProxyConnector(
                proxy_type=ProxyType.SOCKS5,
                host=host,
                port=port,
                username=login,
                password=password,
                rdns=True
            )
        else:
            proxy_connector = None

#        self.http._session = aiohttp.ClientSession(connector=proxy_connector)
        await super().login(*args, **kwargs)

    async def log_error(self, event, error: Exception, *args, **kwargs):
        await self.database.logs.insert_one({
            "date": dt.datetime.now(),
            "type": "steam",
            "login": self.username,
            "proxy": self.proxy_info,
            "request": event,
            "response": str(error)
        })






# Ready class





# Create your views here.
def main(request):
    if request.user.is_authenticated:
        bots = Bots.objects.all()
        context={
            'bots':bots
        }
        return render(request,'main/index1.html',context=context)
    else:
        return redirect('login',)
def login(request):
    return render(request,'main/login.html')

from django.db.models import Q

@csrf_exempt
def logs(request):
    if request.user.is_authenticated:
        logs = Logs.objects.all()
        bots = Bots.objects.all()
        print(request.GET)
        if request.method == "GET":
            try:
                if request.GET['first'] == 'all':
                    if request.GET['third'] == 'all':
                        k = Logs.objects.all()
                    else:
                        k = Logs.objects.filter(log_type = request.GET['third'])

                elif request.GET['first'] == 'bots':
                    if request.GET['third'] == 'all':
                        k = Logs.objects.all().exclude(bot='')
                    else:
                        k = Logs.objects.filter(log_type = request.GET['third']).exclude(bot='')
                elif request.GET['first'] == 'others':
                    if request.GET['third'] == 'all':
                        k = Logs.objects.filter(bot='')
                    else:
                        k.objects.filter(bot='',log_type = request.GET['third'])
                print(logs)
            except Exception as e:
                print(e)
                
                k = Logs.objects.all()
        
        try:
            paginator = Paginator(k.order_by('-pk'), int(request.GET['num']))
        except:
            paginator = Paginator(k.order_by('-pk'), 100)  # 3 поста на каждой странице
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # Если страница не является целым числом, поставим первую страницу
            posts = paginator.page(1)
        except EmptyPage:
            # Если страница больше максимальной, доставить последнюю страницу результатов
            posts = paginator.page(paginator.num_pages)
        context={
            'logs':logs,
            'bots':bots,
            'page': page,
		    'posts': posts,
            
        }
        return render(request,'main/logs.html',context=context)
    else:
        return redirect('login',)

def logs_for(request,login):
    if request.user.is_authenticated:
        logs = Logs.objects.filter(bot=login)
        bots = Bots.objects.all()
        print(request.POST)
        if request.method == "GET":
            try:
                if request.GET['first'] == 'all':
                    if request.GET['third'] == 'all':
                        logs = Logs.objects.filter(bot=login)
                    else:
                        logs = Logs.objects.filter(bot=login,log_type = request.GET['third'])

                elif request.GET['first'] == 'bots':
                    if request.GET['third'] == 'all':
                        logs = Logs.objects.all().exclude(bot=login)
                    else:
                        Logs.objects.filter(log_type = request.GET['third']).exclude(bot=login)
                elif request.GET['first'] == 'others':
                    logs = Logs.objects.filter(bot='')
                    if request.GET['third'] == 'all':
                        logs = Logs.objects.filter(bot='')
                    else:
                        Logs.objects.filter(bot='',log_type = request.GET['third'])
            except Exception as e:
                print(e)
        try:
            paginator = Paginator(logs.order_by('-pk'), int(request.GET['num']))
        except:
            paginator = Paginator(logs.order_by('-pk'), 100) # 3 поста на каждой странице
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # Если страница не является целым числом, поставим первую страницу
            posts = paginator.page(1)
        except EmptyPage:
            # Если страница больше максимальной, доставить последнюю страницу результатов
            posts = paginator.page(paginator.num_pages)
        context={
            'logs':logs,
            'bots':bots,
            'page': page,
		    'posts': posts,
            'main':main,
            'login':login
        }
        return render(request,'main/logs_for.html',context=context)
    else:
        return redirect('login',)


def items_for(request,login):
    items = Item.objects.filter(bot=login)
    bots = Bots.objects.all()
    j = Item.objects.all()
    print(request.POST)
    if request.method == "GET":
        try:
            if request.GET['daterange'] != '0':
                print('asdasd')
                a = request.GET['daterange'].split(' - ')[0].split('/')
                print(int(a[2]),int(a[0]),int(a[1]))
                a1 = date(int(a[2]),int(a[0]),int(a[1]))
                b = request.GET['daterange'].split(' - ')[1].split('/')
                b1 = date(int(b[2]),int(b[0]),int(b[1]))
                z = items.filter(hold_off__range=[a1,b1])
                print(z)
            else:
                z = items
            if request.GET['daterange1'] != '0':
                a = request.GET['daterange1'].split(' - ')[0].split('/')
                a1 = date(int(a[2]),int(a[0]),int(a[1]))
                b = request.GET['daterange1'].split(' - ')[1].split('/')
                b1 = date(int(b[2]),int(b[0]),int(b[1]))
                g = z.filter(hold_off__range=[a1,b1])
            else:
                g = z
            print(request.GET)
            if request.GET['radio'] == '1':
                p = g
            elif request.GET['radio'] == '2':
                p = g.filter(place='Drive')
            elif request.GET['radio'] == '3':
                p = g.filter(place='WrongName')
            elif request.GET['radio'] == '4':
                p = g.filter(place='NotDetermined')
            if request.GET['radio1'] == '1':
                o = p
            elif request.GET['radio1'] == '2':
                o = p.filter(status='New')
            elif request.GET['radio1'] == '3':
                o = p.filter(place='NotAtInventory')
            if request.GET['radio2'] == '1':
                j = o
            elif request.GET['radio2'] == '2':
                j = o
            elif request.GET['radio2'] == '3':
                j = o
        except Exception as e:
            print(e)
            j = Item.objects.all()
#            if request.POST['radio'][] == 'others':
#                logs = Logs.objects.filter(bot='')
#                if request.POST['third'] == 'all':
#                    logs = Logs.objects.filter(bot='')
#                else:
#                    Logs.objects.filter(bot='',log_type = request.POST['third'])
#        else:
#            j = Item.objects.all()
        try:
            paginator = Paginator(j.order_by('-pk'), int(request.GET['num']))
        except:
            paginator = Paginator(j.order_by('-pk'), 100)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # Если страница не является целым числом, поставим первую страницу
            posts = paginator.page(1)
        except EmptyPage:
            # Если страница больше максимальной, доставить последнюю страницу результатов
            posts = paginator.page(paginator.num_pages)
        drive_c = len(Item.objects.filter(place='Drive'))
        wrongname_c = len(Item.objects.filter(place='WrongName'))
        notdetermined_c = len(Item.objects.filter(place='NotDetermined'))
        status_new = len(Item.objects.filter(status='New'))
        status_notat = len(Item.objects.filter(status='NotAtInventory'))
        hold_at = 0
        all_ = len(items)
        hold_not = len(items)
        context={
            'items':items,
            'bots':bots,
            'page': page,
		    'posts': posts,
            'main':main,
            'drive_c':drive_c,
        'wrongname_c':wrongname_c,
        'notdetermined_c':notdetermined_c,
        'status_new':status_new,
        'status_notat':status_new,
        'all_':all_,
        'hold_not':hold_not,
            'login':login
        }
        return render(request,'main/items_for.html',context=context)
    else:
        return redirect('login',)

from datetime import date
@csrf_exempt
def items(request):
    if request.user.is_authenticated:
        items = Item.objects.all()
        bots = Bots.objects.all()
        drive_c = len(Item.objects.filter(place='Drive'))
        wrongname_c = len(Item.objects.filter(place='WrongName'))
        notdetermined_c = len(Item.objects.filter(place='NotDetermined'))
        status_new = len(Item.objects.filter(status='New'))
        status_notat = len(Item.objects.filter(status='NotAtInventory'))
        hold_at = 0
        all_ = len(items)
        hold_not = len(items)
        
        j = Item.objects.all()
        print(request.POST)
        if request.method == "GET":
            try:
                if request.GET['daterange'] != '0':
                    print('asdasd')
                    a = request.GET['daterange'].split(' - ')[0].split('/')
                    print(int(a[2]),int(a[0]),int(a[1]))

                    a1 = date(int(a[2]),int(a[0]),int(a[1]))
                    b = request.GET['daterange'].split(' - ')[1].split('/')
                    b1 = date(int(b[2]),int(b[0]),int(b[1]))
                    z = items.filter(hold_off__range=[a1,b1])
                    print(z)
                else:
                    z = items
                if request.GET['daterange1'] != '0':
                    a = request.GET['daterange1'].split(' - ')[0].split('/')
                    a1 = date(int(a[2]),int(a[0]),int(a[1]))
                    b = request.GET['daterange1'].split(' - ')[1].split('/')
                    b1 = date(int(b[2]),int(b[0]),int(b[1]))
                    g = z.filter(hold_off__range=[a1,b1])
                else:
                    g = z
                print(request.GET)
                if request.GET['radio'] == '1':
                    p = g
                elif request.GET['radio'] == '2':
                    p = g.filter(place='Drive')
                elif request.GET['radio'] == '3':
                    p = g.filter(place='WrongName')
                elif request.GET['radio'] == '4':
                    p = g.filter(place='NotDetermined')

                if request.GET['radio1'] == '1':
                    o = p
                elif request.GET['radio1'] == '2':
                    o = p.filter(status='New')
                elif request.GET['radio1'] == '3':
                    o = p.filter(place='NotAtInventory')

                if request.GET['radio2'] == '1':
                    j = o
                elif request.GET['radio2'] == '2':
                    j = o
                elif request.GET['radio2'] == '3':
                    j = o
            except:
                j = Item.objects.all()
#            if request.POST['radio'][] == 'others':
#                logs = Logs.objects.filter(bot='')
#                if request.POST['third'] == 'all':
#                    logs = Logs.objects.filter(bot='')
#                else:
#                    Logs.objects.filter(bot='',log_type = request.POST['third'])
        else:
            j = Item.objects.all()
        try:
            paginator = Paginator(j.order_by('-pk'), int(request.GET['num']))
        except:
            paginator = Paginator(j.order_by('-pk'), 100) # 3 поста на каждой странице    
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # Если страница не является целым числом, поставим первую страницу
            posts = paginator.page(1)
        except EmptyPage:
            # Если страница больше максимальной, доставить последнюю страницу результатов
            posts = paginator.page(paginator.num_pages)
        context={
            'items':j,
            'bots':bots,
            'page': page,
		    'posts': posts,       
            'drive_c':drive_c,
        'wrongname_c':wrongname_c,
        'notdetermined_c':notdetermined_c,
        'status_new':status_new,
        'status_notat':status_new,
        'all_':all_,
        'hold_not':hold_not,
        }
        return render(request,'main/items.html',context=context)
    else:
        return redirect('login',)

def settings(request):
    try:
        profit = Profit.objects.get(pk=1)
        min_p = profit.min_p
        max_p = profit.max_p
    except Exception as e:
        min_p = 100
        max_p = 100
    context={
        'min_p' : min_p,
        'max_p' : max_p,
    }
    return render(request,'main/setting.html',context=context)

@csrf_exempt
def settingsave(request):
    if request.method == "POST":
        try:
            profit = Profit.objects.get(pk=1)
            profit.min_p = int(request.POST.get('min_p'))
            profit.max_p = int(request.POST.get('max_p'))
            profit.save()
            print('find')
        except Exception as e:
            ac= Profit.objects.create(min_p = int(request.POST.get('min_p')),max_p = int(request.POST.get('max_p')))
            print(int(ac.min_p),int(request.POST.get('max_p')),e,ac.pk)
            ac.save()

    return redirect('setting',)
def logouto(request):
    logout(request)
    return redirect('main')

import asyncio
loop = asyncio.get_event_loop()

def bot_on(request,login):
    instance = Bots.objects.get(login=login)
    bot_data = {
        'login':login,
        'password':instance.password,
        'shared_secret':instance.shared_secret,
        'proxy':instance.proxy,
        'indentity_secret': ''
    }
    try:
#        client = SteamClient(proxy_info=bot_data.get("proxy"))
#        
#        loop.run_until_complete(client.login(
#            bot_data.get("login"),
#            bot_data.get("password"),
#            shared_secret=bot_data.get("shared_secret"),
#            identity_secret=bot_data.get("indentity_secret")
#        ))
        donotcache = 146845136
        password = instance.password
        username = login
        rsatimestamp = '64000000'
        url = 'https://steamcommunity.com/login/'
        dann = {'donotcache': donotcache,
                    'password': password,
                    'username': username,
                    'emailaut': '',
                    'loginfriendlyname': '',
                    'captchagid': '-1',
                    'captcha_text': '',
                    'emailsteamid': '',
                    'rsatimestamp': rsatimestamp,
                    'remember_login': 'true'
                }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
            'ACCEPT' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'ACCEPT-ENCODING' : 'gzip, deflate, br',
            'ACCEPT-LANGUAGE' : 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'REFERER' : 'https://www.google.com/'
        }    
        s = requests.Session()
        proxies = {'https': 'http://%s:%s'%(instance.proxy.split(':')[0],instance.proxy.split(':')[1].replace(']','')) }
        r = s.post(url, dann, verify=True,proxies=proxies,headers = headers)  # >тправка пост запроса)
        print(r.url)
        result = r.text
        print(r.text)
        
        log_type = "steam"
        response = "sucsess"
    except ProxyError as e:
        log_type = "proxy"
        response = f"{e.__class__.__name__} {str(e)}"
    except Exception as e:
        print(e)
        if "rsa" in str(e).lower():
            log_type = "proxy"
        else:
            log_type = "steam"

        response = f"{e.__class__.__name__} {str(e)}"

        if hasattr(e, "response") and e.response:
            response += f" { e.response.text()}"

        if hasattr(e, "message") and e.message:
            response += f" {e.message}"
    dollar = 75.7023
    
    steam = urllib.request.urlopen('https://api.steamapis.com/market/items/730?api_key=bmyRVmF1HOQ9IH5LmSInrD8FgV4&format=comact').read().decode('UTF-8')
    steam_time = str(dt.datetime.now())
#        encoding=steam.info().get_content_charset('utf-8')
    JSON_object = json.loads(steam)
    search = Bots.objects.get(login=login)
    googleDriveId = search.googleDriveId 
    proxy = search.proxy
            
    CREDENTIALS_FILE = 'main/by David-a6013fe2ec30.json'  # имя файла с закрытым ключом
    spreadsheets_id= googleDriveId  #'1XIfaox14sadvI2CWXPJ29pTgbDsHdZr8a0dBD8jfHhc'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                                                                      'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)

    try:
        values = service.spreadsheets().values().get(
             spreadsheetId=spreadsheets_id,
             range='A:H',
             majorDimension='ROWS'
         ).execute()
        z=0
        for i in values.get("values")[1::]:
            print(JSON_object.get(i[0]))
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
                stp = str(JSON_object.get(i[0])) + ' (' + str(JSON_object.get(i[0])*dollar) + ')'
                           
                Item.objects.create(
                     bot=login,
                     name=i[0],
                     drive_price=i[1],
                     hold_off=i[3],
                     status='',
                     assedID=i[4],
                     d_discount=i[2],
                     s_time=steam_time,
                     steam=stp,
                     min_profit=min_p,
                     max_profit=max_p,
                     min_time=time_p,
                     max_time=time_p)
                           
                z+=1
            except Exception as e:
                print(e)
                Logs.objects.create(time=str(dt.datetime.now()),log_type=log_type,bot=login,proxy=proxy,request='parsing Google ID '+login,response='Ошибка. id предмета: '+i[4])
                            
        Logs.objects.create(time=str(dt.datetime.now()),log_type=log_type,bot=login,proxy=proxy,request='parsing Google ID'+str(z),response='sucsess')
    except Exception as e:
         print(e)
   
    Logs.objects.create(time=str(dt.datetime.now()),log_type=log_type,bot=bot_data.get("login"),proxy=instance.proxy,request='login',response=response)
    
    instance.turn = True
    instance.save()
    return JsonResponse({
        "date": dt.datetime.now(),
        "type": log_type,
        "login": bot_data["login"],
        "proxy": bot_data.get("proxy"),
        "request": "login",
        "response": response
    })




def bot_off(request,login):
    instance = Bots.objects.get(login=login)
    bot_data = {
        'login':login,
        'password':instance.password,
        'shared_secret':instance.shared_secret,
        'proxy':instance.proxy,
        'indentity_secret': ''
    }
    try:
        client = SteamClient(
            proxy_info=bot_data.get("proxy"),
#            database=self.database
        )
        client.close(
            bot_data.get("login"),
            bot_data.get("password"),
            shared_secret=bot_data.get("shared_secret"),
            identity_secret=bot_data.get("indentity_secret")
        )
        log_type = "steam"
        response = "sucsess"
#    except ProxyError as e:
#        log_type = "proxy"
#        response = f"{e.__class__.__name__} {str(e)}"
    except Exception as e:
        if "rsa" in str(e).lower():
            log_type = "proxy"
        else:
            log_type = "steam"

        response = f"{e.__class__.__name__} {str(e)}"

        if hasattr(e, "response") and e.response:
            response += f" { e.response.text()}"

        if hasattr(e, "message") and e.message:
            response += f" {e.message}"
    Logs.objects.create(time=str(dt.datetime.now()),log_type=log_type,bot=bot_data.get("login"),proxy=instance.proxy,request='logout',response=response)
    
    instance.turn = False
    instance.save()
    return JsonResponse({
        "date": dt.datetime.now(),
        "type": log_type,
        "login": bot_data["login"],
        "proxy": bot_data.get("proxy"),
        "request": "login",
        "response": response
    })

#import sys
#sys.setrecursionlimit(200)
@csrf_exempt
def save(request):
    dollar = 75.7023
    if request.method == "POST":
        text = request.POST.get("edit")
        try:
            texto = text.split(']\r\n[')
        except:
            print('only one')
            return redirect('main',)
        print(texto)
        items = []
        if texto == ['']:
            a = Bots.objects.all()
            l = Logs.objects.all()
            i = Item.objects.all()
            l.delete()
            i.delete()
            a.delete()
            return redirect('main',)
        steam = urllib.request.urlopen('https://api.steamapis.com/market/items/730?api_key=bmyRVmF1HOQ9IH5LmSInrD8FgV4&format=comact').read().decode('UTF-8')
#        encoding=steam.info().get_content_charset('utf-8')
        JSON_object = json.loads(steam)

        steam_time = str(dt.datetime.now())
#        for i in grequests.map(steam):
#        print(json.loads(steam.read()))
        print('----------------------------------aaaaaaaaaaaaaaaaaaaaaaaaaaaaa--------------------------')
        for i in texto:
            k =  i.replace('"]\r\n','').split('","')
            print(k)
            comment = k[0].split('":"')[1]
            print()
            login = k[1].split('":"')[1]
            password = k[2].split('":"')[1]
            steamid = k[3].split('":"')[1]
            shared_secret=k[4].split('":"')[1]
            steamAPI=k[5].split('":"')[1]
            googleDriveId=k[6].split('":"')[1]
            proxy=k[7].split('":"')[1].replace('"','')
            try:
                Bots.objects.get(comment=comment,login=login,password=password,steamid=steamid,steamAPI=steamAPI,shared_secret=shared_secret,googleDriveId=googleDriveId,proxy=proxy)
            except:
                print('Аккаунт не существует либо изменен')
                try:
                    search = Bots.objects.get(steamid=steamid)
                    search.comment = comment
                    search.login = login
                    search.password = password
                    search.steamid = steamid
                    search.shared_secret = shared_secret
                    search.steamAPI = steamAPI
                    search.googleDriveId = googleDriveId
                    search.comment = comment
                    search.proxy = proxy
                    search.save()
                    log_type = 'others'
                    request = 'Изменение Аккаунта:'+login
                    response = 'sucsess'
                    Logs.objects.create(time=str(dt.datetime.now()),log_type=log_type,bot=login,proxy=proxy,request=request,response=response)
                except Exception as e:
                    print(e)
                    print('Аккаунта не существует, надо добавить')
                    Bots.objects.create(comment=comment,login=login,password=password,steamid=steamid,steamAPI=steamAPI,shared_secret=shared_secret,googleDriveId=googleDriveId,proxy=proxy)
                    log_type = 'others'
                    request = 'Добавление Аккаунта:'+login
                    response = 'sucsess'
                    Logs.objects.create(time=str(dt.datetime.now()),log_type=log_type,bot=login,proxy=proxy,request=request,response=response)
#                    CREDENTIALS_FILE = 'main/by David-a6013fe2ec30.json'  # имя файла с закрытым ключом
#                    spreadsheets_id= googleDriveId  #'1XIfaox14sadvI2CWXPJ29pTgbDsHdZr8a0dBD8jfHhc'
#
#                    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
#                                                                                                      'https://www.googleapis.com/auth/drive'])
#                    httpAuth = credentials.authorize(httplib2.Http())
#                    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
#
#                    try:
#                        values = service.spreadsheets().values().get(
#                            spreadsheetId=spreadsheets_id,
#                            range='A:H',
#                            majorDimension='ROWS'
#                        ).execute()
#                        z=0
#                        for i in values.get("values")[1::]:
#                            print(JSON_object.get(i[0]))
#                            try:
#                                try:
#                                    min_p = str(Profit.objects.get(pk=1).min_p)
#                                    max_p = str(Profit.objects.get(pk=1).max_p)
#                                    time_p = str(Profit.objects.get(pk=1).time)
#                                except:
#                                    p = Profit.objects.create(min_p=100,max_p=100)
#                                    min_p = str(100)
#                                    max_p = str(100)
#                                    time_p = str(p.time)
#                                stp = str(JSON_object.get(i[0])) + ' (' + str(JSON_object.get(i[0])*dollar) + ')'
#                                          
#                                Item.objects.create(
#                                    bot=login,
#                                    name=i[0],
#                                    drive_price=i[1],
#                                    hold_off=i[3],
#                                    status='',
#                                    assedID=i[4],
#                                    d_discount=i[2],
#                                    s_time=steam_time,
#                                    steam=stp,
#                                    min_profit=min_p,
#                                    max_profit=max_p,
#                                    min_time=time_p,
#                                    max_time=time_p)
#                                          
#                                z+=1
#                            except Exception as e:
#                                print(e)
#                                Logs.objects.create(time=str(dt.datetime.now()),log_type=log_type,bot=login,proxy=proxy,request='parsing Google drive ID '+login,response='Ошибка. id предмета: '+i[4])
#                                
#                        Logs.objects.create(time=str(dt.datetime.now()),log_type=log_type,bot=login,proxy=proxy,request='Добавление предметов  '+str(z),response=response)
#                    except Exception as e:
#                        print(e)
            items.append(steamid)
            todel = Bots.objects.all().exclude(steamid__in=items)
            print(todel)
            for i in todel:
                a = Item.objects.filter(bot = i.login)
                print(a)
                a.delete()
                
                y = Logs.objects.filter(bot = i.login)
                y.delete()
                print(y)
            todel.delete()



        return redirect('main',)
#        return HttpResponse("<h2>Hello, {0}</h2>".format(text))
    else:
        return HttpResponse("<h2>Hello, </h2>")





class BotsViewSet(viewsets.ModelViewSet):
    queryset = Bots.objects.all()
    serializer_class = BotsSerializer
    permission_classes = [permissions.IsAuthenticated]

class BotsShowViewSet(viewsets.ModelViewSet):
    queryset = Bots.objects.all()
    serializer_class = BotsShowSerializer
    permission_classes = [permissions.IsAuthenticated]

    
    
    
    
    
    
    
    
#    
#["comments":"test1","login":"111111","pass":"Ujr7H3df","steamID":"76561199043442138","shared_secret":"Uoe44hHfd=","steamAPI":"UjdvejNved","googleDriveId":"1rWaPUriTjreYKvfC5MHjpDpLa_b8plm8QYjT3sekcLc","proxy":"192.123.23.123:3643:Gheyhf:gGrcje3f"]
#["comments":"testdfg1","login":"1111512411","pass":"Ujr7H3df","steamID":"76561199043124212442138","shared_secret":"Uoe4dfgdfg4hHfd=","steamAPI":"UjdvejNved","googleDriveId":"1rWaPUriTj12412421421reYKvfC5MHjpDpLa_b8plm8QYjT3sekcLc","proxy":"192.123.23.123"]
