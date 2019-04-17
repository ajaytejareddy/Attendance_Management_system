# USAGE
# python recognize_faces_video.py --encodings encodings.pickle
# python recognize_faces_video.py --encodings encodings.pickle --output output/jurassic_park_trailer_output.avi --display 0
# import the necessary packages

from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import firebase

dd = time.strftime("%d")
mm = time.strftime("%m")
yy = time.strftime("%Y")
HH = time.strftime("%H")
MM = time.strftime("%M")

date = time.strftime("%d") + time.strftime("%m") + time.strftime("%Y")

attendance = {}
held={}

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", default="encodings.pickle",
		help="path to serialized db of facial encodings")
ap.add_argument("-o", "--output", type=str,
		help="path to output video")
ap.add_argument("-y", "--display", type=int, default=1,
		help="whether or not to display output frame to screen")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
		help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())


def start():


	# load the known faces and embeddings
	print("[.]loading encodings...")
	data = pickle.loads(open(args["encodings"], "rb").read())
	vs = VideoStream(src=0)
	vs.start()

	fileObj=open("data.pickle",'rb')

	b=pickle.load(fileObj)

	args['display'] = 1
	# initialize the video stream and pointer to output video file, then
	# allow the camera sensor to warm up
	print("[.] starting video stream...")
	writer = None

	# loop over frames from the video file stream
	while True:
		# grab the frame from the threaded video stream
		frame = vs.read()

		# convert the input frame from BGR to RGB then resize it to have
		# a width of 750px (to speedup processing)
		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		rgb = imutils.resize(frame, width=750)
		r = frame.shape[1] / float(rgb.shape[1])

		# detect the (x, y)-coordinates of the bounding boxes
		# corresponding to each face in the input frame, then compute
		# the facial embeddings for each face
		boxes = face_recognition.face_locations(rgb,
			model=args["detection_method"])
		encodings = face_recognition.face_encodings(rgb, boxes)
		names = []
		rno=""

		date = time.strftime("%d") + time.strftime("%m") + time.strftime("%Y")
		HH = time.strftime("%H")

		if date not in held:
			held[date] = ''
			if HH not in held[date]:
				held[date] = held[date] + HH
		else:
			if HH not in held[date]:
				held[date] = held[date] + HH

		# loop over the facial embeddings
		for encoding in encodings:
			# attempt to match each face in the input image to our known
			# encodings
			matches = face_recognition.compare_faces(data["encodings"],
				encoding)
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

				# determine the recognized face with the largest number
				# of votes (note: in the event of an unlikely tie Python
				# will select first entry in the dictionary)
				#print(counts)
				max_count = max(counts.values())
				#print(max_count)
				name="Unknown"
				if  max_count>=178:
					for key in counts:
						if counts[key] == max_count:
							name = b[key]
							rno=key

			# update the list of names
			names.append(name)

		# loop over the recognized faces
		for ((top, right, bottom, left), name) in zip(boxes, names):
			# rescale the face coordinates
			top = int(top * r)
			right = int(right * r)
			bottom = int(bottom * r)
			left = int(left * r)

			if name != "Unknown":
				if rno in attendance:
					if date in attendance[rno]:
						attendance[rno][date][HH] = 1
					else:
						attendance[rno][date] = {}
						attendance[rno][date][HH] = 1
				else:
					attendance[rno] = {}
					if date in attendance[rno]:
						attendance[rno][date][HH] = 1
					else:
						attendance[rno][date] = {}
						attendance[rno][date][HH] = 1

			# draw the predicted face name on the image
			cv2.rectangle(frame, (left, top), (right, bottom),
				(0, 255, 0), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
				0.75, (0, 255, 0), 2)

		#print(attendance,held)
		# if the video writer is None *AND* we are supposed to write
		# the output video to disk initialize the writer
		if writer is None and args["output"] is not None:
			fourcc = cv2.VideoWriter_fourcc(*"MJPG")
			writer = cv2.VideoWriter(args["output"], fourcc, 20,
				(frame.shape[1], frame.shape[0]), True)

		# if the writer is not None, write the frame with recognized
		# faces t odisk
		if writer is not None:
			writer.write(frame)

		# check to see if we are supposed to display the output frame to
		# the screen
		if args["display"] > 0:
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF

			# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break
		else:
			break

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()
	print(attendance)

	# check to see if the video writer point needs to be released
	if writer is not None:
		writer.release()


def stop():
	args["display"]=0
	#print(attendance, held)
	cv2.destroyAllWindows()
	return attendance,held
