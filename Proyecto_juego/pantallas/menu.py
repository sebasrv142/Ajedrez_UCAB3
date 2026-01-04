import pygame
import globales as gb

def ejecutar(ventana_interfaz_principal):
    reloj_controlador_tiempo = pygame.time.Clock()
    
    imagen_fondo_menu = gb.cargar_imagen("menu.JPG", (gb.ANCHO_VENTANA, gb.ALTO_VENTANA))
    fuente_opciones_menu = pygame.font.SysFont("Arial", 30, bold=True)
    
    lista_nombres_opciones = ["REGISTRAR JUGADOR", "INICIAR SESIÓN", "REPORTES", "CRÉDITOS", "SALIR"]
    lista_identificadores_estados = ["REGISTRO", "LOGIN", "REPORTES", "CREDITOS", "SALIR"]
    
    indice_opcion_seleccionada = 0
    esta_en_menu_principal = True
    
    while esta_en_menu_principal:
        if imagen_fondo_menu:
            ventana_interfaz_principal.blit(imagen_fondo_menu, (0, 0))
        else:
            ventana_interfaz_principal.fill((40, 40, 45))
            
        posicion_x_contenedor = 50
        posicion_y_contenedor = 80
        ancho_contenedor_opciones = 450
        alto_contenedor_opciones = 460
        
        pygame.draw.rect(ventana_interfaz_principal, (255, 255, 255), 
                         (posicion_x_contenedor, posicion_y_contenedor, ancho_contenedor_opciones, alto_contenedor_opciones), 
                         border_radius=15)
        
        pygame.draw.rect(ventana_interfaz_principal, (0, 0, 0), 
                         (posicion_x_contenedor, posicion_y_contenedor, ancho_contenedor_opciones, alto_contenedor_opciones), 
                         6, border_radius=15)
        
        for indice_recorrido, texto_opcion in enumerate(lista_nombres_opciones):
            distancia_vertical_entre_opciones = 90
            posicion_y_base_texto = 135 + (indice_recorrido * distancia_vertical_entre_opciones)
            
            if indice_recorrido == indice_opcion_seleccionada:
                color_texto_actual = (200, 0, 0)
                
                punto_superior_puntero = (posicion_x_contenedor + 20, posicion_y_base_texto - 10)
                punto_inferior_puntero = (posicion_x_contenedor + 20, posicion_y_base_texto + 15)
                punto_derecho_puntero = (posicion_x_contenedor + 45, posicion_y_base_texto + 2)
                
                lista_puntos_puntero_triangular = [punto_superior_puntero, punto_inferior_puntero, punto_derecho_puntero]
                
                pygame.draw.polygon(ventana_interfaz_principal, color_texto_actual, lista_puntos_puntero_triangular)
                posicion_x_renderizado_texto = posicion_x_contenedor + 65
            else:
                color_texto_actual = (30, 30, 30)
                posicion_x_renderizado_texto = posicion_x_contenedor + 60
                
            superficie_texto_opcion = fuente_opciones_menu.render(texto_opcion, True, color_texto_actual)
            ventana_interfaz_principal.blit(superficie_texto_opcion, (posicion_x_renderizado_texto, posicion_y_base_texto - 5))
            
        pygame.display.flip()
        
        for evento_sistema in pygame.event.get():
            if evento_sistema.type == pygame.QUIT:
                return "SALIR"
                
            if evento_sistema.type == pygame.KEYDOWN:
                if evento_sistema.key == pygame.K_UP:
                    indice_opcion_seleccionada = (indice_opcion_seleccionada - 1) % len(lista_nombres_opciones)
                
                elif evento_sistema.key == pygame.K_DOWN:
                    indice_opcion_seleccionada = (indice_opcion_seleccionada + 1) % len(lista_nombres_opciones)
                
                elif evento_sistema.key == pygame.K_RETURN:
                    return lista_identificadores_estados[indice_opcion_seleccionada]
                    
                elif evento_sistema.key == pygame.K_ESCAPE:
                    return "SALIR"
                    
        reloj_controlador_tiempo.tick(30)