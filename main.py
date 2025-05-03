import cv2
import numpy as np
import face_recognition
import os
import pandas as pd
from datetime import datetime

# Get the directory of this script
base_path = os.path.dirname(os.path.abspath(__file__))

# Load background image safely
bg_path = os.path.join(base_path, 'background.png')
bg_image = cv2.imread(bg_path)
if bg_image is None:
    raise FileNotFoundError("Background image not found.")
if bg_image.shape[2] == 4:
    bg_image = bg_image[:, :, :3]

# Load student Excel sheet
excel_path = os.path.join(base_path, 'AI_department.xlsx')
df = pd.read_excel(excel_path)

# Ensure all date columns are treated as string type
df.columns = [str(col) for col in df.columns]

# Extract student details (Roll Number and Name)
df['Roll Number'] = df['Roll Number'].astype(str)
roll_no_list = df['Roll Number'].tolist()
names_list = df['Name'].tolist()

# Load known images
path = os.path.join(base_path, 'images')
if not os.path.exists(path):
    raise FileNotFoundError(f"Image directory '{path}' not found.")

images = []
student_ids = []
myList = os.listdir(path)
for img_name in myList:
    curImg = cv2.imread(os.path.join(path, img_name))
    if curImg is not None:
        images.append(curImg)
        student_ids.append(os.path.splitext(img_name)[0])  # roll number

# Encode known faces
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if encodes:
            encodeList.append(encodes[0])
    return encodeList

encodeListKnown = findEncodings(images)

# Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Webcam not accessible.")

cv2.namedWindow("Attendance System", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Attendance System", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

marked_students = set()

while True:
    success, img = cap.read()
    if not success:
        continue

    imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # Prepare background
    output_frame = bg_image.copy()

    # Resize camera feed to fit into background layout
    cam_frame = cv2.resize(img, (400, 480))
    output_frame[120:600, 780:1180] = cam_frame

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            roll_no = student_ids[matchIndex]
            if roll_no not in marked_students:
                marked_students.add(roll_no)

                # Get the current date in 'YYYY-MM-DD' format
                # Get the current date in Indian format
                current_date = datetime.now().strftime('%d-%m-%Y')

                # If date column doesn't exist, create it with '-' for all students
                if current_date not in df.columns:
                    df[current_date] = '-'

                # Mark the detected student as present (✓)
                df.loc[df['Roll Number'] == roll_no, current_date] = '✓'
                df.to_excel(excel_path, index=False)



                # Check if the current date is a valid column in the Excel sheet
                if current_date in df.columns:
                    df.loc[df['Roll Number'] == roll_no, current_date] = '✓'
                    df.to_excel(excel_path, index=False)
                else:
                    print(f"Date column '{current_date}' not found in the Excel sheet.")

            # Get coordinates for the face location
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4

            name_index = roll_no_list.index(roll_no)
            name = names_list[name_index]

            # Highlight the student's name
            cv2.putText(output_frame, f'{name} ({roll_no})', (x1 + 780, y2 + 120 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Attendance System", output_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
