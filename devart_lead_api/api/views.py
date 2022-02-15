from datetime import date, datetime, time, timedelta
from email import header
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async, async_to_sync
from django.http import HttpResponse
from time import sleep
import httpx
import asyncio
from django.utils import timezone
from django.shortcuts import get_object_or_404
import json
import requests
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from api.serializers import SourceSerializer, KeySerializer, LeadSerializer
from rest_framework import permissions
from rest_framework import viewsets
from api.models import Source, Key, Lead, Request, Offer
from django.http import Http404, HttpResponse
from django.http import Http404
from unittest import result
import http
from channels.db import database_sync_to_async
import pytz
import os
import environ
import random

env = environ.Env()
environ.Env.read_env()


class SourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = [permissions.IsAuthenticated]


class KeyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Key.objects.all()
    serializer_class = KeySerializer
    permission_classes = [permissions.IsAuthenticated]


class LeadViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]


async def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


async def check_ispis(rodne_cislo):

    # used to check katastr nemovitostí
    flip = random.randint(0, 1)
    return True if flip == 0 else False
    mydata = {"username": str(os.environ.get("ISPIS_USERNAME")),
              "password": str(os.environ.get("ISPIS_PASSWORD")),
              "profile": "OsobaCUZK",
              "RC": rodne_cislo}
    # 5804042343 - ma nemovitost
    # 0108271295 - nema nemovitost
    async with httpx.AsyncClient() as client:
        response = await client.post("https://ispis.cz/api/lustraceSearchSubject", data=mydata)
        if response.status_code == 200:
            # if request to ispis is ok, check if the subject has a building registered for himself
            print(response.text)
            if "Osoba NEMÁ nemovitosti" in response.text:
                return False
            elif "Osoba JE evidována" in response.text:
                return True
            else:
                return "Error with the response"

        else:
            return "Error connecting"


async def testStats(request, token):
    if request.method == "GET":
        source = await _get_source(str(token))
        if isinstance(source, bool):
            return HttpResponse("Wrong Token.")
        elif source.active is True:
            checked = 0
            accepted = 0
            data = await _get_offer_data_for_source(source)
            for offer in data:
                if offer.checked == True:
                    checked += 1
                if offer.accepted == True:
                    accepted += 1

            return HttpResponse(str(source) + " sent us  " + str(len(data)) + " leads this month <br> Out of which we checked: " + str(checked) + "<br> and successfully recieved: " + str(accepted))


@database_sync_to_async
def _get_offer_data_for_source(source):
    try:
        result = Offer.objects.filter(source=source)
        if result:
            return result
    except Offer.DoesNotExist:
        return False


@database_sync_to_async
def _get_lead(rc):
    try:
        result = Lead.objects.get(rodne_cislo=rc)
        if result:
            return result
    except Lead.DoesNotExist:
        return False


@database_sync_to_async
def _get_source(token):
    try:
        result = Key.objects.get(api_key=token)
        return result.source
    except Key.DoesNotExist:
        return False


@database_sync_to_async
def _new_request(ip, url, data, headers):
    new_request = Request()
    new_request.ip = ip
    new_request.url = url
    new_request.data = data
    new_request.headers = headers
    new_request.save()
    return new_request


@database_sync_to_async
def _new_lead(rc, is_owner, source):
    new_lead = Lead()
    new_lead.rodne_cislo = rc
    new_lead.is_owner = is_owner
    new_lead.source = source
    new_lead.save()
    return new_lead


@database_sync_to_async
def _new_offer(rc, source, checked=False, price=0.00, lead=None):
    new_offer = Offer()
    new_offer.rodne_cislo = rc
    new_offer.source = source
    new_offer.checked = checked
    new_offer.price = price
    new_offer.lead = lead
    new_offer.save()
    return new_offer


@database_sync_to_async
def _check_offer(lead, source):
    try:
        filterTime = datetime.now(pytz.utc) - timedelta(minutes=10)
        result = Offer.objects.filter(lead=lead).filter(
            source=source).filter(checked=True).filter(created_at__gte=filterTime)
        if result.exists():

            return result.first()
        return False
    except Offer.DoesNotExist:
        return False


@database_sync_to_async
def _edit_offer(lead):
    try:
        offer = Offer.objects.get(lead=lead)
        offer.accepted = True
        offer.save()
        return offer
    except Offer.DoesNotExist:
        return False


@database_sync_to_async
def _edit_lead(rc=None, source=None, bought=False, price=0.00, first_name=None, last_name=None, email=None, phone_number=None, addr_street=None, income=None, requested_amount=None, addr_city=None, addr_zip=None):
    try:
        lead = Lead.objects.get(rodne_cislo=rc)
        if source:
            lead.source = source
        lead.price = price
        if first_name:
            lead.first_name = first_name
        if last_name:
            lead.last_name = last_name
        if email:
            lead.email = email
        if phone_number:
            lead.phone_number = phone_number
        if bought:
            lead.bought = bought

        if income:
            lead.income = income

        if requested_amount:
            lead.requested_amount = requested_amount
        if addr_street:
            lead.addr_street = addr_street
        if addr_city:
            lead.addr_city = addr_city

        if addr_zip:
            lead.addr_zip = addr_zip
        lead.save()
        return lead
    except Lead.DoesNotExist:
        return False


@sync_to_async
@csrf_exempt
@async_to_sync
async def check(request):

    if request.method == "GET":
        return HttpResponse("This is a GET request")
    elif request.method == "POST":
        headers = request.headers
        body = request.body  # [1:-1].replace("\'", '\"')
        data = body.decode("utf-8")
        json_data = json.loads(data)
#
        rc = json_data["rodnecislo"]
        token = headers["token"]

        ip = await get_client_ip(request)
        url = request.path
        res = await _new_request(ip, url, data, headers)

        # find source based on token in DB
        source = await _get_source(token)
        if isinstance(source, bool):

            # Token not found
            response = JsonResponse({'status': 'wrong token'}, status=401)
            return response
        elif source.active is True:
            # Token found
            # Check our database first
            precheck = False
            found_lead = await _get_lead(rc)

            # LEAD FOUND, DISMISS!
            if not isinstance(found_lead, bool):
                print("dismiss it: " + str(found_lead.bought))

                offer = await _new_offer(rc, source)
                return JsonResponse({'status': 'duplicita'}, status=403)
            if isinstance(found_lead, bool):
                # LEAD NOT FOUND- BUY IT!
                print("BUy it!")
                ### Pause depending on the source of the lead ###
                if str(source) == "Leadx":
                    sleep(0)
                    if precheck == False:
                        ispis_check = await check_ispis(rc)
                    if precheck == True:
                        ispis_check = True  # prechecks our database
                    if isinstance(ispis_check, str):
                        if "Error" in ispis_check:
                            if "connecting" in ispis_check:
                                return JsonResponse({'status': 'ispis down'}, status=500)
                            if "response" in ispis_check:
                                return JsonResponse({'status': 'ispis response broken'}, status=500)
                    else:
                        if ispis_check is False:
                            # New Lead,  is_owner = False, dissmiss offer
                            new_lead = await _new_lead(rc, is_owner=False, source=source)
                            # new dismissed offer
                            offer = await _new_offer(rc, source)
                            return JsonResponse({'status': 'bez nemovitosti'}, status=403)
                        elif ispis_check is True:
                            # New Lead, is_owner = True, accept offer
                            new_lead = await _new_lead(rc, True, source)
                            # new accepted offer
                            offer = await _new_offer(rc, source, True, lead=new_lead)
                            return JsonResponse({'status': 'bereme'}, status=200)
                elif str(source) == "Volsor":
                    sleep(10)
                    found_lead = await _get_lead(rc)  # returns lead or False

                    if not isinstance(found_lead, bool):
                        # LEAD FOUND - dismissed
                        offer = await _new_offer(rc, source)
                        return JsonResponse({'status': 'duplicita'}, status=403)
                    if isinstance(found_lead, bool):
                        if precheck == False:
                            ispis_check = await check_ispis(rc)
                        if precheck == True:
                            ispis_check = True  # prechecks our database
                        if isinstance(ispis_check, str):
                            if "Error" in ispis_check:
                                if "connecting" in ispis_check:
                                    return JsonResponse({'status': 'ispis down'}, status=500)
                                if "response" in ispis_check:
                                    return JsonResponse({'status': 'ispis response broken'}, status=500)
                        else:
                            if ispis_check is False:
                                # New Lead,  is_owner = False, dissmiss offer
                                new_lead = await _new_lead(rc, is_owner=False, source=source)
                                # new dismissed offer
                                offer = await _new_offer(rc, source)
                                return JsonResponse({'status': 'bez nemovitosti'}, status=403)
                            elif ispis_check is True:
                                # New Lead, is_owner = True, accept offer
                                new_lead = await _new_lead(rc, True, source)
                                # new accepted offer
                                offer = await _new_offer(rc, source, True, lead=new_lead)
                                return JsonResponse({'status': 'bereme'}, status=200)

                elif str(source) == "Hyperia":
                    sleep(10)
                    found_lead = await _get_lead(rc)  # returns lead or False

                    if not isinstance(found_lead, bool):
                        # FOUND LEAD - dissmiss
                        offer = await _new_offer(rc, source)
                        return JsonResponse({'status': 'duplicita'}, status=403)
                    if isinstance(found_lead, bool):
                        if precheck == False:
                            ispis_check = await check_ispis(rc)
                        if precheck == True:
                            ispis_check = True  # prechecks our database
                        if isinstance(ispis_check, str):
                            if "Error" in ispis_check:
                                if "connecting" in ispis_check:
                                    return JsonResponse({'status': 'ispis down'}, status=500)
                                if "response" in ispis_check:
                                    return JsonResponse({'status': 'ispis response broken'}, status=500)
                        else:
                            if ispis_check is False:
                                # New Lead,  is_owner = False, dissmiss offer
                                new_lead = await _new_lead(rc, is_owner=False, source=source)
                                # new dismissed offer
                                offer = await _new_offer(rc, source)
                                return JsonResponse({'status': 'bez nemovitosti'}, status=403)
                            elif ispis_check is True:
                                # New Lead, is_owner = True, accept offer
                                new_lead = await _new_lead(rc, True, source)
                                # new accepted offer
                                offer = await _new_offer(rc, source, True, lead=new_lead)
                                return JsonResponse({'status': 'bereme'}, status=200)

                elif str(source) == "Leadsor":
                    sleep(5)
                    found_lead = await _get_lead(rc)  # returns lead or False

                    if not isinstance(found_lead, bool):
                        # LEAD FOUND - dismissed
                        if found_lead.bought == False:
                            found_lead = False
                        else:
                            offer = await _new_offer(rc, source)
                        return JsonResponse({'status': 'duplicita'}, status=403)
                    if isinstance(found_lead, bool):
                        if precheck == False:
                            ispis_check = await check_ispis(rc)
                        if precheck == True:
                            ispis_check = True  # prechecks our database
                        if isinstance(ispis_check, str):
                            if "Error" in ispis_check:
                                if "connecting" in ispis_check:
                                    return JsonResponse({'status': 'ispis down'}, status=500)
                                if "response" in ispis_check:
                                    return JsonResponse({'status': 'ispis response broken'}, status=500)
                        else:
                            if ispis_check is False:
                                # New Lead,  is_owner = False, dissmiss offer
                                new_lead = await _new_lead(rc, is_owner=False, source=source)
                                # new dismissed offer
                                offer = await _new_offer(rc, source)
                                return JsonResponse({'status': 'bez nemovitosti'}, status=403)
                            elif ispis_check is True:
                                # New Lead, is_owner = True, accept offer
                                new_lead = await _new_lead(rc, True, source)
                                # new accepted offer
                                offer = await _new_offer(rc, source, True, lead=new_lead)
                                return JsonResponse({'status': 'bereme'}, status=200)

        return HttpResponse("results: " + str(source))


@sync_to_async
@csrf_exempt
@async_to_sync
async def accept(request):

    if request.method == "GET":
        return HttpResponse("This is a GET request")
    elif request.method == "POST":
        headers = request.headers
        body = request.body  # [1:-1].replace("\'", '\"')
        data = body.decode("utf-8")
        json_data = json.loads(data)
#
        rc = json_data["rodnecislo"]
        token = headers["token"]

        ip = await get_client_ip(request)
        url = request.path
        headers = request.headers
        res = await _new_request(ip, url, data, headers)
        print(str(res))

        # find API key in DB
        source = await _get_source(token)

        if isinstance(source, bool):
            # Token not found
            return JsonResponse({'status': 'wrong token'}, status=403)
        elif source.active is True:
            # Token found
            # Load POST Data

            if "jmeno" in json_data:
                first_name = json_data["jmeno"]
            else:
                first_name = None
            if "prijmeni" in json_data:
                last_name = json_data["prijmeni"]
            else:
                last_name = None
            if "telefon" in json_data:
                phone_number = json_data["telefon"]
            else:
                phone_number = None
            if "email" in json_data:
                email = json_data["email"]
            else:
                email = None
            if "pozadovanaCastka" in json_data:
                requested_amount = json_data["pozadovanaCastka"]
            else:
                requested_amount = None
            if "prijem" in json_data:
                income = json_data["prijem"]
            else:
                income = None
            if "trvUlice" in json_data:
                addr_street = json_data["trvUlice"]
            else:
                addr_street = None
            if "trvMesto" in json_data:
                addr_city = json_data["trvMesto"]
            else:
                addr_city = None
            if "trvPsc" in json_data:
                addr_zip = json_data["trvPsc"]
            else:
                addr_zip = None
            ### ###
            # Leadsor sends us all leads ???
            lead = await _get_lead(rc)
            if isinstance(lead, bool):
                # if there is no lead there is nothing to log
                return JsonResponse({'status': 'lead not found.'}, status=403)
            if str(source) == "Leadsor":
                offer = await _check_offer(lead, source)

                if isinstance(offer, bool):
                    return JsonResponse({'status': 'not offered'}, status=403)
                elif str(offer.source) == str(source) and offer.checked == True and offer.accepted == False:
                    # Lead found and offer OK!
                    edit_lead = await _edit_lead(rc=rc, bought=True, first_name=first_name, last_name=last_name, phone_number=phone_number, email=email,
                                                 requested_amount=requested_amount, income=income, addr_street=addr_street, addr_city=addr_city, addr_zip=addr_zip)
                    edit_offer = await _edit_offer(lead)
                    if edit_lead is False:
                        # this generally shouldnt happen, thats why we return 404, _edit_lead() is responsible for this
                        return JsonResponse({'status': 'Error! Lead not found!'}, status=401)
                    if edit_offer is False:
                        # this generally shouldnt happen, thats why we return 401, _edit_offer() is responsible for this

                        return JsonResponse({'status': 'Error! Offer not found!'}, status=401)

                    if edit_lead and edit_offer:
                        return JsonResponse({'status': 'lead accepted successfully'}, status=201)
                elif offer.checked == False:
                    # Lead not checked
                    return JsonResponse({'status': 'lead not checked.'}, status=403)
                elif lead.bought == True:
                    # Lead already accepted
                    return JsonResponse({'status': 'lead already accepted.'}, status=403)
            else:
                offer = await _check_offer(lead, source)

                if isinstance(offer, bool):
                    return JsonResponse({'status': 'not offered'}, status=403)
                elif str(offer.source) == str(source) and offer.checked == True and offer.accepted == False:
                    # Lead found and offer OK!
                    edit_lead = await _edit_lead(rc=rc, bought=True, first_name=first_name, last_name=last_name, phone_number=phone_number, email=email,
                                                 requested_amount=requested_amount, income=income, addr_street=addr_street, addr_city=addr_city, addr_zip=addr_zip)
                    edit_offer = await _edit_offer(lead)
                    if edit_lead is False:
                        # this generally shouldnt happen, thats why we return 404, _edit_lead() is responsible for this
                        return JsonResponse({'status': 'Error! Lead not found!'}, status=401)
                    if edit_offer is False:
                        # this generally shouldnt happen, thats why we return 401, _edit_offer() is responsible for this

                        return JsonResponse({'status': 'Error! Offer not found!'}, status=401)

                    if edit_lead and edit_offer:
                        return JsonResponse({'status': 'lead accepted successfully'}, status=201)
                elif offer.checked == False:
                    # Lead not checked
                    return JsonResponse({'status': 'lead not checked.'}, status=403)
                elif lead.bought == True:
                    # Lead already accepted
                    return JsonResponse({'status': 'lead already accepted.'}, status=403)

        return HttpResponse("results: " + str(source))
