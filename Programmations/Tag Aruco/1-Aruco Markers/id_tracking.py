import cv2 as cv
from cv2 import aruco
import numpy as np

# Loading all pre-built libraries
ARUCO_DICT = {
    "DICT_4X4_50": cv.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv.aruco.DICT_APRILTAG_36h11
}

# Capture video from webcam (change the argument to your video file if needed)
cap = cv.VideoCapture(2)

# Moving ID
moving_id = 100

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # Defining lists
    corners = []
    ID = []
    centres = []
    z_rot = []

    # Checking the frame with each pre-loaded library
    for i in ARUCO_DICT.values():
        dictionary = aruco.getPredefinedDictionary(i)
        parameters = aruco.DetectorParameters()
        detector = aruco.ArucoDetector(dictionary, parameters)
        marker_corners, markers_ID, reject = detector.detectMarkers(frame)
        if marker_corners is not None and markers_ID is not None:
            corners.append(marker_corners)
            ID.append(markers_ID)
            break

    # Find index of moving_id in the detected markers
    moving_id_index = None
    if moving_id in ID:
        moving_id_index = ID.index(moving_id)

    # Calculate centre and angle of each marker
    for mark, current_id in zip(corners, ID):
        for dv in mark:
            for c0, c1, c2, c3 in dv:
                mx = (c0[0] + c1[0] + c2[0] + c3[0]) / 4
                my = (c0[1] + c1[1] + c2[1] + c3[1]) / 4
                c = [mx, my]
                centres.append(c)

                # Check if the marker is the moving_id
                if moving_id_index is not None and current_id == moving_id:
                    continue  # Skip the moving_id for distance calculation

                # Calculate Euclidean distance to the moving_id if it exists
                if moving_id_index is not None:
                    distance = np.linalg.norm(c - np.array(centres[moving_id_index]))
                    print(f"Distance from {current_id} to {moving_id}: {distance}")

    # Updating frame to show the values and data found
    if len(marker_corners) > 0:
        aruco.drawDetectedMarkers(frame, marker_corners, markers_ID, (0, 255, 0))

    for centre in centres:
        cv.circle(frame, (int(centre[0]), int(centre[1])), 5, (255, 0, 255), -1)

    cv.imshow("Frame", frame)

    # Press 'q' to exit the loop
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv.destroyAllWindows()
