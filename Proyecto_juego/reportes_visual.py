import pygame
import struct
import globales as gb

def quicksort_piezas(lista):
    if len(lista) <= 1: return lista
    pivote = lista[len(lista) // 2]
    izq = [x for x in lista if x["movs"] > pivote["movs"]]
    centro = [x for x in lista if x["movs"] == pivote["movs"]]
    der = [x for x in lista if x["movs"] < pivote["movs"]]
    return quicksort_piezas(izq) + centro + quicksort_piezas(der)

def buscar_jugador_por_cedula(cedula_buscada):
    jugador = None
    # Limpiamos la cédula buscada de puntos y guiones para comparar valores puros
    ced_buscada_limpia = cedula_buscada.replace(".", "").replace("-", "").strip()
    
    try:
        with open(gb.ARCHIVO_USUARIOS, "rb") as f:
            encontrado = False
            bloque = f.read(gb.CANTIDAD_BYTES_REGISTRO)
            while bloque and not encontrado:
                d = struct.unpack(gb.FORMATO_ESTRUCTURA_USUARIO, bloque)
                ced_bd = d[0].decode('utf-8').strip('\x00').strip()
                ced_bd_limpia = ced_bd.replace(".", "").replace("-", "")
                
                if ced_bd_limpia == ced_buscada_limpia:
                    jugador = {
                        "cedula": ced_bd,
                        "nombre": d[1].decode('utf-8').strip('\x00').strip(),
                        "correo": d[5].decode('utf-8').strip('\x00').strip(),
                        "puntos_totales": 0,
                        "pieza_mas_usada": "N/A"
                    }
                    encontrado = True
                else:
                    bloque = f.read(gb.CANTIDAD_BYTES_REGISTRO)
    except: pass

    if jugador:
        # Calcular puntos totales
        try:
            with open(gb.ARCHIVO_JUEGOS, "rb") as fj:
                bj = fj.read(gb.CANTIDAD_BYTES_JUEGO)
                while bj:
                    dj = struct.unpack(gb.FORMATO_REGISTRO_JUEGO, bj)
                    c1 = dj[2].decode('utf-8').strip('\x00').strip().replace(".", "").replace("-", "")
                    c2 = dj[5].decode('utf-8').strip('\x00').strip().replace(".", "").replace("-", "")
                    if ced_buscada_limpia == c1: jugador["puntos_totales"] += dj[3]
                    if ced_buscada_limpia == c2: jugador["puntos_totales"] += dj[6]
                    bj = fj.read(gb.CANTIDAD_BYTES_JUEGO)
        except: pass

        # Pieza más usada
        conteo_piezas = {}
        nombres_p = {"P": "Peon B", "T": "Torre B", "C": "Caballo B", "A": "Alfil B", "Q": "Dama B", "R": "Rey B",
                     "p": "Peon N", "t": "Torre N", "c": "Caballo N", "a": "Alfil N", "q": "Dama N", "r": "Rey N"}
        try:
            with open(gb.ARCHIVO_MOVIMIENTOS, "rb") as fm:
                bm = fm.read(gb.CANTIDAD_BYTES_MOVIMIENTO)
                while bm:
                    dm = struct.unpack(gb.FORMATO_MOVIMIENTO, bm)
                    pid = dm[1].decode('utf-8').strip('\x00').strip()
                    conteo_piezas[pid] = conteo_piezas.get(pid, 0) + 1
                    bm = fm.read(gb.CANTIDAD_BYTES_MOVIMIENTO)
            if conteo_piezas:
                mejor_id = max(conteo_piezas, key=conteo_piezas.get)
                jugador["pieza_mas_usada"] = nombres_p.get(mejor_id, mejor_id)
        except: pass

    return jugador

def reporte_a_datos():
    lista = []
    try:
        with open(gb.ARCHIVO_USUARIOS, "rb") as f:
            bu = f.read(gb.CANTIDAD_BYTES_REGISTRO)
            while bu:
                du = struct.unpack(gb.FORMATO_ESTRUCTURA_USUARIO, bu)
                ced = du[0].decode('utf-8').strip('\x00').strip()
                nom = du[1].decode('utf-8').strip('\x00').strip()
                cont = 0
                try:
                    with open(gb.ARCHIVO_JUEGOS, "rb") as fj:
                        bj = fj.read(gb.CANTIDAD_BYTES_JUEGO)
                        while bj:
                            dj = struct.unpack(gb.FORMATO_REGISTRO_JUEGO, bj)
                            c1_limp = dj[2].decode('utf-8').strip('\x00').strip().replace(".", "").replace("-", "")
                            c2_limp = dj[5].decode('utf-8').strip('\x00').strip().replace(".", "").replace("-", "")
                            ced_limp = ced.replace(".", "").replace("-", "")
                            if ced_limp in [c1_limp, c2_limp]:
                                cont += 1
                            bj = fj.read(gb.CANTIDAD_BYTES_JUEGO)
                except: pass
                lista.append({"cedula": ced, "nombre": nom, "participaciones": cont})
                bu = f.read(gb.CANTIDAD_BYTES_REGISTRO)
    except: pass
    return lista

def reporte_c_piezas():
    conteo = {"P": 0, "T": 0, "C": 0, "A": 0, "Q": 0, "R": 0, "p": 0, "t": 0, "c": 0, "a": 0, "q": 0, "r": 0}
    nombres = {"P": "Peon B", "T": "Torre B", "C": "Caballo B", "A": "Alfil B", "Q": "Dama B", "R": "Rey B",
               "p": "Peon N", "t": "Torre N", "c": "Caballo N", "a": "Alfil N", "q": "Dama N", "r": "Rey N"}
    try:
        with open(gb.ARCHIVO_MOVIMIENTOS, "rb") as f:
            bm = f.read(gb.CANTIDAD_BYTES_MOVIMIENTO)
            while bm:
                dm = struct.unpack(gb.FORMATO_MOVIMIENTO, bm)
                pid = dm[1].decode('utf-8').strip('\x00').strip()
                if pid in conteo: conteo[pid] += 1
                bm = f.read(gb.CANTIDAD_BYTES_MOVIMIENTO)
    except: pass
    lista = [{"nombre": nombres.get(k, k), "movs": v} for k, v in conteo.items() if v > 0]
    return quicksort_piezas(lista)[:5]

def pantalla_reportes(ventana):
    f_tit = pygame.font.SysFont("Arial", 26, bold=True)
    f_sub = pygame.font.SysFont("Arial", 20, bold=True)
    f_txt = pygame.font.SysFont("Courier New", 18)
    reloj = pygame.time.Clock()
    
    menu_actual = "PRINCIPAL"
    opciones_menu = ["Listado de Participaciones", "Busqueda por Cedula", "Top 5 Piezas mas Movidas", "Volver"]
    indice_sel = 0
    scroll_y = 0
    input_cedula = ""
    resultado_busqueda = None
    datos_listado, datos_top = [], []
    ejecutando = True

    while ejecutando:
        ventana.fill((30, 32, 45))
        
        if menu_actual == "PRINCIPAL":
            ventana.blit(f_tit.render("PANEL DE REPORTES", True, (0, 255, 255)), (50, 50))
            for i, o in enumerate(opciones_menu):
                color_bg = (60, 70, 100) if i == indice_sel else (45, 50, 70)
                rect = pygame.Rect(50, 140 + i*60, 500, 45)
                pygame.draw.rect(ventana, color_bg, rect, border_radius=8)
                if i == indice_sel: pygame.draw.rect(ventana, (0, 255, 0), rect, 2, border_radius=8)
                ventana.blit(f_sub.render(o, True, (255, 255, 255)), (70, 150 + i*60))

        elif menu_actual == "LISTADO":
            ventana.blit(f_tit.render("LISTADO DE PARTICIPACIONES", True, (255, 255, 0)), (50, 20))
            pygame.draw.rect(ventana, (40, 45, 60), (50, 70, 700, 410))
            cabecera = f"{'CEDULA':<15} {'NOMBRE':<25} {'PARTIDAS'}"
            ventana.blit(f_txt.render(cabecera, True, (0, 255, 0)), (70, 80))
            y_base = 115
            for i, d in enumerate(datos_listado):
                y_pos = y_base + (i * 25) - scroll_y
                if 110 < y_pos < 460:
                    linea = f"{d['cedula']:<15} {d['nombre']:<25} {d['participaciones']:>8}"
                    ventana.blit(f_txt.render(linea, True, (255, 255, 255)), (70, y_pos))
            ventana.blit(f_txt.render("Flechas: Scroll | ESC: Salir", True, (200, 200, 200)), (50, 500))

        elif menu_actual == "BUSQUEDA":
            ventana.blit(f_tit.render("BUSQUEDA POR CEDULA", True, (255, 255, 0)), (50, 40))
            ventana.blit(f_sub.render("Cédula (permite puntos):", True, (255, 255, 255)), (50, 110))
            pygame.draw.rect(ventana, (255, 255, 255), (50, 140, 350, 40), border_radius=5)
            ventana.blit(f_txt.render(input_cedula + "|", True, (0, 0, 0)), (60, 150))
            
            if resultado_busqueda:
                pygame.draw.rect(ventana, (45, 50, 70), (50, 210, 550, 240), border_radius=10)
                ventana.blit(f_txt.render(f"Nombre:   {resultado_busqueda['nombre']}", True, (255, 255, 255)), (70, 240))
                ventana.blit(f_txt.render(f"Cédula:   {resultado_busqueda['cedula']}", True, (255, 255, 255)), (70, 275))
                ventana.blit(f_txt.render(f"Pts Tot:  {resultado_busqueda['puntos_totales']}", True, (0, 255, 255)), (70, 345))
                ventana.blit(f_txt.render(f"Favorita: {resultado_busqueda['pieza_mas_usada']}", True, (255, 255, 0)), (70, 380))
            elif resultado_busqueda == False:
                ventana.blit(f_txt.render("Jugador no encontrado.", True, (255, 100, 100)), (50, 210))
            
            ventana.blit(f_txt.render("ENTER: Buscar | ESC: Volver", True, (200, 200, 200)), (50, 500))

        elif menu_actual == "TOP5":
            ventana.blit(f_tit.render("TOP 5 PIEZAS MAS USADAS", True, (255, 255, 0)), (50, 40))
            for i, p in enumerate(datos_top):
                y_p = 130 + (i * 60)
                pygame.draw.rect(ventana, (45, 50, 70), (70, y_p, 500, 45), border_radius=5)
                ventana.blit(f_txt.render(f"{i+1}. {p['nombre']}: {p['movs']} movs", True, (255, 255, 255)), (85, y_p+12))
            ventana.blit(f_txt.render("ESC: Volver", True, (200, 200, 200)), (50, 500))

        # Gestión de eventos sin break
        eventos = pygame.event.get()
        for ev in eventos:
            if ev.type == pygame.QUIT:
                ejecutando = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    menu_actual = "PRINCIPAL"
                elif menu_actual == "PRINCIPAL":
                    if ev.key == pygame.K_UP: indice_sel = (indice_sel - 1) % 4
                    elif ev.key == pygame.K_DOWN: indice_sel = (indice_sel + 1) % 4
                    elif ev.key == pygame.K_RETURN:
                        if indice_sel == 0:
                            menu_actual = "LISTADO"; datos_listado = reporte_a_datos()
                        elif indice_sel == 1:
                            menu_actual = "BUSQUEDA"; input_cedula = ""; resultado_busqueda = None
                        elif indice_sel == 2:
                            menu_actual = "TOP5"; datos_top = reporte_c_piezas()
                        elif indice_sel == 3: ejecutando = False
                elif menu_actual == "LISTADO":
                    if ev.key == pygame.K_DOWN: scroll_y += 25
                    elif ev.key == pygame.K_UP: scroll_y = max(0, scroll_y - 25)
                elif menu_actual == "BUSQUEDA":
                    if ev.key == pygame.K_RETURN:
                        resultado_busqueda = buscar_jugador_por_cedula(input_cedula)
                        if not resultado_busqueda: resultado_busqueda = False
                    elif ev.key == pygame.K_BACKSPACE:
                        input_cedula = input_cedula[:-1]
                    # SECCIÓN CLAVE: PERMITIR NÚMEROS Y PUNTOS
                    elif ev.unicode.isdigit() or ev.unicode in ".-":
                        if len(input_cedula) < 15:
                            input_cedula += ev.unicode

        pygame.display.flip()
        reloj.tick(30)
    return "MENU"