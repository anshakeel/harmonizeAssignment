from django.shortcuts import render
import requests
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from django.core.cache import cache
from .parser import wether_report

#-_-_-Creating Sepearte class Based API Functions for Both Functionalities-_-_-
#-_-_-We can also create a Single API for Both functionalities-_-_-


# API endpoint responsbile for pong response
class pingAPI(APIView):
    def get(self, request):
        jsonOutput=json.dumps({"data":"pong"})
        return HttpResponse (jsonOutput , status=status.HTTP_200_OK)

#API endpoint responsbile for Fetching, Parsing and Retruning Wether Response
class WetherInfo(APIView):
    def get(self, request):
        jsonResponse = {"data": ""}
        scode = request.query_params.get("scode")
        nocache = request.query_params.get("nocache")
        if scode is not None:          
            scode = scode.upper()
            if nocache is None:
                nocache=1
            if cache.get(scode) and int(nocache)!=1:
                jsonResponse['data']=cache.get(scode)
            else:              
                data = requests.get(f'https://tgftp.nws.noaa.gov/data/observations/metar/stations/{scode}.TXT')
                #Parsing Wether Data
                response =wether_report(data.text)
                #Converting the String into JSON
                jsonResponse['data']=response               
                if(nocache==1): 
                    cache.clear()
                cache.set(scode,jsonResponse['data'])
            jsonResponse = json.dumps(jsonResponse)           
            return HttpResponse(jsonResponse , status=status.HTTP_200_OK)
        else:
            return HttpResponse("Please Enter SCODE in URL to get Wether Report", status=status.HTTP_404_NOT_FOUND)

    
class HomeAPI(APIView):
    def get(self, request):
        return HttpResponse("HOME PAGE")