import pygame
import globales as gb
import datos
import motor
import interfaz
import pantallas_previa as pp

def renderizar_interfaz_estetica(ventana, nombre_j1, id_j1, ficha_j1, puntos_j1, nombre_j2, id_j2, ficha_j2, puntos_j2, es_turno_blancas, historial_movimientos):
    fuente_interfaz = pygame.font.SysFont("Arial", 14, bold=True)
    fuente_historial = pygame.font.SysFont("Consolas", 13)
    ANCHO_BITACORA = 220
    AREA_TABLERO_DISPONIBLE = gb.ANCHO_VENTANA - ANCHO_BITACORA
    ANCHO_PANEL_JUGADOR = (AREA_TABLERO_DISPONIBLE - 30) // 2 
    
    icono_corona = None
    try:
        icono_corona = pygame.image.load("assets/corona.png").convert_alpha()
        icono_corona = pygame.transform.scale(icono_corona, (25, 25))
    except:
        icono_corona = None

    color_fondo_activo = (45, 55, 80)
    color_fondo_inactivo = (30, 30, 40)
    
    # Panel J1
    color_p1 = color_fondo_activo if es_turno_blancas else color_fondo_inactivo
    rect_j1 = pygame.Rect(10, 10, ANCHO_PANEL_JUGADOR, 65)
    pygame.draw.rect(ventana, color_p1, rect_j1, border_radius=10)
    pygame.draw.rect(ventana, (0, 255, 0) if es_turno_blancas else (80, 80, 80), rect_j1, 2, border_radius=10)
    ventana.blit(fuente_interfaz.render(f"J1: {nombre_j1}", True, (255, 255, 255)), (rect_j1.x + 10, 20))
    ventana.blit(fuente_interfaz.render(f"FICHA: {ficha_j1} | PTS: {puntos_j1}", True, (255, 255, 0)), (rect_j1.x + 10, 42))

    # Panel J2
    color_p2 = color_fondo_activo if not es_turno_blancas else color_fondo_inactivo
    rect_j2 = pygame.Rect(rect_j1.right + 10, 10, ANCHO_PANEL_JUGADOR, 65)
    pygame.draw.rect(ventana, color_p2, rect_j2, border_radius=10)
    pygame.draw.rect(ventana, (0, 255, 0) if not es_turno_blancas else (80, 80, 80), rect_j2, 2, border_radius=10)
    ventana.blit(fuente_interfaz.render(f"J2: {nombre_j2}", True, (255, 255, 255)), (rect_j2.x + 10, 20))
    ventana.blit(fuente_interfaz.render(f"FICHA: {ficha_j2} | PTS: {puntos_j2}", True, (255, 255, 0)), (rect_j2.x + 10, 42))

    # Historial
    x_hist = gb.ANCHO_VENTANA - ANCHO_BITACORA
    pygame.draw.rect(ventana, (20, 20, 25), (x_hist, 0, ANCHO_BITACORA, gb.ALTO_VENTANA))
    pygame.draw.line(ventana, (255, 255, 255), (x_hist, 0), (x_hist, gb.ALTO_VENTANA), 1)
    ventana.blit(fuente_interfaz.render("HISTORIAL", True, (0, 255, 255)), (x_hist + 65, 80))

    y_t = 120
    inicio = max(0, len(historial_movimientos) - 22)
    for i in range(inicio, len(historial_movimientos)):
        linea = historial_movimientos[i]
        col = (150, 255, 150) if "J1" in linea else (150, 150, 255)
        if "---" in linea: col = (255, 255, 0)
        ventana.blit(fuente_historial.render(linea, True, col), (x_hist + 15, y_t))
        y_t += 22

def iniciar_partida(ventana_maestra):
    esta_jugando = True
    
    while esta_jugando:
        # 1. SELECCIÓN DE CONFIGURACIÓN
        dimension = pp.pantalla_seleccion_dimension(ventana_maestra)
        id_j1, id_j2 = gb.ID_SESION_JUGADOR_UNO, gb.ID_SESION_JUGADOR_DOS
        nombre_j1 = datos.obtener_nombre_jugador(id_j1)
        nombre_j2 = datos.obtener_nombre_jugador(id_j2)
        
        ficha_j1 = pp.pantalla_seleccion_pieza(ventana_maestra, nombre_j1, id_j1, True)
        ficha_j2 = pp.pantalla_seleccion_pieza(ventana_maestra, nombre_j2, id_j2, False)
        
        # 2. INICIALIZACIÓN DE PARTIDA
        tablero_actual = motor.crear_matriz_dinamica(dimension)
        reloj_fps = pygame.time.Clock()
        pos_j1, pos_j2 = None, None
        puntos_j1, puntos_j2 = 0, 0
        id_partida_bd, es_turno_blancas, partida_activa = 0, True, True
        pieza_seleccionada, movimientos_posibles = None, []
        historial_partida = []
        fase_juego = "COLOCACION"
        texto_pos_inicial_j1 = ""

        while partida_activa:
            ventana_maestra.fill((30, 32, 40))
            renderizar_interfaz_estetica(ventana_maestra, nombre_j1, id_j1, ficha_j1, puntos_j1, nombre_j2, id_j2, ficha_j2, puntos_j2, es_turno_blancas, historial_partida)
            interfaz.imprimir_tablero_dinamico(ventana_maestra, tablero_actual, dimension, movimientos_posibles, es_turno_blancas)
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    partida_activa, esta_jugando = False, False
                
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    coord = interfaz.convertir_posicion_a_coordenada(evento.pos, dimension)
                    if coord:
                        fila, col = int(coord[0]), int(coord[1])
                        
                        # --- FASE 1: COLOCACIÓN INICIAL ---
                        if fase_juego == "COLOCACION":
                            if pos_j1 is None:
                                if tablero_actual[fila][col] == gb.VACIO:
                                    texto_pos_inicial_j1 = interfaz.convertir_a_texto(fila, col, dimension)
                                    tablero_actual[fila][col], pos_j1 = ficha_j1, (fila, col)
                                    historial_partida.append(f"J1: {ficha_j1} en {texto_pos_inicial_j1}")
                                    es_turno_blancas = False
                            elif pos_j2 is None:
                                if tablero_actual[fila][col] == gb.VACIO:
                                    t_pos_j2 = interfaz.convertir_a_texto(fila, col, dimension)
                                    tablero_actual[fila][col], pos_j2 = ficha_j2, (fila, col)
                                    id_partida_bd = datos.registrar_juego_binario(texto_pos_inicial_j1, ficha_j1, t_pos_j2, ficha_j2)
                                    motor.generar_peones_ciegos(tablero_actual, dimension)
                                    historial_partida.append(f"J2: {ficha_j2} en {t_pos_j2}")
                                    historial_partida.append("--- PEONES LISTOS ---")
                                    es_turno_blancas, fase_juego = True, "ACCION"

                        # --- FASE 2: MOVIMIENTO Y CAPTURA ---
                        elif fase_juego == "ACCION":
                            if pieza_seleccionada is None:
                                ficha_detectada = tablero_actual[fila][col]
                                # Solo permitir seleccionar si es la ficha del jugador actual
                                if (es_turno_blancas and ficha_detectada == ficha_j1) or (not es_turno_blancas and ficha_detectada == ficha_j2):
                                    pieza_seleccionada = (fila, col)
                                    movimientos_posibles = motor.calcular_movimientos(fila, col, ficha_detectada, dimension, tablero_actual)
                                    if movimientos_posibles is None: movimientos_posibles = []
                            else:
                                # Si ya hay una pieza seleccionada, intentar moverla
                                if (fila, col) in movimientos_posibles:
                                    f_o, c_o = pieza_seleccionada
                                    target = tablero_actual[fila][col]
                                    
                                    # Calcular puntos (si el destino no está vacío y no es una pieza de jugador)
                                    puntos_ganados = 10 if (target != gb.VACIO and target not in [ficha_j1, ficha_j2]) else 0
                                    
                                    if es_turno_blancas: puntos_j1 += puntos_ganados
                                    else: puntos_j2 += puntos_ganados
                                    
                                    # Ejecutar movimiento en la matriz
                                    tablero_actual[fila][col] = tablero_actual[f_o][c_o]
                                    tablero_actual[f_o][c_o] = gb.VACIO
                                    
                                    # Registrar en BD e Historial
                                    t_dest = interfaz.convertir_a_texto(fila, col, dimension)
                                    datos.registrar_movimiento_binario(id_partida_bd, ficha_j1 if es_turno_blancas else ficha_j2, t_dest, puntos_ganados)
                                    historial_partida.append(f"{'J1' if es_turno_blancas else 'J2'}: -> {t_dest}")
                                    
                                    # Verificar victoria
                                    if puntos_j1 >= 40 or puntos_j2 >= 40:
                                        ganador = nombre_j1 if puntos_j1 >= 40 else nombre_j2
                                        datos.actualizar_puntos_jugador(id_j1 if puntos_j1 >= 40 else id_j2, max(puntos_j1, puntos_j2))
                                        
                                        # Pantalla final: decidir si volver a jugar o salir
                                        opcion = pp.pantalla_fin_partida(ventana_maestra, ganador)
                                        if opcion == "REINTENTAR":
                                            partida_activa = False # Sale al bucle de dimensión
                                        else:
                                            partida_activa, esta_jugando = False, False # Sale al menú
                                    else:
                                        # Cambio de turno real
                                        es_turno_blancas = not es_turno_blancas
                                    
                                    pieza_seleccionada, movimientos_posibles = None, []
                                else:
                                    # Si hace click fuera de los movimientos posibles, deseleccionar
                                    pieza_seleccionada, movimientos_posibles = None, []
                    else:
                        # Click fuera del tablero deselecciona
                        pieza_seleccionada, movimientos_posibles = None, []

            pygame.display.flip()
            reloj_fps.tick(60)

    return "MENU"