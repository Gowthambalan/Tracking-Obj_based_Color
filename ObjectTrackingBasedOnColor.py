import imutils # for resizeing image
import cv2 # opencv

orgLower = (0, 255, 96)
orgUpper = (63, 255, 255)

cam = cv2.VideoCapture(0) # camera init.

while True:

    _,frame = cam.read() # reading frame from camera

    frame = imutils.resize(frame, width=600) # resizeing a frame

    blur = cv2.GaussianBlur(frame, (11,11), 0) # smoothing

    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) # convert bgr 2 hsv color format

    mask = cv2.inRange(hsv, orgLower, orgUpper) # mask the orange color

    mask = cv2.erode(mask, None, iterations = 2)

    mask = cv2.dilate(mask, None, iterations = 2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

    center = None
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]),int(M["m01"] / M["m00"]))

        if radius > 10:

            cv2.circle(frame,(int(x), int(y)),int(radius),(0.255,255), 2)

            cv2.circle(frame, center,5,(0,0,255),-1)

            # print(center,radius)
            if radius > 250:
                print("stop")
            else:
                if(center[0]<150):
                    print("Left")
                elif(center[0]>450):
                    print("Right")
                elif(center[0]<250):
                    print("Front")
                else:
                    print("Stop")

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
       
cam.release()
cv2.destroyAllWindows()

