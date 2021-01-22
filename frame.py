import cv2 as cv
import numpy as np

class Frame:
    def __init__(self, filename = r"D:\code\scripts\python\cart.jpg", threshold1 = 50, threshold2 = 150, minLineLen = 100, maxLineGap = 10):
        self.filename = filename
        self.threshold1 = threshold1
        self.threshold2 = threshold2
        self.minLineLen = minLineLen
        self.maxLineGap = maxLineGap
        
    def process_frame(self, frame):
        converted = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        edges = cv.Canny(converted, self.threshold1, self.threshold2, apertureSize = 3)
        lines = cv.HoughLinesP(edges, 1, np.pi/180, self.minLineLen, self.maxLineGap)

        for line in lines:
            for x1, y1, x2, y2 in line:
                return cv.line(frame, (x1, y1), (x2, y2), color, 3)

    def process_edge(self, frame):
      converted = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
      blurred = cv.GaussianBlur(converted, (4, 4), 0)
      edges = cv.Canny(blurred, self.threshold1, self.threshold2)

      return edges

    def process_single_frame(self, color):
      image = cv.imread(self.filename)
      converted = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
      edges = cv.Canny(converted, self.threshold1, self.threshold2, apertureSize = 3)
      lines = cv.HoughLinesP(edges, 1, np.pi/180, self.minLineLen, self.maxLineGap)

      for line in lines:
        for x1, y1, x2, y2 in line:
          cv.line(image, (x1, y1), (x2, y2), color, 3)
        
      cv.imwrite("hlinesp.jpg", image)