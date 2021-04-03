from django.shortcuts import render,redirect
from django.template import Context, Template
from django.contrib.auth import logout
from rest_framework import viewsets
from rest_framework import permissions
from main.serializers import BotsSerializer,BotsShowSerializer
from .models import Bots,Logs,Item
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
#import sys
import json


import httplib2 
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials




# Ready class

# import steam.client
import logging
#import aiohttp
import datetime as dt

from aiohttp_socks import ProxyConnector, ProxyType, ProxyError


import datetime as dt
from asgiref.sync import async_to_sync


# from gevent import monkey
# monkey.patch_all(thread=False, select=False,ssl=False)

#from gevent import monkey as curious_george
#curious_george.patch_all(thread=False, select=False,ssl=False)
#import requests
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

        self.http._session = aiohttp.ClientSession(connector=proxy_connector)
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


def logs(request):
    if request.user.is_authenticated:
        logs = Logs.objects.all()
        context={
            'logs':logs
        }
        return render(request,'main/logs.html',context=context)
    else:
        return redirect('login',)

def items(request):
    if request.user.is_authenticated:
        items = Item.objects.all()
        context={
            'items':items
        }
        return render(request,'main/items.html',context=context)
    else:
        return redirect('login',)

def logouto(request):
    logout(request)
    return redirect('main')



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
        client = SteamClient(
            proxy_info=bot_data.get("proxy"),
#            database=self.database
        )
        async_to_sync(client.login(
            bot_data.get("login"),
            bot_data.get("password"),
            shared_secret=bot_data.get("shared_secret"),
            identity_secret=bot_data.get("indentity_secret")
        ))
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

def bot_off(request):
    pass

#import sys
#sys.setrecursionlimit(200)
@csrf_exempt
def save(request):
    if request.method == "POST":
        text = request.POST.get("edit")
        try:
            texto = text.split(']\r\n[')
        except:
            print('only one')
            return redirect('main',)
        print(texto)
        items = []

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
                    CREDENTIALS_FILE = 'main/by David-a6013fe2ec30.json'  # имя файла с закрытым ключом
                    spreadsheets_id= googleDriveId  #'1XIfaox14sadvI2CWXPJ29pTgbDsHdZr8a0dBD8jfHhc'

                    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                                                                      'https://www.googleapis.com/auth/drive'])
                    httpAuth = credentials.authorize(httplib2.Http())
                    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)


                    values = service.spreadsheets().values().get(
                        spreadsheetId=spreadsheets_id,
                        range='A:H',
                        majorDimension='ROWS'
                    ).execute()
                    for i in values.get("values")[1::]:
                        print(JSON_object.get(i[0]))
                        try:

                            Item.objects.create(bot=login,name=i[0],drive_price=i[1],d_time=str(dt.datetime.now()),hold_off=i[3],status='New',assedID=i[4],d_discount=i[2],s_time=steam_time,steam=str(JSON_object.get(i[0])))
                            Logs.objects.create(time=str(dt.datetime.now()),log_type=log_type,bot=login,proxy=proxy,request='Добавление предмета'+i[4],response=response)
                        except:
                            Logs.objects.create(time=str(dt.datetime.now()),log_type=log_type,bot=login,proxy=proxy,request='Добавление предмета'+i[4],response='Предмет уже существует')
            items.append(steamid)
            todel = Bots.objects.all().exclude(steamid__in=items)
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
