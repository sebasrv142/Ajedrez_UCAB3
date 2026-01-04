import globales as gb
import struct
from datetime import datetime

def obtener_nombre_jugador(cedula_a_buscar):
    nombre_encontrado = "Desconocido"
    continuar_busqueda = True
    try:
        with open(gb.ARCHIVO_USUARIOS, "rb") as archivo_binario:
            while continuar_busqueda:
                bloque_registro = archivo_binario.read(gb.CANTIDAD_BYTES_REGISTRO)
                if not bloque_registro:
                    continuar_busqueda = False
                else:
                    datos_desempaquetados = struct.unpack(gb.FORMATO_ESTRUCTURA_USUARIO, bloque_registro)
                    cedula_en_archivo = datos_desempaquetados[0].decode('utf-8').strip('\x00').strip()
                    if cedula_en_archivo == cedula_a_buscar:
                        nombre_encontrado = datos_desempaquetados[1].decode('utf-8').strip('\x00').strip()
                        continuar_busqueda = False
    except:
        pass
    return nombre_encontrado

def actualizar_puntos_jugador(cedula_del_ganador, puntos_para_sumar):
    lista_de_registros = []
    usuario_encontrado = False
    continuar_lectura = True
    try:
        with open(gb.ARCHIVO_USUARIOS, "rb") as archivo_lectura:
            while continuar_lectura:
                bloque_actual = archivo_lectura.read(gb.CANTIDAD_BYTES_REGISTRO)
                if not bloque_actual:
                    continuar_lectura = False
                else:
                    datos_usuario = list(struct.unpack(gb.FORMATO_ESTRUCTURA_USUARIO, bloque_actual))
                    cedula_actual = datos_usuario[0].decode('utf-8').strip('\x00').strip()
                    if cedula_actual == cedula_del_ganador:
                        cadena_puntos_actuales = datos_usuario[5].decode('utf-8').strip('\x00').strip()
                        valor_puntos_actuales = int(cadena_puntos_actuales) if cadena_puntos_actuales.isdigit() else 0
                        total_puntos_nuevos = valor_puntos_actuales + puntos_para_sumar
                        datos_usuario[5] = str(total_puntos_nuevos).encode('utf-8').ljust(40, b'\x00')
                        usuario_encontrado = True
                    lista_de_registros.append(struct.pack(gb.FORMATO_ESTRUCTURA_USUARIO, *datos_usuario))
        
        if usuario_encontrado:
            with open(gb.ARCHIVO_USUARIOS, "wb") as archivo_escritura:
                indice = 0
                while indice < len(lista_de_registros):
                    archivo_escritura.write(lista_de_registros[indice])
                    indice += 1
    except:
        pass

def obtener_catalogo_piezas(es_blanco):
    if es_blanco:
        return gb.PIEZAS_BLANCAS
    return gb.PIEZAS_NEGRAS

def obtener_id_consecutivo_juego():
    identificador_actual = 1
    archivo_abierto = True
    try:
        with open(gb.ARCHIVO_JUEGOS, "rb") as archivo_juegos:
            while archivo_abierto:
                bloque = archivo_juegos.read(gb.CANTIDAD_BYTES_JUEGO)
                if not bloque:
                    archivo_abierto = False
                else:
                    identificador_actual += 1
    except:
        pass
    return identificador_actual

def registrar_juego_binario(pos_inicial_j1, ficha_j1, pos_inicial_j2, ficha_j2):
    id_nuevo_juego = obtener_id_consecutivo_juego()
    fecha_actual_texto = datetime.now().strftime("%d/%m/%Y")
    registro_empaquetado = struct.pack(
        gb.FORMATO_REGISTRO_JUEGO,
        id_nuevo_juego,
        fecha_actual_texto.encode('utf-8'),
        gb.ID_SESION_JUGADOR_UNO.encode('utf-8'),
        ficha_j1.encode('utf-8'),
        pos_inicial_j1.encode('utf-8'),
        gb.ID_SESION_JUGADOR_DOS.encode('utf-8'),
        ficha_j2.encode('utf-8'),
        pos_inicial_j2.encode('utf-8')
    )
    with open(gb.ARCHIVO_JUEGOS, "ab") as archivo_append:
        archivo_append.write(registro_empaquetado)
    return id_nuevo_juego

def registrar_movimiento_binario(id_del_juego, ficha_utilizada, destino_texto, puntos_obtenidos):
    objeto_fecha_hora = datetime.now()
    fecha_texto = objeto_fecha_hora.strftime("%d/%m/%Y")
    hora_texto = objeto_fecha_hora.strftime("%H:%M:%S")
    movimiento_empaquetado = struct.pack(
        gb.FORMATO_MOVIMIENTO,
        id_del_juego,
        ficha_utilizada.encode('utf-8'),
        fecha_texto.encode('utf-8'),
        hora_texto.encode('utf-8'),
        destino_texto.encode('utf-8'),
        puntos_obtenidos
    )
    with open(gb.ARCHIVO_MOVIMIENTOS, "ab") as archivo_movs:
        archivo_movs.write(movimiento_empaquetado)