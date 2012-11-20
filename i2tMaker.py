#!/usr/bin/python

import threading
import sys, os
import time
import cv2
import urllib, urllib2

URL = "http://i2t.posquit0.com/lot_insert.php"
mHeader = {"Host": "i2t.posquit0.com", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language":"ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4", "Accept-Charset":"windows-949,utf-8;q=0.7,*;q=0.3","Content-Type":"application/x-www-form-urlencoded"}

if(len(sys.argv)-1 != 1):
        NO = raw_input('project Name ? ')
else:
        NO = sys.argv[1]

def makeFootprint(bit_data, cnt):
	mPostData = {'bits' : bit_data, 'vid' : NO , 'pid' : cnt}
	mEncodedData = urllib.urlencode(mPostData)
	mReq = urllib2.Request(URL, None, mHeader)
	mConn = urllib2.urlopen(mReq, mEncodedData)
#	mData = mConn.read()
	print cnt

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


def hmdistance(desc1,desc2):
	
	all_cnt=0
	for x in range(8):
		cnt=0
		for y in range(24):
			if(desc1[x*y]!=desc2[x*y]):
				cnt+=1
				all_cnt+=1
			if(all_cnt>10 || cnt > 2)
				return -1

	return all_cnt


def main():
	detector_type = "SIFT"

	curPath = os.path.split(os.path.abspath(__file__))[0]
	tempDir = os.path.join(curPath , "backup/"+str(NO))
	fileDir = os.listdir(tempDir)
	fileDir.sort()

	i=0
	desc = []

	for fileName, cnt in zip(fileDir, range(len(fileDir))):
		imfile = os.path.join(tempDir, fileName)
		print imfile
		img_data = cv2.imread(imfile)
		(feature_points, descriptors) = i2t_feature_detector(detector_type, img_data)
#		i2t_view_featured_image(img_data, feature_points)

		grace_result = ""

		if descriptors is None:
			continue
		
		desc.append([])
		
		#after.append('')
		desc[i].append(0)
		desc[i].append([])
		desc[i].append([])
		desc[i].append([])
	
		j=0

		desc[i][0]=cnt

		for dsc in descriptors:
			px,py = feature_points[j].pt

			desc[i][1].append(0)
			desc[i][2].append(0)
			desc[i][3].append("")
			desc[i][1][j]=px
			desc[i][2][j]=py

			dscList = dsc.tolist()[60 : 124]
			dscList = [int(x ** 0.5) for x in dscList]
			for x in dscList:
				if x > 0 and x <= 7:
					desc[i][3][j]+= '1'
				else:
					desc[i][3][j]+= '0'
		
				if x >= 4 and x <= 11:
					desc[i][3][j]+= '1'
				else:
					desc[i][3][j]+= '0'
	
				if x >= 8 and x <= 16:
					desc[i][3][j]+= '1'
				else:
					desc[i][3][j]+= '0'
			j+=1


		if i>1:
			after = desc[i]
			now = desc[i-1]
  			before = desc[i-2]

			des_range=10

			max_arr = []

			for x in range(now[0]):
				for y in range(before[0]):
					if(abs(now[1][x]-before[1][y])<=des_range && abs(now[2][x]-before[2][y])<=des_range):
						v=0
						v=hmdistance(now[3][x],before[3][y])
						if(v==-1):
							continue

						k=0
						kmax=[0,0]

						for z in max_arr:
							if(z==x):
								k=50
								break
							if(kmax[0]<z[0]): //[0] == value , [1] == idx
								kmax[0]=z[0]
								kmax[1]=z[1]




							



	


		i+=1
	
		makeFootprint(grace_result, cnt)
		

if __name__ == '__main__':
	main()
#	i2t_handle(None)
