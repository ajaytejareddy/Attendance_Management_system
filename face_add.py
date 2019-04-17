import cv2 as cv
import os


def fun(name):
    images="dataset/"+name
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR,images)

    max=0

    for root,dirs,files in os.walk(image_dir):
        for file in files:
            file=file.replace(".png","")
            file = file.replace(".jpeg","")
            if int(file) > max:
                max=int(file)

    return max



def add(name):
        count = 0
        cap = cv.VideoCapture(0)
        face_cascade = cv.CascadeClassifier('cascades/data/haarcascade_frontalface_default.xml')

        #To create Directory with the Name
        path = os.getcwd()
        path = path + "/dataset/" + name

        try:
            os.mkdir(path)
            count1=0
        except OSError:
            print("name already exists")
            count=fun(name)
            count1=fun(name)
            print(type(count))

        while(cap.isOpened()):
            # Capture frame-by-frame
            cv.waitKey(5)
            ret, frame = cap.read()
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            rgb = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
            bgr = cv.cvtColor(rgb,cv.COLOR_RGB2BGR)

            img_item = "dataset/" + name + "/" + str(count) + ".png"

            faces = face_cascade.detectMultiScale(gray, 1.32, 5)
            for (x, y, w, h) in faces:
                # To draw a rectangle in a face
                print(x,y,w,h)
                end_cord_x = x+h
                end_cord_y = y+h
                cv.rectangle(frame, (x, y), (end_cord_x, end_cord_y), (255, 255, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
                if count > count1+61:
                    break
                img_item = "dataset/"+name+"/"+str(count)+".png"
                count = count+1
                cv.waitKey(100)
                cv.imwrite(img_item,bgr)

                # Detects eyes of different sizes in the input image
                # To draw a rectangle in eyes
            if ret == True:
                frame = cv.flip(frame, 1)
                cv.imshow('frame',frame)
                if (cv.waitKey(20) & 0xFF == ord('q')) | count>count1+60 :
                    break
            else:
                break
        # When everything done, release the capture
        cap.release()
        cv.destroyAllWindows()