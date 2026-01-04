import pygame
import globales as gb
import struct

def validar_reglas_seguridad_clave(clave_texto, posicion_caracter=0, tiene_mayuscula=False, tiene_minuscula=False, tiene_numero=False, tiene_especial=False, contador_numeros=0):
    caracteres_especiales_validos = ["*", "=", "%", "_"]
    longitud_clave = len(clave_texto)
    if longitud_clave < 6 or longitud_clave > 10:
        return False, "Debe tener 6-10 caracteres."
    if posicion_caracter == longitud_clave:
        errores_encontrados = []
        if not tiene_mayuscula: errores_encontrados.append("mayúscula")
        if not tiene_minuscula: errores_encontrados.append("minúscula")
        if not tiene_numero:    errores_encontrados.append("número")
        if not tiene_especial:  errores_encontrados.append("especial")
        return (True, "") if len(errores_encontrados) == 0 else (False, "Falta: " + ", ".join(errores_encontrados))
    
    caracter_actual = clave_texto[posicion_caracter]
    if 'A' <= caracter_actual <= 'Z': tiene_mayuscula = True
    elif 'a' <= caracter_actual <= 'z': tiene_minuscula = True
    elif caracter_actual.isdigit():
        tiene_numero = True
        contador_numeros += 1
        if contador_numeros > 3: return False, "Máximo 3 números."
    elif caracter_actual in caracteres_especiales_validos: tiene_especial = True
    else: return False, f"Carácter '{caracter_actual}' no permitido."
    return validar_reglas_seguridad_clave(clave_texto, posicion_caracter + 1, tiene_mayuscula, tiene_minuscula, tiene_numero, tiene_especial, contador_numeros)

def transformar_clave_a_encriptada(clave_original):
    resultado_encriptado = ""
    for unidad_caracter in clave_original:
        resultado_encriptado += chr(ord(unidad_caracter) + 2)
    return resultado_encriptado

def comprobar_si_usuario_existe(cedula_a_buscar):
    usuario_encontrado = False
    try:
        with open(gb.ARCHIVO_USUARIOS, "rb") as archivo_binario:
            while True:
                bloque_datos = archivo_binario.read(gb.CANTIDAD_BYTES_REGISTRO)
                if not bloque_datos: break
                datos_desempaquetados = struct.unpack(gb.FORMATO_ESTRUCTURA_USUARIO, bloque_datos)
                cedula_en_archivo = datos_desempaquetados[0].decode('utf-8').replace('\x00', '').strip()
                if cedula_en_archivo == cedula_a_buscar.strip():
                    usuario_encontrado = True
                    break
    except FileNotFoundError: pass
    return usuario_encontrado

def validar_campo_actual(indice_campo, valor_campo):
    if not valor_campo.strip(): return False, "No puede estar vacío."
    if indice_campo == 0:
        if not valor_campo.replace(".", "").isdigit(): return False, "Solo números y puntos."
        if comprobar_si_usuario_existe(valor_campo): return False, "Cédula ya registrada."
    elif indice_campo == 1:
        if len(valor_campo) < 4: return False, "Mínimo 4 caracteres."
    elif indice_campo == 2:
        if valor_campo.lower() not in ['m', 'f']: return False, "Use 'M' o 'F'."
    elif indice_campo == 3:
        partes_fecha = valor_campo.split("/")
        if len(partes_fecha) != 3: return False, "Use DD/MM/AAAA."
    elif indice_campo == 4:
        if "@" not in valor_campo: return False, "Falta el '@'."
        if not (valor_campo.lower().endswith("gmail.com") or valor_campo.lower().endswith("hotmail.com")):
            return False, "Debe ser gmail o hotmail."
    elif indice_campo == 5:
        resultado_validacion, mensaje_error = validar_reglas_seguridad_clave(valor_campo)
        return resultado_validacion, mensaje_error
    return True, ""

def dibujar_campo_entrada(ventana, posicion_x, posicion_y, ancho_recuadro, etiqueta_texto, valor_actual, esta_activo, mensaje_error, mostrar_texto_real, posicion_cursor):
    fuente_etiqueta = pygame.font.SysFont("Arial", 18, bold=True)
    fuente_error = pygame.font.SysFont("Arial", 14, italic=True)
    
    color_borde = (0, 120, 215) if esta_activo else (200, 0, 0) if mensaje_error else (50, 50, 50)
    
    superficie_etiqueta = fuente_etiqueta.render(etiqueta_texto, True, (30, 30, 30))
    ventana.blit(superficie_etiqueta, (posicion_x, posicion_y - 25))
    
    pygame.draw.rect(ventana, (255, 255, 255), (posicion_x, posicion_y, ancho_recuadro, 35))
    pygame.draw.rect(ventana, color_borde, (posicion_x, posicion_y, ancho_recuadro, 35), 2 if esta_activo else 1)
    
    texto_visible = valor_actual if mostrar_texto_real else "*" * len(valor_actual)
    
    superficie_texto = fuente_etiqueta.render(texto_visible, True, (0, 0, 0))
    ventana.blit(superficie_texto, (posicion_x + 8, posicion_y + 8))

    if esta_activo and (pygame.time.get_ticks() // 500) % 2 == 0:
        texto_antes_cursor = texto_visible[:posicion_cursor]
        ancho_texto_antes = fuente_etiqueta.size(texto_antes_cursor)[0]
        pygame.draw.line(ventana, (0, 0, 0), (posicion_x + 8 + ancho_texto_antes, posicion_y + 6), (posicion_x + 8 + ancho_texto_antes, posicion_y + 28), 2)

    if mensaje_error and esta_activo:
        superficie_error = fuente_error.render(mensaje_error, True, (200, 0, 0))
        ventana.blit(superficie_error, (posicion_x + ancho_recuadro + 15, posicion_y + 8))

def mostrar_menu_confirmacion(ventana, pregunta_texto):
    fuente_pregunta = pygame.font.SysFont("Arial", 20, bold=True)
    recuadro_confirmacion = pygame.Rect(200, 250, 400, 150)
    while True:
        pygame.draw.rect(ventana, (255, 255, 255), recuadro_confirmacion, border_radius=10)
        pygame.draw.rect(ventana, (0, 0, 0), recuadro_confirmacion, 3, border_radius=10)
        texto_render = fuente_pregunta.render(pregunta_texto, True, (0, 0, 0))
        texto_opciones = fuente_pregunta.render("[S] Sí    [N] No", True, (0, 100, 0))
        ventana.blit(texto_render, (recuadro_confirmacion.centerx - texto_render.get_width()//2, recuadro_confirmacion.y + 40))
        ventana.blit(texto_opciones, (recuadro_confirmacion.centerx - texto_opciones.get_width()//2, recuadro_confirmacion.y + 85))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s: return True
                if evento.key == pygame.K_n: return False

def ejecutar(ventana):
    reloj_fotogramas = pygame.time.Clock()
    fuente_instrucciones = pygame.font.SysFont("Consolas", 14, bold=True)
    
    while True:
        lista_campos_formulario = [
            ["Cédula:", "", 180, False], ["Nombre:", "", 280, False],
            ["Sexo (M/F):", "", 60, False], ["Fecha:", "", 150, False],
            ["Correo:", "", 280, False], ["Clave (Manten 'V' para ver):", "", 180, True]
        ]
        indice_campo_activo = 0
        posicion_cursor_texto = 0
        mensaje_error_actual = ""
        finalizar_llenado_formulario = False

        while not finalizar_llenado_formulario:
            ventana.fill((235, 235, 235))
            pygame.draw.rect(ventana, (255, 255, 255), (40, 20, 720, 560), border_radius=15)
            pygame.draw.rect(ventana, (0, 0, 0), (40, 20, 720, 560), 2, border_radius=15)
            
            pygame.draw.rect(ventana, (40, 40, 40), (40, 540, 720, 40), border_bottom_left_radius=12, border_bottom_right_radius=12)
            guia = fuente_instrucciones.render("[TAB/ENTER] Campo | [FLECHAS] Mover Cursor | [ESC] Salir", True, (255, 255, 255))
            ventana.blit(guia, (gb.ANCHO_VENTANA//2 - guia.get_width()//2, 550))
            
            estado_teclas = pygame.key.get_pressed()
            esta_presionada_tecla_ver = estado_teclas[pygame.K_v]

            posicion_vertical_actual = 80
            for i in range(len(lista_campos_formulario)):
                debe_mostrar_texto = (i != 5 or esta_presionada_tecla_ver)
                dibujar_campo_entrada(ventana, 80, posicion_vertical_actual, 
                                     lista_campos_formulario[i][2], lista_campos_formulario[i][0], 
                                     lista_campos_formulario[i][1], indice_campo_activo == i, 
                                     mensaje_error_actual if i == indice_campo_activo else "", debe_mostrar_texto, posicion_cursor_texto)
                posicion_vertical_actual += 75

            pygame.display.flip()

            for evento_pygame in pygame.event.get():
                if evento_pygame.type == pygame.QUIT: return "SALIR"
                if evento_pygame.type == pygame.KEYDOWN:
                    if evento_pygame.key == pygame.K_ESCAPE: return "MENU"
                    
                    elif evento_pygame.key == pygame.K_RIGHT:
                        if posicion_cursor_texto < len(lista_campos_formulario[indice_campo_activo][1]):
                            posicion_cursor_texto += 1
                    elif evento_pygame.key == pygame.K_LEFT:
                        if posicion_cursor_texto > 0:
                            posicion_cursor_texto -= 1
                    
                    elif evento_pygame.key in [pygame.K_TAB, pygame.K_RETURN]:
                        resultado_es_valido, mensaje_de_error = validar_campo_actual(indice_campo_activo, lista_campos_formulario[indice_campo_activo][1])
                        if resultado_es_valido:
                            mensaje_error_actual = ""
                            if indice_campo_activo < len(lista_campos_formulario) - 1:
                                indice_campo_activo += 1
                                posicion_cursor_texto = len(lista_campos_formulario[indice_campo_activo][1])
                            else:
                                cedula, nombre, sexo, fecha, correo, clave = [campo[1].strip() for campo in lista_campos_formulario]
                                if mostrar_menu_confirmacion(ventana, "¿Desea encriptar su clave?"):
                                    clave = transformar_clave_a_encriptada(clave)
                                
                                registro_empaquetado = struct.pack(gb.FORMATO_ESTRUCTURA_USUARIO, 
                                    cedula.encode('utf-8'), nombre.encode('utf-8'), sexo.encode('utf-8'), 
                                    fecha.encode('utf-8'), clave.encode('utf-8'), correo.encode('utf-8'))
                                with open(gb.ARCHIVO_USUARIOS, "ab") as archivo_salida: archivo_salida.write(registro_empaquetado)
                                if mostrar_menu_confirmacion(ventana, "¿Registrar a otro jugador?"):
                                    finalizar_llenado_formulario = True 
                                else: return "MENU"
                        else: mensaje_error_actual = mensaje_de_error
                    
                    elif evento_pygame.key == pygame.K_BACKSPACE:
                        if posicion_cursor_texto > 0:
                            texto_actual = lista_campos_formulario[indice_campo_activo][1]
                            nuevo_texto = texto_actual[:posicion_cursor_texto-1] + texto_actual[posicion_cursor_texto:]
                            lista_campos_formulario[indice_campo_activo][1] = nuevo_texto
                            posicion_cursor_texto -= 1
                            
                    elif evento_pygame.key == pygame.K_DELETE:
                        if posicion_cursor_texto < len(lista_campos_formulario[indice_campo_activo][1]):
                            texto_actual = lista_campos_formulario[indice_campo_activo][1]
                            nuevo_texto = texto_actual[:posicion_cursor_texto] + texto_actual[posicion_cursor_texto+1:]
                            lista_campos_formulario[indice_campo_activo][1] = nuevo_texto

                    else:
                        if len(lista_campos_formulario[indice_campo_activo][1]) < 30 and evento_pygame.unicode.isprintable():
                            if not (evento_pygame.key == pygame.K_v and indice_campo_activo == 5):
                                texto_actual = lista_campos_formulario[indice_campo_activo][1]
                                nuevo_texto = texto_actual[:posicion_cursor_texto] + evento_pygame.unicode + texto_actual[posicion_cursor_texto:]
                                lista_campos_formulario[indice_campo_activo][1] = nuevo_texto
                                posicion_cursor_texto += 1
                                mensaje_error_actual = ""
            reloj_fotogramas.tick(30)