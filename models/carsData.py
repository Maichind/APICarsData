class CarsData:
    def __init__(self, id, placa, marca, modelo, kilometraje, transmision, tipo, precio):
        self.id = id
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.kilometraje = kilometraje
        self.transmision = transmision
        self.tipo = tipo
        self.precio = precio
    
    def toDBCollection(self):
        return {
            "id": self.id,
            "placa": self.placa,
            "marca": self.marca,
            "modelo": self.modelo,
            "kilometraje": self.kilometraje,
            "transmision": self.transmision,
            "tipo": self.tipo,
            "precio": self.precio
        }