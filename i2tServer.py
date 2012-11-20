#!/usr/bin/python

from SocketServer import ThreadingTCPServer, StreamRequestHandler
from StringIO import StringIO
import threading
import sys, os
import time
import cv2
import urllib
import tempfile

PORT = 31337

def retrieveImage(url, filename):
	urllib.urlretrieve(url, filename)
	return

def i2t_feature_detector(detector, image):
	featureDetector = cv2.FeatureDetector_create(detector)
	gridAdaptedDetector = cv2.GridAdaptedFeatureDetector(featureDetector, 200)
	descriptorExtractor = cv2.DescriptorExtractor_create(detector)

	start_time = time.time()
	feature_points = gridAdaptedDetector.detect(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
	(feature_points, descriptors) = descriptorExtractor.compute(image, feature_points)
	end_time = time.time()
	print detector, ": Number of Feature Points is", len(feature_points), "[", end_time - start_time, "]"
	
	return (feature_points, descriptors)

def i2t_view_featured_image(image, feature_points):
	for feature in feature_points:
		x, y = feature.pt
		center = (int(x), int(y))
		size = int(feature.size)
		cv2.circle(image, center, size, (0,255,0))

	cv2.namedWindow("Image2Torrent Test View", cv2.CV_WINDOW_AUTOSIZE)	
	cv2.imshow("Image2Torrent Test View", image)
	cv2.waitKey(0)
	return

def i2t_handle(conn):
	img_url = conn.recv(512).strip()
#	img_url = "http://imgnews.naver.net/image/123/2012/10/30/20121030093238_59_20121030094202.jpg"	
#	img_url = "http://imgnews.naver.net/image/073/2012/11/09/121109_509c9fa56b000_59_20121109155029.jpg"
	detector_type = "SIFT"

	curPath = os.path.split(os.path.abspath(__file__))[0]
	tempDir = os.path.join(curPath , "temp")
	tempfile.tempdir = tempDir

	if os.path.exists(tempDir) == False:
		os.mkdir(tempDir)

	tempFile = tempfile.mktemp()
	imgFile = tempFile + ".img"
	dscFile = tempFile + ".dsc"
	print tempFile

	retrieveImage(img_url, imgFile)
	img_data = cv2.imread(imgFile)
	(feature_points, descriptors) = i2t_feature_detector(detector_type, img_data)
#	i2t_view_featured_image(img_data, feature_points)

	grace_result = ""

	for dsc in  descriptors:
		dscList = dsc.tolist()[60 : 124]
		dscList = [int(x ** 0.5) for x in dscList]
		for x in dscList:
			if x > 0 and x <= 7:
				grace_result += '1'
			else:
				grace_result += '0'
	
			if x >= 4 and x <= 11:
				grace_result += '1'
			else:
				grace_result += '0'
	
			if x >= 8 and x <= 16:
				grace_result += '1'
			else:
				grace_result += '0'
		
	conn.send(grace_result)
		

class I2T_Handler(StreamRequestHandler):
	def handle(self):
		print "connection from", self.client_address

		conn = self.request
		i2t_handle(conn)

		return

def main():
	i2t_server = ThreadingTCPServer(('', PORT), I2T_Handler)
	i2t_server.allow_reuse_address = True
	print "listening on port", PORT
	i2t_threads = threading.Thread(target = i2t_server.serve_forever)
	i2t_threads.setDaemon(True)
	i2t_threads.start()
	print "Image2Torrent Machine started..."
	raw_input()

if __name__ == '__main__':
	main()
#	i2t_handle(None)
