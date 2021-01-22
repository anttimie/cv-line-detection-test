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
            retval, frame = cap.read()

            self.screen.fill(self.screen_fill)

            canny = frame_obj.canny_edges(frame)
            cropped = frame_obj.mask(canny)

            lines = cv.HoughLinesP(cropped, 2, np.pi / 180, 100, np.array([]), 100, maxLineGap = 5 )
            
            average_lines = frame_obj.average_slope_intercept(frame, lines)
            line_frame = frame_obj.process_frame_for_lines(color_bgr, frame, average_lines)
            combo_frame = cv.addWeighted(frame, 0.8, line_frame, 1, 1)
            cf = combo_frame.swapaxes(0,1)
            key = cv.waitKey(100)

            pygame.surfarray.blit_array(self.screen, cf)
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