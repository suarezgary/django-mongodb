'''
Created on 7/4/2016

@author: suarez
'''
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.http.response import StreamingHttpResponse
from bson.json_util import dumps
import datetime
import pymongo
import json
import uuid
import hashlib, binascii



client = pymongo.MongoClient('localhost', 27017)
db = client['estacio_ga']

'''
Metodo para insertar un ticket al sistema
'''
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

'''
Metodo para hacer que un ticket se ponga como pago
'''
def pagar_ticket(request):
	if request.method=='POST':
			rdata=json.loads(request.body)
			print(rdata)
			try:
				tickets = db.tickets
				result = tickets.update_one( {"_id": rdata['num_ticket']}, { "$set": {'pago_hecho':True, 'hora_pago':datetime.datetime.utcnow()} } )
				print(result)
				return StreamingHttpResponse('true')
			except ValueError:
				print('Error al actualizar el ticket')
				return StreamingHttpResponse('false')
	return StreamingHttpResponse('GET request')


def create_cashier(request):
    if request.method=='POST':
            rdata=json.loads(request.body)
            try:
                #Unique Identifier
                guid = uuid.uuid4()
                print(guid)
            
                hash_object = hashlib.sha256( rdata['password'] + str(guid))
                hex_dig = hash_object.hexdigest()
                print(hex_dig)
                cashier = {
                           '_id': rdata['usuario'],
                           'password': hex_dig,
                           'guid': guid,
                           'nombre_cajero':rdata['nombre_cajero'],
                           'apellido_cajero':rdata['apellido_cajero'],
                           'cedula_cajero':rdata['cedula_cajero'],
                           'telefono':rdata['telefono'],
                           'nivel_cajero':rdata['nivel_cajero'],
                           'cargo_cajero':rdata['cargo_cajero'],
                           'direccion_cajero':rdata['direccion_cajero'],
                           }
                cashiers = db.cashiers
                cashier_id = cashiers.insert_one(cashier).inserted_id
                print(cashier_id)
                print(cashier)
                return StreamingHttpResponse('true')
            except ValueError:
                print('Error al insertar en la base de datos')
                return StreamingHttpResponse('false')
    return StreamingHttpResponse('GET request')


def delete_cashier(request):
    if request.method=='POST':
            rdata=json.loads(request.body)
            try:
                cashiers = db.cashiers
                cashiers.delete_one({'_id': rdata['usuario']})
                return StreamingHttpResponse('true')
            except ValueError:
                print('Error al borrar el cajero en la base de datos')
                return StreamingHttpResponse('false')
    return StreamingHttpResponse('GET request')

def verif_password(request):
    if request.method=='POST':
            rdata=json.loads(request.body)
            try:
                cashiers = db.cashiers
                cashier = cashiers.find_one({'_id': rdata['usuario']})
                #Verificando si coincide la Password
                hash_object = hashlib.sha256( rdata['password'] + str(cashier['guid']))
                hex_dig = hash_object.hexdigest()
                #Comparando claves
                if (hex_dig == cashier['password']):
                    return StreamingHttpResponse('true')
                else:
                    return StreamingHttpResponse('false')
                
            except ValueError:
                print('Error al insertar en la base de datos')
                return StreamingHttpResponse('false')
    return StreamingHttpResponse('GET request')


def add_operation(request):
    if request.method=='POST':
            rdata=json.loads(request.body)
            try:
                operacion={
                                 'hora_operacion':datetime.datetime.utcnow(),
                                 'ticket_asociado':rdata['ticket'],
                                 'tipo_operacion':rdata['tipo_operacion'],
                                 'num_taquilla':rdata['num_taquilla'],
                                 'nombre_estacionamiento':rdata['nombre_estacionamiento'],
                                 'cajero':rdata['cajero'],
                                 'pago_hecho':rdata['pago_hecho'],
                                 'monto_pago':rdata['monto_pago'], 
                            }
                operaciones = db.operaciones
                operacion_id = operaciones.insert_one(operacion).inserted_id
                print(operacion_id)
                print(operacion)
                return StreamingHttpResponse('true')
                
            except ValueError:
                print('Error al insertar Operacion en la base de datos')
                return StreamingHttpResponse('false')
    return StreamingHttpResponse('GET request')


def get_operaciones_fecha(request):
    if request.method=='POST':
            rdata=json.loads(request.body)
            try:
                filtro={
                        'hora_operacion': {
                                           '$gte': datetime.datetime.strptime(rdata['fecha_inicial'], '%Y-%m-%d %H:%M:%S.%f' ),
                                           '$lte': datetime.datetime.strptime(rdata['fecha_final'], '%Y-%m-%d %H:%M:%S.%f' ),
                                           }
                        }
                               
                operaciones = db.operaciones
                finded = operaciones.find(filtro)
                return JsonResponse(dumps(finded), safe = False)
                
            except ValueError:
                print('Error al insertar Operacion en la base de datos')
                return StreamingHttpResponse('false')
    return StreamingHttpResponse('GET request')


def add_estaciona(request):
    if request.method=='POST':
            rdata=json.loads(request.body)
            try:
                estacionamiento = {
                                    'nombre_estacionamiento':rdata['nombre'],
                                     'cantidad_puestos':rdata['puestos'],
                                     'puestos_disponibles':rdata['puestos'],
                                     'descripcion':rdata['descripcion'],
                                     'direccion_estacionamiento':rdata['direccion'],
                                     'estacionamiento_full':False,
                                     'precio_primera_fraccion':rdata['fraccion'],
                                     'precio_menos_3horas':rdata['menos_tres'],
                                     'precio_mas_3horas':rdata['mas_tres'],
                                     'porcentaje_iva':rdata['iva'],
                                }
                               
                estacionamientos = db.estacionamientos
                estacionamientos.insert_one(estacionamiento)
                return StreamingHttpResponse('true')
                
            except ValueError:
                print('Error al insertar Operacion en la base de datos')
                return StreamingHttpResponse('false')
    return StreamingHttpResponse('GET request')


def inicio(request):
    return render(request, 'test.html')
