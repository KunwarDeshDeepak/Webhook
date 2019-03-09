from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from handler.models import Webhook, SasSActions,SasSSheetMap,JiraSetup, User, AccessToken
from rest_framework.utils import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import gspread
import requests
from oauth2client import client
import uuid
import time
import pandas as pd
import io


def sheets_handler(request):#request will receive the id of the file
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    gauth = GoogleAuth()#whe can update the scope of the gauth as well.

    # Try to load saved client credentials
    try:
        #get the spread_sheet id , from there get the user and then get the aceess token of the particular user.
        access_token = AccessToken.objects.get(pk=1)#Request will specify which user it is asking for
        gauth.credentials = client.Credentials.new_from_json(access_token.token)

    except ObjectDoesNotExist:
        print('No access token Found')

    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()

    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()

    drive = GoogleDrive(gauth)
    print(AccessToken.objects.filter(token=gauth.credentials.to_json()).exists())
    if not AccessToken.objects.filter(token=gauth.credentials.to_json()).exists():
        token_obj = AccessToken(user = User.objects.get(pk=1),token=gauth.credentials.to_json())  # user is made as null = True
        token_obj.save()

    sheet_client = gspread.authorize(gauth.credentials)

    title_list = []
    print("Choose from the List of SpreadSheets")
    for sheet in sheet_client.openall():
        print(sheet.title, sheet.id)
        create_channel(gauth.credentials.access_token,sheet.id)
        title_list.append(sheet.id)



def create_channel(access_token,sheet_id):
    uuid_str = str(uuid.uuid4())
    expiration_time = int(time.time())+86300

    body_data = {

        "id": uuid_str,
        "type": "web_hook",
        "address": "https://kddeepak.pythonanywhere.com/webhook/",
        "expiration": expiration_time

    }
    headers = {
        'Authorization': 'Bearer '+access_token
        , 'Accept': 'application/json'

        }

    URL ='https://www.googleapis.com/drive/v3/files/'+sheet_id+'/watch'
    r = requests.post(URL,data=body_data, headers=headers)



@csrf_exempt
@api_view(['POST'])
def get_changes(request):
    resource_uri = request.META['HTTP_X-GOOG-RESOURCE-URI']

    str = resource_uri[42:]
    file_id = ''
    for i in str:

        if i=='?':
            break
        file_id = file_id + i


    # we will retrieve the user and then the google Access - token of the user from this file_id


    REVISION_URL = 'https://www.googleapis.com/drive/v2/files/'+file_id+'/revisions?fields=items(exportLinks%2Cid)'

    # if the token is not valid then do refresh the token.

    headers = {
        'Authorization': 'Bearer ' + access_token #this access token will be accessed from the database
        , 'Accept': 'application/json'

    }

    r = requests.get(REVISION_URL,headers=headers)

    data = r.json()
    l = len(data['items'])
    latest_update = int(data['items'][l-1]['id'])#fetching the latest update id for this file
    export_link_prev = 'https://docs.google.com/spreadsheets/export?id='+file_id+'&revision='+str(latest_update-1)+'&exportFormat=csv'
    export_link_latest = 'https://docs.google.com/spreadsheets/export?id='+file_id+'&revision='+str(latest_update)+'&exportFormat=csv'

    spreadsheet_data_prev = requests.get(export_link_prev, headers=headers)
    spreadsheet_data_latest = requests.get(export_link_latest, headers=headers)

    df1 = pd.read_csv(io.BytesIO(spreadsheet_data_prev), encoding='utf8')
    df2 = pd.read_csv(io.BytesIO(spreadsheet_data_latest), encoding='utf8')


    # print(df1.ix[1])

    #returning the response
    hook = Webhook(data="Chal gaya code")
    hook.save()
    return Response(status=200, data={'msg': "This is done"})


@api_view(['GET'])
def get_changes_show(request):
    return Response(status=200, data={'msg': "This is made for post requests"})


def show_html(request):
    return HttpResponse("google-site-verification: googlea73117b61cc11fc2.html")


