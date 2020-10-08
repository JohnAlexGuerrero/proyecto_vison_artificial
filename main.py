#libreria para redimensionar imagenes
import imutils 
import numpy as np
#opencv es la encargada de procesar la informacion de la webcam
import cv2
import argparse
import pygame

from datetime import date
from pygame.locals import *

pygame.init()

pygame.display.set_mode((470,300))

count = 1
camera = cv2.VideoCapture(0)

while True:
    grabbed, frame = camera.read()

    #en una variable llamada eventos le pasamos un método que recibe precisamente todo tipo de eventos que vienen preprogramados en Pygame
    for eventos in pygame.event.get():
        if eventos.type == pygame.QUIT:
            exit()


    if not grabbed:
        break

    frame = imutils.resize(frame, width=400)

    #mostramos el frame
    cv2.imshow('CAMARA', frame)

    k = cv2.waitKey(1)

    if k & 0xFF == ord('q'):
        break

    #tomamos foto con cv2
    if k & 0xFF == ord('c'):
        cv2.imwrite("foto_{}.png".format(count), frame)
        print("Foto tomada correctamente: foto_{}".format(count))
        count += 1
   
    #libera la camara y cierra todas las ventanas
camera.release()

cv2.destroyAllWindows()
