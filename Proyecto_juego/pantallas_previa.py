import pygame
import globales as gb

def pantalla_seleccion_dimension(ventana):
    fuente_titulo = pygame.font.SysFont("Arial", 30, bold=True)
    fuente_opcion = pygame.font.SysFont("Arial", 25)
    opciones = [8, 10, 12, 14]
    indice = 0
    seleccionando = True
    while seleccionando:
        ventana.fill((30, 32, 40))
        txt_titulo = fuente_titulo.render("SELECCIONA EL TAMAÑO DEL TABLERO", True, (255, 255, 255))
        ventana.blit(txt_titulo, (gb.ANCHO_VENTANA // 2 - txt_titulo.get_width() // 2, 150))
        for i, opt in enumerate(opciones):
            color = (0, 255, 0) if i == indice else (150, 150, 150)
            txt_opt = fuente_opcion.render(f"{opt} x {opt}", True, color)
            ventana.blit(txt_opt, (gb.ANCHO_VENTANA // 2 - txt_opt.get_width() // 2, 250 + (i * 50)))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP: indice = (indice - 1) % len(opciones)
                if evento.key == pygame.K_DOWN: indice = (indice + 1) % len(opciones)
                if evento.key == pygame.K_RETURN: return opciones[indice]
        pygame.display.flip()

def pantalla_seleccion_pieza(ventana, nombre_jugador, id_jugador, es_blancas):
    fuente_titulo = pygame.font.SysFont("Arial", 25, bold=True)
    fuente_piezas = pygame.font.SysFont("Arial", 18, bold=True)
    if es_blancas:
        opciones = [('Torre', 'T', 'B_Torre'), ('Caballo', 'C', 'B_Caballo'), ('Alfil', 'A', 'B_Alfil'), ('Dama', 'D', 'B_Dama')]
    else:
        opciones = [('Torre', 't', 'N_Torre'), ('Caballo', 'c', 'N_Caballo'), ('Alfil', 'a', 'N_Alfil'), ('Dama', 'd', 'N_Dama')]
    imagenes_seleccion = []
    for nombre, letra, archivo in opciones:
        try:
            img = pygame.image.load(f"assets/{archivo}.png").convert_alpha()
            img = pygame.transform.scale(img, (60, 60))
            imagenes_seleccion.append(img)
        except:
            imagenes_seleccion.append(None)
    seleccionando = True
    indice = 0
    while seleccionando:
        ventana.fill((30, 32, 40))
        titulo = fuente_titulo.render(f"{nombre_jugador}, elige tu pieza", True, (255, 255, 255))
        ventana.blit(titulo, (gb.ANCHO_VENTANA // 2 - titulo.get_width() // 2, 80))
        for i, (nombre, letra, archivo) in enumerate(opciones):
            x_pos = 100 + (i * 150)
            y_pos = 220
            color_recuadro = (0, 255, 0) if i == indice else (70, 70, 80)
            rect = pygame.Rect(x_pos - 15, y_pos - 15, 90, 120)
            pygame.draw.rect(ventana, color_recuadro, rect, 3, border_radius=10)
            if imagenes_seleccion[i]:
                ventana.blit(imagenes_seleccion[i], (x_pos, y_pos))
            else:
                txt_letra = fuente_piezas.render(letra, True, (255, 255, 255))
                ventana.blit(txt_letra, (x_pos + 25, y_pos + 20))
            txt_nom = fuente_piezas.render(nombre, True, (200, 200, 200))
            ventana.blit(txt_nom, (x_pos + 45 - txt_nom.get_width() // 2, y_pos + 80))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT: indice = (indice - 1) % len(opciones)
                if evento.key == pygame.K_RIGHT: indice = (indice + 1) % len(opciones)
                if evento.key == pygame.K_RETURN: return opciones[indice][1]
        pygame.display.flip()

def pantalla_fin_partida(ventana, ganador):
    fuente_fin = pygame.font.SysFont("Arial", 40, bold=True)
    fuente_opcion = pygame.font.SysFont("Arial", 25)
    opciones = ["REINTENTAR", "MENU PRINCIPAL"]
    indice = 0
    while True:
        ventana.fill((20, 20, 30))
        txt_ganador = fuente_fin.render(f"¡GANADOR: {ganador}!", True, (255, 255, 0))
        ventana.blit(txt_ganador, (gb.ANCHO_VENTANA // 2 - txt_ganador.get_width() // 2, 150))
        
        for i, opt in enumerate(opciones):
            color = (0, 255, 0) if i == indice else (255, 255, 255)
            txt_opt = fuente_opcion.render(opt, True, color)
            ventana.blit(txt_opt, (gb.ANCHO_VENTANA // 2 - txt_opt.get_width() // 2, 300 + (i * 60)))
            
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP: indice = (indice - 1) % len(opciones)
                if evento.key == pygame.K_DOWN: indice = (indice + 1) % len(opciones)
                if evento.key == pygame.K_RETURN:
                    if indice == 0: return "REINTENTAR"
                    else: return "MENU"
        pygame.display.flip()