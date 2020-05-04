# USAGE
# python recognize_faces_image.py --encodings encodings.pickle --image examples/example_01.png 

# import the necessary packages
import face_recognition
import argparse
import pickle
import cv2
import matplotlib as plt
from imutils import paths
import os
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report 
actual=['s01', 's02', 's03', 's04', 's05', 's06', 's07', 's08', 's09', 's10', 's11', 's12', 's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20', 's21', 's22', 's23', 's24', 's25', 's26', 's27', 's28', 's29', 's30', 's31', 's32', 's33', 's34', 's35', 's36', 's37', 's38', 's39', 's40', 's41', 's42', 's43', 's44', 's45', 's46', 's47', 's48', 's49', 's50', 'alan_grant', 'MH123456','ian_malcolm', 'MH162017']
predicted=[]
imagePaths = list(paths.list_images("./examples//"))
#print(imagePaths)
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

# load the known faces and embeddings
#print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())

# load the input image and convert it from BGR to RGB

#from PIL import Image
#import math

#foo = Image.open(args["image"])
#x, y = foo.size
#x2, y2 = math.floor(x-20), math.floor(y-50)
#foo = foo.resize((x2,y2),Image.ANTIALIAS)
#foo.save(args["image"],quality=30)
#print(type(imagePaths[0]))
#print(type(args["image"]))
for i in imagePaths:
	#print(i[(len(i)-6):(len(i)-4)])
	image = cv2.imread(i)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# detect the (x, y)-coordinates of the bounding boxes corresponding
# to each face in the input image, then compute the facial embeddings
# for each face
#print("[INFO] recognizing faces...")
	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])
	encodings = face_recognition.face_encodings(rgb, boxes)

# initialize the list of names for each face detected
	names = []

# loop over the facial embeddings
	for encoding in encodings:
	# attempt to match each face in the input image to our known
	# encodings
		matches = face_recognition.compare_faces(data["encodings"],encoding)
		name = "Unknown"

	# check to see if we have found a match
		if True in matches:
		# find the indexes of all matched faces then initialize a
		# dictionary to count the total number of times each face
		# was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}

		# loop over the matched indexes and maintain a count for
		# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

		# determine the recognized face with the largest number of
		# votes (note: in the event of an unlikely tie Python will
		# select first entry in the dictionary)
			name = max(counts, key=counts.get)
	
	# update the list of names
		names.append(name)

# loop over the recognized faces
	for ((top, right, bottom, left), name) in zip(boxes, names):
	# draw the predicted face name on the image
		cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 255, 0), 2)

# show the output image
#cv2.imshow("Image", image)
#plt.imshow(img,cmap='gray')
#plt.show()
	print(name)
	predicted.append(name)
#cv2.waitKey(0)	
print(predicted)
results = confusion_matrix(actual, predicted) 
print("Confusion Matrix:")
print(results)
print ('Accuracy Score :',accuracy_score(actual, predicted)) 
print ('Report : ')
print (classification_report(actual, predicted)) 