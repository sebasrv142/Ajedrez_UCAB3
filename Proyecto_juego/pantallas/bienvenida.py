import pygame
import globales as gb

def ejecutar(ventana_principal_juego):
    reloj_controlador_fotogramas = pygame.time.Clock()
    
    imagen_logo_central = gb.cargar_imagen("logo.PNG", (300, 300))
    
    fuente_titulo_ajedrez = pygame.font.SysFont("Arial Black", 55)
    fuente_instruccion_inicio = pygame.font.SysFont("Consolas", 22)
    
    nivel_transparencia_aparicion = 0
    velocidad_aparicion_suave = 5
    
    numero_fotogramas_transcurridos = 0
    esperando_entrada_usuario = True
    
    while esperando_entrada_usuario:
        ventana_principal_juego.fill((15, 15, 15))
        
        if nivel_transparencia_aparicion < 255:
            nivel_transparencia_aparicion += velocidad_aparicion_suave
            
        superficie_logo_transparente = imagen_logo_central.copy()
        superficie_logo_transparente.set_alpha(nivel_transparencia_aparicion)
        
        posicion_centro_horizontal_logo = gb.ANCHO_VENTANA // 2 - 150
        posicion_vertical_logo = 60
        
        if imagen_logo_central:
            ventana_principal_juego.blit(superficie_logo_transparente, (posicion_centro_horizontal_logo, posicion_vertical_logo))
        
        superficie_texto_titulo = fuente_titulo_ajedrez.render("AJEDREZ UCAB", True, (255, 215, 0))
        superficie_texto_titulo.set_alpha(nivel_transparencia_aparicion)
        
        posicion_x_titulo = gb.ANCHO_VENTANA // 2 - superficie_texto_titulo.get_width() // 2
        posicion_y_titulo = 380
        
        ventana_principal_juego.blit(superficie_texto_titulo, (posicion_x_titulo, posicion_y_titulo))
        
        numero_fotogramas_transcurridos += 1
        frecuencia_parpadeo_texto = (numero_fotogramas_transcurridos // 40) % 2
        
        if frecuencia_parpadeo_texto == 0 and nivel_transparencia_aparicion >= 255:
            superficie_texto_instruccion = fuente_instruccion_inicio.render("PRESIONE CUALQUIER TECLA PARA COMENZAR", True, (220, 220, 220))
            
            posicion_x_instruccion = gb.ANCHO_VENTANA // 2 - superficie_texto_instruccion.get_width() // 2
            posicion_y_instruccion = 520
            
            ventana_principal_juego.blit(superficie_texto_instruccion, (posicion_x_instruccion, posicion_y_instruccion))
        
        pygame.display.flip()
        
        for evento_sistema in pygame.event.get():
            if evento_sistema.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if evento_sistema.type == pygame.KEYDOWN or evento_sistema.type == pygame.MOUSEBUTTONDOWN:
                if nivel_transparencia_aparicion >= 100:
                    esperando_entrada_usuario = False
                    
        reloj_controlador_fotogramas.tick(60)