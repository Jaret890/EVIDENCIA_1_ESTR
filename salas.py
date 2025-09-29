from datetime import datetime, timedelta
import random


#Listas
clientes = []
salas = []
reservaciones = []


#Clases
class Cliente:
    def __init__(self, clave, nombre, apellidos):
        self.clave = clave
        self.nombre = nombre
        self.apellidos = apellidos

class Sala:
    def __init__(self, clave, nombre, cupo):
        self.clave = clave
        self.nombre = nombre
        self.cupo = cupo

class Reservacion:
    def __init__(self, folio, fecha, turno, sala, cliente, evento):
        self.folio = folio
        self.fecha = fecha
        self.turno = turno
        self.sala = sala
        self.cliente = cliente
        self.evento = evento 
        
#Generador para las claves
def clave_cliente():
    while True:
        clave = f"C{random.randint(100,999)}"
        if not any(c.clave == clave for c in clientes):
            return clave

def clave_sala():
    while True:
        clave = f"S{random.randint(100,999)}"
        if not any(s.clave == clave for s in salas):
            return clave

def generar_folio():
    while True:
        folio = f"F{random.randint(10000,99999)}"
        if not any(r.folio == folio for r in reservaciones):
            return folio

#Constantes
TURNOS = {"1": "Matutino", "2": "Vespertino", "3": "Nocturno"}

FORMATO_FECHA = "%d/%m/%Y"

#Funciones
def registar_reservacion():
    if not clientes or not salas:
        print("--No hay ningun cliente/sala registrados--")
        return

    ordenados = sorted(clientes, key=lambda c: (c.apellidos.lower(), c.nombre.lower()))
    print("Clientes Registrados: ")
    print(f"{'Clave:6'} | {'Apellidos:20'} | {'Nombre:15'}")
    print("-"*50)
    for c in ordenados:
        print(f"{c.clave:6} | {c.apellidos:20} | {c.nombre:15} ") 

    while True:
        clave_cliente = input("Clave del cliente ('0' para cancelar): ")
        if clave_cliente == "0":
            return
        cliente = next((c for c in clientes if c.clave == clave_cliente), None)
        if cliente:
            break
        print("--Clave no encontrada--")

    hoy = datetime.now().date()
    minimo = hoy + timedelta(days=2)
    while True:
        fecha_str = input(f"Fecha del evento ({FORMATO_FECHA}), minimo {minimo.strftime(FORMATO_FECHA)}: ")
        try:
            fecha = datetime.strptime(fecha_str, FORMATO_FECHA).date()
            if fecha < minimo:
                print("La reservacion debe de hacerse al menos dos dias antes")
            else:
                break
        except:
            print("Fecha invalida")

    print("--Salas con disponibilidad: ")
    disponibles = []
    for s in salas:
        libres = [t for t in TURNOS.values() if not any(r.sala.clave == s.clave and r.fecha == fecha and r.turno == t for r in reservaciones)]
        if libres:
            disponibles.append((s, libres))
            print(f"{s.clave} - {s.nombre} (cupo{s.cupo}) | Turnos: {', '.join(libres)}")
    
    if not disponibles:
        print("--No hay salas disponibles en esa fecha--")
        return
    
    clave_sala = input("Clave de sala ('0' para cancelar): ")
    if clave_sala == "0":
        return
    sala = next((s for s in salas if s.clave == clave_sala), None)
    if not sala:
        print("--Sala no encontrada--")
        return
    
    libres = [t for t in TURNOS.values() if not any(r.sala.clave == sala.clave and r.fecha == fecha and r.turno == t for r in reservaciones)]
    print("--Turnos disponibles--")
    for k, v in TURNOS.items():
        if v in libres:
            print(f"{k}. {v}")

    opcion_turno = input("-Elige el turno (1/2/3): ")
    if opcion_turno not in TURNOS or TURNOS[opcion_turno] not in libres:
        print("--Turno invalido--")
        return
    
    nombre_evento = input("-Nombre del evento: ")
    if not nombre_evento:
        print("--El nombre no puede estar vacio--")
        return
    turno = TURNOS[opcion_turno]
    
    folio = generar_folio()
    reservaciones.append(Reservacion(folio, fecha, turno, sala, cliente, nombre_evento))
    print(f"--Reservacion registrada con folio {folio}")

def editar_evento():
    if not reservaciones:
        print("--No hay reservaciones registradas--")
        return
    fecha_inicio_str = input(f"Fecha inicio ({FORMATO_FECHA}): ")
    fecha_fin_str = input(f"Fecha fin ({FORMATO_FECHA}): ")
    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, FORMATO_FECHA).date()
        fecha_fin = datetime.strptime(fecha_fin_str, FORMATO_FECHA).date()
    except:
        print("--Fechas invalidas--")
        return
    if fecha_inicio > fecha_fin:
        print("--La fecha inicial no puede se mayor que la final--")
        return
    
    seleccionadas = [r for r in reservaciones if fecha_inicio <= r.fecha <= fecha_fin]
    if not seleccionadas:
        print("--No existen reservacines en ese rango--")
        return
    
    while True:
        print("--Reservaciones en rango:")
        for r in seleccionadas:
            print(f"Folio: {r.folio}, Evento: {r.evento}, Fecha: {r.fecha.strftime(FORMATO_FECHA)}")
        folio = input("Folio a editar ('0' para cancelar): ")
        if folio == "0":
            return
        res = next((r for r in seleccionadas if r.folio == folio), None)
        if res:
            nuevo_nombre = input("Nuevo nombre: ")
            if nuevo_nombre:
                res.nombre_evento = nuevo_nombre
                print("--Evento actualizado--")
                return
            else:
                print("--El nombre no puede estar vacio--")
        else:
            print("--Folio no valido--")

def consultar_por_fecha():
    if not reservaciones:
        print("--No hay reservaciones registradas--")
        return
    fecha_str = input(f"Fecha a consultar ({FORMATO_FECHA}): ")
    try:
        fecha = datetime.strptime(fecha_str, FORMATO_FECHA).date()
    except:
        print("--Fecha invalida--")
        return
    encontrados = [r for r in reservaciones if r.fecha == fecha]
    if not encontrados:
        print("--No hay reservaciones en esta fecha--")
        return
    for r in encontrados:
        print(f"Folio: {r.folio}, Evento: {r.evento}, Sala: {r.sala.nombre}, Turno: {r.turno}, Cliente: {r.cliente.nombre} {r.cliente.apellidos}")

def registrar_cliente():
    clave =  clave_cliente()
    nombre = input("-Nombre del cliente: ")
    apellidos = input("-Apellidos: ")
    clientes.append(Cliente(clave, nombre, apellidos))
    print(f"--Cliente registrado con clave {clave}--")

def registrar_sala():
    clave = clave_sala()
    nombre = input("-Nombre de la sala: ")
    cupo = int(input("-Cupo maximo: "))
    salas.append(Sala(clave, nombre, cupo))
    print(f"--Sala registrada con clave {clave}--")
     

    

#Menu
while True:
    print("--Menu de Reservas--")
    print("1.-Registrar reservacion de sala")
    print("2.-Editar el nombre del evento de una reservacion ya hecha")
    print("3.-Consultar las reservaciones por una fecha en especifico")
    print("4.-Registrar un nuevo cliente")
    print("5.-Registrar un sala")
    print("6.-Salir")
    opcion = int(input("--Elige una opcion: "))

    if opcion == 1:
        registar_reservacion()
    elif opcion == 2:
        editar_evento()
    elif opcion == 3:
        consultar_por_fecha()
    elif opcion == 4:
        registrar_cliente()
    elif opcion == 5:
        registrar_sala()
    elif opcion == 6:
        print("--Adios--")
        break