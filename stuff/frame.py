import os
import cv2 as cv
import numpy as np

class Frame:
    def __init__(self, filename = os.getenv("PICTUREPATH"), threshold1 = 50, threshold2 = 150, minLineLen = 100, maxLineGap = 10):
        self.filename = filename
        self.threshold1 = threshold1
        self.threshold2 = threshold2
        self.minLineLen = minLineLen
        self.maxLineGap = maxLineGap
        
    def process_frame_for_lines(self, color,  frame, lines):
        frame_ok = np.zeros_like(frame)

        if lines is not None:
          for x1, y1, x2, y2 in lines:
            cv.line(frame, (x1, y1), (x2, y2), (color), 10)
        
        return frame_ok

    # Thanks begin: https://www.geeksforgeeks.org/opencv-real-time-road-lane-detection/
    def canny_edges(self, frame):
      converted = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
      blurred = cv.GaussianBlur(converted, (5, 5), 0)
      canny = cv.Canny(blurred, self.threshold1, self.threshold2)

      return canny

    def mask(self, frame):
      h = frame.shape[0]
      polygons = np.array([
        [(200, h), (1920, h), (550, 250)]
      ])
      
      # print(polygons)

      mask = np.zeros_like(frame)
      cv.fillPoly(mask, polygons, 255)
      masked = cv.bitwise_and(frame, mask)

      return masked

    def create_coordinates(self, frame, line_parameters):
      slope, intercept = line_parameters
      y1 = frame.shape[0]
      y2 = int(y1 * (4 / 5))
      x1 = int((y1 - intercept) / slope)
      x2 = int((y2 - intercept) / slope)

      return np.array([x1, y1, x2, y2])
    
    def average_slope_intercept(self, frame, lines):
      left_fit = []
      right_fit = []
      
      for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        param = np.polyfit((x1, x2), (y1, y2), 1)
        slope = param[0]
        intercept = param[1]

        if slope < 0:
          left_fit.append((slope, intercept))
        else:
          right_fit.append((slope, intercept)) 
      
      if left_fit:
        left_line = self.fits(left_fit, frame)
        # print(left_line)

      if right_fit:
        right_line = self.fits(right_fit, frame)
        print(right_line)

      return np.array([left_line, right_line])
    # Thanks end: https://www.geeksforgeeks.org/opencv-real-time-road-lane-detection/

    def fits(self, side_fit, frame):
      value = []
      avg = np.average(side_fit, axis = 0)
      value = self.create_coordinates(frame, avg)

      return value

    # To test single frame
    def process_single_frame(self, color):
      image = cv.imread(self.filename)
      converted = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
      edges = cv.Canny(converted, self.threshold1, self.threshold2, apertureSize = 3)
      lines = cv.HoughLinesP(edges, 1, np.pi/180, self.minLineLen, self.maxLineGap)

      for line in lines:
        for x1, y1, x2, y2 in line:
          cv.line(image, (x1, y1), (x2, y2), color, 3)
        
      cv.imwrite("locals/hlinesp.jpg", image)