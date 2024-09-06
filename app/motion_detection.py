import cv2
import numpy as np
import time
from termcolor import colored
import os
from app.notifications import NotificationSystem

# ASCII art for motion detection
motion_symbols = ["🟥", "🟩"]

# Check if we're in TEST mode
TEST_MODE = os.environ.get('TEST', '0') == '1'

# Todo: Add an 'System Arm" function that will arm the motion detection system



# Todo: make this a class
def detect_motion(frame, prev_frame, min_area=1000):

	''' 
	https: // docs.opencv.org/4.x/d7/df3/group__imgproc__motion.html
	https://docs.opencv.org/4.x/de/de1/group__video__motion.html
	'''

	if frame is None or prev_frame is None:
		return False
	if frame.shape != prev_frame.shape:
		return False
	
	'''
	https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html
	'''

	try:
		# convert frame to grayscale
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

		# difference between frames
		d = cv2.absdiff(prev_gray, gray)

		# Apply a threshold to get binary image
		_, t = cv2.threshold(d, 25, 255, cv2.THRESH_BINARY)

		# Dilate the thresholded image to fill holes
		t = cv2.dilate(t, None, iterations=2)

		# find image contours on t
		# cs = contours
		cs, _ = cv2.findContours(t, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]

		# Check for motion!
		for c in cs:
			if cv2.contourArea(c) < min_area: # current sens
				continue
			return True
		
		return False
	except Exception as e:
		print(f"Error in motion_detection(): {e}")
		return False


def main():
	cap = cv2.VideoCapture(0) # Default camera

	if not cap.isOpened():
		print("Error: Could not open camera")
		return 
	
	ret, prev_frame = cap.read()
	if not ret:
		print("Error: could not read first frame")
		return 

	# Read first frames
	time.sleep(0.1) # To avoid a duplicate frame bug

	frame_count = 0
	motion_detected = False  # Initialize motion_detected

	# Initialize NotificationSystem (only if not in TEST mode)
	if not TEST_MODE:
		notification_system = NotificationSystem(
			"your_email@gmail.com",
			"your_app_password",
			"recipient@example.com"
		)

	while True:
		if TEST_MODE:
			# In TEST mode, we'll simulate frames instead of capturing from camera
			frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
		else:
			ret, frame = cap.read()
			if not ret: 
				print(f"Error: could not read frame {frame_count}.")
				break

		frame_count += 1

		# main driver thing that does stuff
		new_motion_detected = detect_motion(frame, prev_frame)

		# only print when the motion state changes
		if new_motion_detected != motion_detected:
			motion_detected = new_motion_detected
			if motion_detected:
				print(f"\r{motion_symbols[0]}", end="", flush=True)
				if not TEST_MODE:
					notification_system.send_email("Motion Detected", "Motion has been detected in your monitored area.")
			else:
				print(f"\r{motion_symbols[1]}", end="", flush=True)

		# read next frames. Prev becomes curr, curr gets next
		prev_frame = frame.copy()

		# Testing
		if not TEST_MODE:
			cv2.imshow('Frame', frame)

		# break loop on q press or after 100 frames in TEST mode
		if TEST_MODE and frame_count >= 100:
			break
		if not TEST_MODE and cv2.waitKey(1) & 0xFF == ord('q'):
			break

		# Add a small delay to slow down the output
		time.sleep(0.1)

	if not TEST_MODE:
		cap.release()
		cv2.destroyAllWindows()

if __name__ == '__main__':
	main()