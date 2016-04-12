'''
Created on 7/4/2016

@author: suarez
'''
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.http.response import StreamingHttpResponse
import datetime
import pymongo
import json


client = pymongo.MongoClient('localhost', 27017)
db = client['estacio_ga']

def insert_ticket(request):
    if request.method=='POST':
            rdata=json.loads(request.body)
            try:
                ticket =  {
                        '_id':rdata['num_ticket'],
                        'hora_entrada':datetime.datetime.utcnow(),
                        'nombre_estacionamiento':rdata['nombre_estacionamiento'],
                        'pago_hecho':rdata['pago_hecho'],
                        'ticket_activo':True,
                        }
                tickets = db.tickets
                ticket_id = tickets.insert_one(ticket).inserted_id
                print(ticket_id)
                print(ticket)
                return StreamingHttpResponse('true')
            except ValueError:
                print('Error al insertar en la base de datos')
                return StreamingHttpResponse('false')
    return StreamingHttpResponse('GET request')

def inicio(request):
    return render(request, 'test.html')