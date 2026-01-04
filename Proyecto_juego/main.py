import pygame
import globales as gb
from pantallas import bienvenida, menu, creditos, registro, login 
import juego as jg 
import reportes_visual as rep

def ejecutar_sistema():
    pygame.init()
    ventana = pygame.display.set_mode((gb.ANCHO_VENTANA, gb.ALTO_VENTANA))
    pygame.display.set_caption("SISTEMA DE AJEDREZ Y ODS - SEBASTIAN RIVAS")
    
    bienvenida.ejecutar(ventana)
    
    estado = "MENU"
    ejecutando = True
    
    while ejecutando:
        if estado == "MENU":
            estado = menu.ejecutar(ventana)
        
        elif estado == "REGISTRO":
            estado = registro.ejecutar(ventana)
            
        elif estado == "LOGIN":
            estado = login.ejecutar(ventana)
                
        elif estado == "JUEGO":
            estado = jg.iniciar_partida(ventana)
            
        elif estado == "REPORTES":
            estado = rep.pantalla_reportes(ventana)
            
        elif estado == "CREDITOS":
            creditos.ejecutar(ventana)
            estado = "MENU"
            
        elif estado == "SALIR":
            ejecutando = False

    pygame.quit()

if __name__ == "__main__":
    ejecutar_sistema()