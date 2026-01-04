import pygame
import globales as gb
import struct

def realizar_desencriptacion_clave(cadena_clave_encriptada):
    resultado_clave_original = ""
    for unidad_caracter in cadena_clave_encriptada:
        resultado_clave_original += chr(ord(unidad_caracter) - 2)
    return resultado_clave_original

def buscar_usuario_en_archivo_binario(cedula_proporcionada, clave_proporcionada):
    datos_completos_usuario = None
    try:
        with open(gb.ARCHIVO_USUARIOS, "rb") as archivo_binario_usuarios:
            while True:
                bloque_registro_binario = archivo_binario_usuarios.read(gb.CANTIDAD_BYTES_REGISTRO)
                if not bloque_registro_binario:
                    break
                
                datos_extraidos = struct.unpack(gb.FORMATO_ESTRUCTURA_USUARIO, bloque_registro_binario)
                cedula_en_archivo = datos_extraidos[0].decode('utf-8').replace('\x00', '').strip()
                
                if cedula_en_archivo == cedula_proporcionada.strip():
                    clave_en_archivo = datos_extraidos[4].decode('utf-8').replace('\x00', '').strip()
                    clave_desencriptada = realizar_desencriptacion_clave(clave_en_archivo)
                    
                    if clave_en_archivo == clave_proporcionada or clave_desencriptada == clave_proporcionada:
                        datos_completos_usuario = datos_extraidos
                        break
    except FileNotFoundError:
        pass
    return datos_completos_usuario

def dibujar_interfaz_entrada_login(ventana, x_pos, y_pos, etiqueta, valor, activo, error, mostrar_real, cursor_pos):
    fuente_etiquetas = pygame.font.SysFont("Arial", 20, bold=True)
    fuente_errores = pygame.font.SysFont("Arial", 14, italic=True)
    
    color_borde_recuadro = (0, 120, 215) if activo else (200, 0, 0) if error else (70, 70, 70)
    
    superficie_etiqueta = fuente_etiquetas.render(etiqueta, True, (40, 40, 40))
    ventana.blit(superficie_etiqueta, (x_pos, y_pos - 30))
    
    pygame.draw.rect(ventana, (255, 255, 255), (x_pos, y_pos, 350, 40), border_radius=5)
    pygame.draw.rect(ventana, color_borde_recuadro, (x_pos, y_pos, 350, 40), 2, border_radius=5)
    
    texto_a_dibujar = valor if mostrar_real else "*" * len(valor)
    superficie_texto = fuente_etiquetas.render(texto_a_dibujar, True, (0, 0, 0))
    ventana.blit(superficie_texto, (x_pos + 10, y_pos + 8))
    
    if activo and (pygame.time.get_ticks() // 500) % 2 == 0:
        texto_previo_al_cursor = texto_a_dibujar[:cursor_pos]
        ancho_previo = fuente_etiquetas.size(texto_previo_al_cursor)[0]
        pygame.draw.line(ventana, (0, 0, 0), (x_pos + 10 + ancho_previo, y_pos + 8), (x_pos + 10 + ancho_previo, y_pos + 32), 2)

    if error and activo:
        superficie_mensaje_error = fuente_errores.render(error, True, (200, 0, 0))
        ventana.blit(superficie_mensaje_error, (x_pos, y_pos + 45))

def ejecutar(ventana_juego):
    controlador_tiempo_fps = pygame.time.Clock()
    fuente_instrucciones_inferior = pygame.font.SysFont("Consolas", 16, bold=True)
    fuente_encabezado_jugador = pygame.font.SysFont("Arial", 35, bold=True)
    
    identificador_jugador_actual = 1
    
    while identificador_jugador_actual <= 2:
        lista_campos_login = [["Cédula:", "", 0], ["Clave (Mantener V):", "", 0]]
        indice_campo_en_foco = 0
        mensaje_notificacion_error = ""
        autenticacion_completada = False
        
        while not autenticacion_completada:
            ventana_juego.fill((230, 230, 230))
            pygame.draw.rect(ventana_juego, (255, 255, 255), (100, 50, 600, 500), border_radius=20)
            pygame.draw.rect(ventana_juego, (0, 0, 0), (100, 50, 600, 500), 3, border_radius=20)
            
            texto_jugador = f"AUTENTICACIÓN JUGADOR {identificador_jugador_actual}"
            superficie_encabezado = fuente_encabezado_jugador.render(texto_jugador, True, (0, 51, 102))
            ventana_juego.blit(superficie_encabezado, (gb.ANCHO_VENTANA//2 - superficie_encabezado.get_width()//2, 80))
            
            estado_teclado = pygame.key.get_pressed()
            esta_activada_vision_clave = estado_teclado[pygame.K_v]
            
            for indice_iteracion, datos_campo in enumerate(lista_campos_login):
                es_campo_clave = (indice_iteracion == 1)
                debe_revelar_contenido = (not es_campo_clave or esta_activada_vision_clave)
                
                dibujar_interfaz_entrada_login(ventana_juego, 225, 200 + (indice_iteracion * 120), 
                                               datos_campo[0], datos_campo[1], 
                                               indice_campo_en_foco == indice_iteracion, 
                                               mensaje_notificacion_error if indice_campo_en_foco == indice_iteracion else "",
                                               debe_revelar_contenido, datos_campo[2])

            pygame.draw.rect(ventana_juego, (50, 50, 50), (100, 510, 600, 40), border_bottom_left_radius=18, border_bottom_right_radius=18)
            guia_texto = fuente_instrucciones_inferior.render("[ENTER] Validar | [FLECHAS] Cursor | [ESC] Volver", True, (255, 255, 255))
            ventana_juego.blit(guia_texto, (gb.ANCHO_VENTANA//2 - guia_texto.get_width()//2, 520))
            
            pygame.display.flip()
            
            for evento_actual in pygame.event.get():
                if evento_actual.type == pygame.QUIT: return "SALIR"
                if evento_actual.type == pygame.KEYDOWN:
                    if evento_actual.key == pygame.K_ESCAPE: return "MENU"
                    
                    elif evento_actual.key == pygame.K_RIGHT:
                        if lista_campos_login[indice_campo_en_foco][2] < len(lista_campos_login[indice_campo_en_foco][1]):
                            lista_campos_login[indice_campo_en_foco][2] += 1
                    elif evento_actual.key == pygame.K_LEFT:
                        if lista_campos_login[indice_campo_en_foco][2] > 0:
                            lista_campos_login[indice_campo_en_foco][2] -= 1
                            
                    elif evento_actual.key in [pygame.K_TAB, pygame.K_RETURN]:
                        if indice_campo_en_foco == 0:
                            if not lista_campos_login[0][1].strip():
                                mensaje_notificacion_error = "Ingrese su cédula."
                            else:
                                indice_campo_en_foco = 1
                                lista_campos_login[1][2] = len(lista_campos_login[1][1])
                        else:
                            cedula_final = lista_campos_login[0][1]
                            clave_final = lista_campos_login[1][1]
                            datos_verificados = buscar_usuario_en_archivo_binario(cedula_final, clave_final)
                            
                            if datos_verificados:
                                if identificador_jugador_actual == 2 and cedula_final == gb.ID_SESION_JUGADOR_UNO:
                                    mensaje_notificacion_error = "Debe ser un jugador distinto."
                                else:
                                    if identificador_jugador_actual == 1: gb.ID_SESION_JUGADOR_UNO = cedula_final
                                    else: gb.ID_SESION_JUGADOR_DOS = cedula_final
                                    autenticacion_completada = True
                            else:
                                mensaje_notificacion_error = "Cédula o Clave incorrecta."
                                
                    elif evento_actual.key == pygame.K_BACKSPACE:
                        pos = lista_campos_login[indice_campo_en_foco][2]
                        if pos > 0:
                            txt = lista_campos_login[indice_campo_en_foco][1]
                            lista_campos_login[indice_campo_en_foco][1] = txt[:pos-1] + txt[pos:]
                            lista_campos_login[indice_campo_en_foco][2] -= 1
                    else:
                        if len(lista_campos_login[indice_campo_en_foco][1]) < 20 and evento_actual.unicode.isprintable():
                            if not (evento_actual.key == pygame.K_v and indice_campo_en_foco == 1):
                                pos = lista_campos_login[indice_campo_en_foco][2]
                                txt = lista_campos_login[indice_campo_en_foco][1]
                                lista_campos_login[indice_campo_en_foco][1] = txt[:pos] + evento_actual.unicode + txt[pos:]
                                lista_campos_login[indice_campo_en_foco][2] += 1
                                mensaje_notificacion_error = ""
            controlador_tiempo_fps.tick(60)
        identificador_jugador_actual += 1
    return "JUEGO"