import pygame
import globales as gb

IMAGENES_PIEZAS = {}

def cargar_recursos_graficos(tamano_celda):
    traductor_nombres = {
        'P': 'B_Peon', 'p': 'N_Peon',
        'T': 'B_Torre', 't': 'N_Torre',
        'C': 'B_Caballo', 'c': 'N_Caballo',
        'A': 'B_Alfil', 'a': 'N_Alfil',
        'D': 'B_Dama', 'd': 'N_Dama',
        'R': 'B_Rey', 'r': 'N_Rey'
    }

    for letra, nombre_archivo in traductor_nombres.items():
        try:
            ruta = f"assets/{nombre_archivo}.png"
            imagen = pygame.image.load(ruta).convert_alpha()
            IMAGENES_PIEZAS[letra] = pygame.transform.scale(imagen, (tamano_celda, tamano_celda))
        except:
            IMAGENES_PIEZAS[letra] = None

def imprimir_tablero_dinamico(ventana, matriz, dimension, sugerencias, es_turno_blancas):
    MARGEN_IZQUIERDO = 50
    MARGEN_SUPERIOR = 100
    ANCHO_BITACORA = 220
    
    ESPACIO_DISPONIBLE = gb.ANCHO_VENTANA - ANCHO_BITACORA - (MARGEN_IZQUIERDO * 2)
    TAMANO_CELDA = ESPACIO_DISPONIBLE // dimension

    if not IMAGENES_PIEZAS:
        cargar_recursos_graficos(TAMANO_CELDA)

    fila = 0
    while fila < dimension:
        columna = 0
        while columna < dimension:
            pos_x = MARGEN_IZQUIERDO + (columna * TAMANO_CELDA)
            pos_y = MARGEN_SUPERIOR + (fila * TAMANO_CELDA)
            rectangulo_celda = pygame.Rect(pos_x, pos_y, TAMANO_CELDA, TAMANO_CELDA)

            color_celda = (240, 217, 181) if (fila + columna) % 2 == 0 else (181, 136, 99)
            pygame.draw.rect(ventana, color_celda, rectangulo_celda)
            pygame.draw.rect(ventana, (0, 0, 0), rectangulo_celda, 1)

            pieza_actual = matriz[fila][columna]
            if pieza_actual != gb.VACIO:
                if pieza_actual in IMAGENES_PIEZAS and IMAGENES_PIEZAS[pieza_actual] is not None:
                    ventana.blit(IMAGENES_PIEZAS[pieza_actual], (pos_x, pos_y))
                else:
                    fuente = pygame.font.SysFont("Arial", TAMANO_CELDA // 2, bold=True)
                    color_texto = (255, 255, 255) if pieza_actual.isupper() else (0, 0, 0)
                    render_letra = fuente.render(pieza_actual, True, color_texto)
                    ventana.blit(render_letra, (pos_x + (TAMANO_CELDA // 4), pos_y + (TAMANO_CELDA // 4)))

            for sug_fila, sug_col in sugerencias:
                if sug_fila == fila and sug_col == columna:
                    superficie_sug = pygame.Surface((TAMANO_CELDA, TAMANO_CELDA), pygame.SRCALPHA)
                    color_circulo = (255, 0, 0, 160) if matriz[fila][columna] != gb.VACIO else (0, 255, 0, 160)
                    pygame.draw.circle(superficie_sug, color_circulo, (TAMANO_CELDA // 2, TAMANO_CELDA // 2), TAMANO_CELDA // 3, 5)
                    ventana.blit(superficie_sug, (pos_x, pos_y))
            columna += 1
        fila += 1

def convertir_posicion_a_coordenada(pos_mouse, dimension):
    MARGEN_IZQUIERDO = 50
    MARGEN_SUPERIOR = 100
    ANCHO_BITACORA = 220
    ESPACIO_DISPONIBLE = gb.ANCHO_VENTANA - ANCHO_BITACORA - (MARGEN_IZQUIERDO * 2)
    TAMANO_CELDA = ESPACIO_DISPONIBLE // dimension

    x, y = pos_mouse
    if MARGEN_IZQUIERDO <= x <= MARGEN_IZQUIERDO + ESPACIO_DISPONIBLE and \
       MARGEN_SUPERIOR <= y <= MARGEN_SUPERIOR + ESPACIO_DISPONIBLE:
        col = (x - MARGEN_IZQUIERDO) // TAMANO_CELDA
        fil = (y - MARGEN_SUPERIOR) // TAMANO_CELDA
        return int(fil), int(col)
    return None

def convertir_a_texto(fila, columna, dimension):
    letras = "ABCDEFGHIJKLMN"
    nombre_columna = letras[columna]
    nombre_fila = str(dimension - fila)
    return f"{nombre_columna}{nombre_fila}"