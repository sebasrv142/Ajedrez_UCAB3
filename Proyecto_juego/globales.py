import struct
import os
import pygame

NOMBRE_CARPETA = "archivos_sistema"
if not os.path.exists(NOMBRE_CARPETA):
    os.makedirs(NOMBRE_CARPETA)

FORMATO_ESTRUCTURA_USUARIO = "10s30s1s10s15s40s"
CANTIDAD_BYTES_REGISTRO = struct.calcsize(FORMATO_ESTRUCTURA_USUARIO)
ARCHIVO_USUARIOS = os.path.join(NOMBRE_CARPETA, "JUGADORES.bin")

ARCHIVO_JUEGOS = os.path.join(NOMBRE_CARPETA, "JUEGO.bin")
FORMATO_REGISTRO_JUEGO = "i10s15s2s5s15s2s5s"
CANTIDAD_BYTES_JUEGO = struct.calcsize(FORMATO_REGISTRO_JUEGO)

ARCHIVO_MOVIMIENTOS = os.path.join(NOMBRE_CARPETA, "MOVIMIENTOS.bin")
FORMATO_MOVIMIENTO = "i2s10s8s5si"
CANTIDAD_BYTES_MOVIMIENTO = struct.calcsize(FORMATO_MOVIMIENTO)

ID_SESION_JUGADOR_UNO = ""
ID_SESION_JUGADOR_DOS = ""
INDICE_PAGINA_ACTUAL = 0

DIMENSION_TABLERO = 8
VACIO = "·"

PIEZAS_BLANCAS = {
    "PAON": "P", "TORRE": "T", "CABALLO": "C",
    "ALFIL": "A", "REINA": "Q", "REY": "R"
}

PIEZAS_NEGRAS = {
    "PAON": "p", "TORRE": "t", "CABALLO": "c",
    "ALFIL": "a", "REINA": "q", "REY": "r"
}

RUTA_IMAGEN_CABALLO = ""
ANCHO_TABLERO_JUEGO = 20
ALTO_TABLERO_JUEGO = 20

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
COLOR_FONDO = (255, 255, 255)
COLOR_TEXTO = (0, 0, 0)
COLOR_SELECCION = (255, 0, 0)
COLOR_TABLERO_CLARO = (238, 238, 210)
COLOR_TABLERO_OSCURO = (118, 150, 86)

def cargar_imagen(nombre_archivo, escala=None):
    ruta = os.path.join("assets", nombre_archivo)
    try:
        imagen = pygame.image.load(ruta).convert_alpha()
        if escala:
            imagen = pygame.transform.scale(imagen, escala)
        return imagen
    except:
        return None