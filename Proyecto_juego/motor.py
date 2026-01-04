import globales as gb
import random

def crear_matriz_dinamica(dimension):
    matriz_tablero = []
    indice_fila = 0
    while indice_fila < dimension:
        nueva_fila_lista = []
        indice_columna = 0
        while indice_columna < dimension:
            nueva_fila_lista.append(gb.VACIO)
            indice_columna += 1
        matriz_tablero.append(nueva_fila_lista)
        indice_fila += 1
    return matriz_tablero

def generar_peones_ciegos(tablero_referencia, dimension):
    peones_blancos_colocados = 0
    while peones_blancos_colocados < 4:
        fila_aleatoria = random.randint(0, dimension - 1)
        columna_aleatoria = random.randint(0, dimension - 1)
        if tablero_referencia[fila_aleatoria][columna_aleatoria] == gb.VACIO:
            tablero_referencia[fila_aleatoria][columna_aleatoria] = "P"
            peones_blancos_colocados += 1
            
    peones_negros_colocados = 0
    while peones_negros_colocados < 4:
        fila_aleatoria = random.randint(0, dimension - 1)
        columna_aleatoria = random.randint(0, dimension - 1)
        if tablero_referencia[fila_aleatoria][columna_aleatoria] == gb.VACIO:
            tablero_referencia[fila_aleatoria][columna_aleatoria] = "p"
            peones_negros_colocados += 1

def calcular_movimientos(fila_origen, columna_origen, pieza_actual, dimension, tablero_actual):
    lista_movimientos = []
    tipo_pieza = pieza_actual.upper()
    simbolo_enemigo = "p" if pieza_actual.isupper() else "P"
    orientaciones_de_movimiento = []
    
    if tipo_pieza == "T": 
        orientaciones_de_movimiento = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    elif tipo_pieza == "A": 
        orientaciones_de_movimiento = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    elif tipo_pieza == "Q": 
        orientaciones_de_movimiento = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    if tipo_pieza in ["T", "A", "Q"]:
        indice_orientacion = 0
        while indice_orientacion < len(orientaciones_de_movimiento):
            cambio_fila, cambio_columna = orientaciones_de_movimiento[indice_orientacion]
            proxima_fila = fila_origen + cambio_fila
            proxima_columna = columna_origen + cambio_columna
            camino_esta_despejado = True
            
            while 0 <= proxima_fila < dimension and 0 <= proxima_columna < dimension and camino_esta_despejado:
                if tablero_actual[proxima_fila][proxima_columna] == gb.VACIO:
                    lista_movimientos.append((proxima_fila, proxima_columna))
                elif tablero_actual[proxima_fila][proxima_columna] == simbolo_enemigo:
                    lista_movimientos.append((proxima_fila, proxima_columna))
                    camino_esta_despejado = False
                else:
                    camino_esta_despejado = False
                proxima_fila += cambio_fila
                proxima_columna += cambio_columna
            indice_orientacion += 1
            
    elif tipo_pieza == "R":
        desplazamiento_fila = -1
        while desplazamiento_fila <= 1:
            desplazamiento_columna = -1
            while desplazamiento_columna <= 1:
                if desplazamiento_fila != 0 or desplazamiento_columna != 0:
                    fila_destino = fila_origen + desplazamiento_fila
                    columna_destino = columna_origen + desplazamiento_columna
                    if 0 <= fila_destino < dimension and 0 <= columna_destino < dimension:
                        if tablero_actual[fila_destino][columna_destino] == gb.VACIO or tablero_actual[fila_destino][columna_destino] == simbolo_enemigo:
                            lista_movimientos.append((fila_destino, columna_destino))
                desplazamiento_columna += 1
            desplazamiento_fila += 1
            
    elif tipo_pieza == "C":
        patrones_salto_caballo = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        indice_patron = 0
        while indice_patron < len(patrones_salto_caballo):
            salto_fila, salto_columna = patrones_salto_caballo[indice_patron]
            fila_final = fila_origen + salto_fila
            columna_final = columna_origen + salto_columna
            if 0 <= fila_final < dimension and 0 <= columna_final < dimension:
                if tablero_actual[fila_final][columna_final] == gb.VACIO or tablero_actual[fila_final][columna_final] == simbolo_enemigo:
                    lista_movimientos.append((fila_final, columna_final))
            indice_patron += 1
            
    return lista_movimientos