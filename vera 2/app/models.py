class Estudiante:
    def __init__(self, id, nombre, carnet, email):
        self.id = id
        self.nombre = nombre
        self.carnet = carnet
        self.email = email

    def __str__(self):
        return f"[{self.id}] {self.nombre} - {self.carnet} - {self.email}"
