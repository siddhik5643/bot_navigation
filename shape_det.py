import cv2
import numpy as np

class ShapeDetector:
	def __init__(self):
		pass
#		print('in shape  detector')
		
	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
#		print(peri)

		approx = cv2.approxPolyDP(c, 0.04 * peri, True)
		# for i in range(1,10):
		# 	approx1 = cv2.approxPolyDP(c, (1/100) * peri, True)
		# 	print(f'{i} --> {len(approx1)}')
		# if the shape is a triangle, it will have 3 vertices
		if len(approx) == 3: #or len(approx) == 4:

			shape = "triangle"
		# if the shape has 4 vertices, it is either a square or
		# a rectangle
#		elif len(approx) == 4:
			# compute the bounding box of the contour and use the
			# bounding box to compute the aspect ratio
#			(x, y, w, h) = cv2.boundingRect(approx)
#			ar = w / float(h)
			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
#			shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
		# if the shape is a pentagon, it will have 5 vertices
#		elif len(approx) == 5:
#			shape = "pentagon"
		# otherwise, we assume the shape is a circle
		else:
			shape = "circle"
			
		# return the name of the shape
#		print('exiting shape dectector')
		return shape