from __future__ import print_function
import cv2
import numpy as np


class AlignimageADJ:
    def __init__(self, im1, im2):
        self.im1 = im1
        self.im2 = im2
        self.MAX_FEATURES = 5000
        self.GOOD_MATCH_PERCENT = 0.99
    def alignImages(self):

      # Convert images to grayscale
      im1Gray = cv2.cvtColor(self.im1, cv2.COLOR_BGR2GRAY)
      im2Gray = cv2.cvtColor(self.im2, cv2.COLOR_BGR2GRAY)

      # Detect ORB features and compute descriptors.
      orb = cv2.ORB_create(self.MAX_FEATURES)
      keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
      keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

      # Match features.
      matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
      matches = matcher.match(descriptors1, descriptors2, None)

      # Sort matches by score
      matches.sort(key=lambda x: x.distance, reverse=False)

      # Remove not so good matches
      numGoodMatches = int(len(matches) * self.GOOD_MATCH_PERCENT)
      matches = matches[:numGoodMatches]

      # Draw top matches
      imMatches = cv2.drawMatches(self.im1, keypoints1, self.im2, keypoints2, matches, None)
      cv2.imwrite("matches.jpg", imMatches)

      # Extract location of good matches
      points1 = np.zeros((len(matches), 2), dtype=np.float32)
      points2 = np.zeros((len(matches), 2), dtype=np.float32)

      for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

      # Find homography
      h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

      # Use homography
      height, width, channels = self.im2.shape
      im1Reg = cv2.warpPerspective(self.im1, h, (width, height))

      return im1Reg, h
