import pygame
import globales as gb

def ejecutar(ventana_principal):
    reloj_fotogramas = pygame.time.Clock()
    
    imagen_fondo_pantalla = gb.cargar_imagen("creditos.JPG", (gb.ANCHO_VENTANA, gb.ALTO_VENTANA))
    
    fuente_titulo_principal = pygame.font.SysFont("Arial", 45, bold=True)
    fuente_contenido_secundario = pygame.font.SysFont("Arial", 28, bold=False)
    fuente_instruccion_escape = pygame.font.SysFont("Consolas", 18, italic=True)

    lista_lineas_texto_creditos = [
        "PROYECTO AJEDREZ UCAB",
        "",
        "DESARROLLADO POR:",
        "Sebastian Rivas",
        "",
        "BAJO LA SUPERVISIÓN DE:",
        "Profesor Franklin Bello",
        "",
        "TECNOLOGÍAS UTILIZADAS:",
        "Python 3.x",
        "Pygame Library",
        "Estructuras Binarias (struct)",
        "",
        "DERECHOS RESERVADOS 2026",
        "",
        "GRACIAS POR JUGAR"
    ]

    posicion_vertical_texto_scroll = gb.ALTO_VENTANA
    velocidad_desplazamiento_pixeles = 1.5
    
    esta_ejecutando_creditos = True

    while esta_ejecutando_creditos:
        if imagen_fondo_pantalla:
            ventana_principal.blit(imagen_fondo_pantalla, (0, 0))
        else:
            ventana_principal.fill((15, 15, 25)) 

        superficie_overlay_oscuro = pygame.Surface((gb.ANCHO_VENTANA, gb.ALTO_VENTANA), pygame.SRCALPHA)
        superficie_overlay_oscuro.fill((0, 0, 0, 160)) 
        ventana_principal.blit(superficie_overlay_oscuro, (0, 0))

        for evento_pygame in pygame.event.get():
            if evento_pygame.type == pygame.QUIT:
                return "SALIR"
            if evento_pygame.type == pygame.KEYDOWN:
                if evento_pygame.key == pygame.K_ESCAPE or evento_pygame.key == pygame.K_RETURN:
                    esta_ejecutando_creditos = False

        posicion_vertical_texto_scroll -= velocidad_desplazamiento_pixeles
        
        limite_superior_desplazamiento = -(len(lista_lineas_texto_creditos) * 60)
        if posicion_vertical_texto_scroll < limite_superior_desplazamiento:
            posicion_vertical_texto_scroll = gb.ALTO_VENTANA

        for indice_linea, contenido_texto in enumerate(lista_lineas_texto_creditos):
            es_titulo_seccion = contenido_texto.isupper() and len(contenido_texto) > 0
            
            if es_titulo_seccion:
                superficie_texto_renderizado = fuente_titulo_principal.render(contenido_texto, True, (255, 215, 0)) # Dorado
            else:
                superficie_texto_renderizado = fuente_contenido_secundario.render(contenido_texto, True, (230, 230, 230)) # Gris claro

            coordenada_x_centrada = gb.ANCHO_VENTANA // 2 - superficie_texto_renderizado.get_width() // 2
            coordenada_y_dinamica = posicion_vertical_texto_scroll + (indice_linea * 60)
            
            if -50 < coordenada_y_dinamica < gb.ALTO_VENTANA + 50:
                ventana_principal.blit(superficie_texto_renderizado, (coordenada_x_centrada, coordenada_y_dinamica))

        pygame.draw.rect(ventana_principal, (0, 0, 0), (0, gb.ALTO_VENTANA - 40, gb.ANCHO_VENTANA, 40))
        superficie_instruccion = fuente_instruccion_escape.render("PRESIONE ESC O ENTER PARA VOLVER AL MENÚ", True, (200, 200, 200))
        ventana_principal.blit(superficie_instruccion, (gb.ANCHO_VENTANA // 2 - superficie_instruccion.get_width() // 2, gb.ALTO_VENTANA - 30))

        pygame.display.flip()
        reloj_fotogramas.tick(60) 