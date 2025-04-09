import cv2

face_capture= cv2.CascadeClassifier("C:/Users/ASUS/AppData/Local/Programs/Python/Python313/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")



vid_cap=cv2.VideoCapture(0)
while True:
    ret , video = vid_cap.read()
    col = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
    faces = face_capture.detectMultiScale(
        
        col,scaleFactor= 1.3,
        minNeighbors= 5,
        minSize=(30,30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    for (x,y,w,h) in faces:
        cv2.rectangle(video,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(video,"Face",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,0),2)


    cv2.imshow("vid_live",video)
    if cv2.waitKey(10) == ord("a"):
        break
vid_cap.release()