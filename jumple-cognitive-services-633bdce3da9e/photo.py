import pygame
import pygame.camera
import time

class photo:
    def take_photo():
        pygame.camera.init()
        pygame.camera.list_cameras()
        cam = pygame.camera.Camera("/dev/video0", (640, 480))
        cam.start()
        time.sleep(0.1)  # You might need something higher in the beginning
        img = cam.get_image()
        pygame.image.save(img, "./photo/ultima_foto.jpg")
        cam.stop()
