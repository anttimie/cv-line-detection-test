import sys
import pygame
import cv2 as cv
import numpy as np
import visual
import frame as f_mod

from pygame.locals import KEYDOWN, K_ESCAPE, K_q

class Player:
    caption = 'open cv video stream on pygame'
    
    def __init__(self, filename):
        self.filename = filename
        self.screen_size = np.array([1920, 1080])
        self.screen = pygame.display.set_mode(np.array([1920, 1080]))
        self.screen_fill = np.array([0, 0, 0])

    def set(self):
        cap = cv.VideoCapture(self.filename)

        pygame.init()
        pygame.display.set_caption(self.caption)

        self.screen

        return cap

    def play(self):
        visual_obj = visual.Color(255, 0, 0)
        color_bgr = visual_obj.solve()
        frame_obj = f_mod.Frame(color_bgr)

        cap = self.set()

        while(cap.isOpened()):
            ret, frame = cap.read()
            self.screen.fill(self.screen_fill)

            ret_frame = frame_obj.process_frame(color_bgr, frame)
            frame = ret_frame.swapaxes(0, 1)
            key = cv.waitKey(5)

            pygame.surfarray.blit_array(self.screen, frame)
            pygame.display.update()
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    cv.destroyAllWindows()
                    sys.exit(0)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_q:
                        cap.release()
                        cv.destroyAllWindows()
                        sys.exit(0)
                elif key == 's':
                    cv.waitKey()