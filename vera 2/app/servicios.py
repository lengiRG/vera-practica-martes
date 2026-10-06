import json
import os

from app.models import Estudiante


class GestorEstudiantes:
    def __init__(self, ruta):
        self.ruta = ruta
        directorio = os.path.dirname(ruta)
        if directorio:
            os.makedirs(directorio, exist_ok=True)
        if not os.path.exists(ruta):
            self.guardar([])

    def cargar(self):
        if not os.path.exists(self.ruta):
            return []

        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if not contenido:
                    return []
                return json.loads(contenido)
        except (json.JSONDecodeError, OSError):
            return []

    def guardar(self, datos):
        directorio = os.path.dirname(self.ruta)
        if directorio:
            os.makedirs(directorio, exist_ok=True)

        with open(self.ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def crear(self, nombre, carnet, email):
        datos = self.cargar()
        nombre = nombre.strip() if nombre else ""
        carnet = carnet.strip() if carnet else ""
        email = email.strip() if email else ""

        if not nombre or not carnet or not email:
            return False, "Todos los campos son obligatorios."

        for d in datos:
            if d["carnet"] == carnet:
                return False, "Ese carnet ya existe."

        nuevo_id = max((d["id"] for d in datos), default=0) + 1
        datos.append({"id": nuevo_id, "nombre": nombre, "carnet": carnet, "email": email})
        self.guardar(datos)
        return True, "Estudiante creado."

    def listar(self):
        return [Estudiante(d["id"], d["nombre"], d["carnet"], d["email"]) for d in self.cargar()]

    def buscar(self, texto):
        texto = (texto or "").lower().strip()
        resultado = []
        for e in self.listar():
            if texto in e.nombre.lower() or texto in e.carnet.lower() or texto in e.email.lower():
                resultado.append(e)
        return resultado

    def actualizar(self, id, nombre=None, carnet=None, email=None):
        datos = self.cargar()
        nombre = nombre.strip() if nombre is not None else None
        carnet = carnet.strip() if carnet is not None else None
        email = email.strip() if email is not None else None

        for d in datos:
            if d["id"] == id:
                if carnet:
                    for otro in datos:
                        if otro["carnet"] == carnet and otro["id"] != id:
                            return False, "Ese carnet ya existe."
                    d["carnet"] = carnet
                if nombre:
                    d["nombre"] = nombre
                if email:
                    d["email"] = email
                self.guardar(datos)
                return True, "Estudiante actualizado."

        return False, "No existe ese estudiante."

    def eliminar(self, id):
        datos = self.cargar()
        nueva = [d for d in datos if d["id"] != id]

        if len(nueva) == len(datos):
            return False, "No existe ese estudiante."

        self.guardar(nueva)
        return True, "Estudiante eliminado."
