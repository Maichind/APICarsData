from flask import Flask, jsonify, request, Response
import pymongo
import certifi
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

from models.carsData import CarsData

ca = certifi.where()
client = pymongo.MongoClient("mongodb://Mind:Mindiola97_@ac-lfv0xhc-shard-00-00.8jzlylr.mongodb.net:27017,ac-lfv0xhc-shard-00-01.8jzlylr.mongodb.net:27017,ac-lfv0xhc-shard-00-02.8jzlylr.mongodb.net:27017/?ssl=true&replicaSet=atlas-4m3kaw-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.test

baseDatos = client["CarData"] 
print(baseDatos.list_collection_names())

@app.route('/')
def home():
    return jsonify({"mensaje": "CARS DATA"})
    #return render_template('index.html')


# ------------- Cars Data ----------------------
# Metods: POST
# Opcion para agregar a la base de datos.
@app.route('/cars', methods=['POST'])
def addCar():
    id = request.json['id']
    placa = request.json['placa']
    marca = request.json['marca']
    modelo = request.json['modelo']
    kilometraje = request.json['kilometraje']
    transmision = request.json['transmision']
    tipo = request.json['tipo']
    precio = request.json['precio']

    if id and placa and marca and modelo and kilometraje and transmision and tipo and precio:
        carNew = CarsData(id, placa, marca, modelo, kilometraje, transmision, tipo, precio)
        baseDatos.carData.insert_one(carNew.toDBCollection())
        response = jsonify({
            "id" : id,
            "placa" : placa,
            "marca" : marca,
            "modelo" : modelo,
            "kilometraje" : kilometraje,
            "transmision" : transmision,
            "tipo" : tipo,
            "precio" : precio
        })
        return response
    return notFound()

# Metods: GET
# Opcion para obtener los datos de todos los autos registrados.
@app.route('/cars', methods=['GET'])
def getCars():
    cars = baseDatos.carData.find()
    response = json_util.dumps(cars)
    return Response (response, mimetype='application/json')

# Opcion para obtener los datos de un auto registrado por su id.
@app.route('/cars/<id>', methods=['GET'])
def getCar(id):
    car = baseDatos.carData.find_one({"_id": ObjectId(id)})
    response = json_util.dumps(car)
    return Response (response, mimetype='application/json')

# Metods: PUT
# Opcion para actualizar los datos de un auto registrado por su id.
@app.route('/cars/update/<id>', methods=['PUT'])
def updateCar(id):
    id = request.json['id']
    placa = request.json['placa']
    marca = request.json['marca']
    modelo = request.json['modelo']
    kilometraje = request.json['kilometraje']
    transmision = request.json['transmision']
    tipo = request.json['tipo']
    precio = request.json['precio']

    if id and placa and marca and modelo and kilometraje and transmision and tipo and precio :
        baseDatos.carData.update_one({"_id": ObjectId(id)}, {'$set' : 
                                    {'id' : id, 'placa' : placa,
                                    'marca' : marca, 'modelo' : modelo, 'kilometraje' : kilometraje,
                                    'transmision' : transmision, 'tipo' : tipo, 'precio' : precio}})
        response = jsonify({'message' : 'Car ' + id + ' actualizado correctamente'})
        return response
    return notFound()

# Metods: DELETE
#Opción para eliminar una mesa por su id.
@app.route('/cars/delete/<id>', methods=['DELETE'])
def deleteCar(id):
    baseDatos.carData.delete_one({"_id": ObjectId(id)})
    return jsonify({'message' : 'Car '+ id +' borrado correctamente'})


#----------------ERROR-----------------------
@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
     app.run(host="0.0.0.0", port=9999, debug=True)