from flask import Flask, render_template, redirect, url_for, request,session
import cv2
import os
import face_recognition
import glob
import numpy as np
from PIL import Image, ImageDraw

app=Flask(__name__)

app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

@app.route('/')
def home():
    return "apoorav"
@app.route('/start', methods=['GET'])
def hunny():
    error=None
    return render_template('start.html', error=error)
@app.route('/start', methods=['POST'])
def start():
    error=None
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("F:\hackathon\Test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        cv2.imshow("F:\hackathon\Test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            a=1;
            img_name = "opencv_frame_{}.png".format(img_counter)
            path = 'F:\hackathon\Test/'
            cv2.imwrite(os.path.join(path , img_name), frame)
            print("{} written!".format(img_name))
            img_counter += 1
            if a==1:
                break;

    cam.release()

    cv2.destroyAllWindows()
    os.chdir("F:\hackathon\Test")
    path2 = 'F:\hackathon/'
    for images in glob.glob("*.png"):
        image_name=images
        image=face_recognition.load_image_file(images)
        face_locations = face_recognition.face_locations(image)
        #test_face = face_recognition.face_encodings(image, face_locations)
        pil_image = Image.fromarray(image)
        draw = ImageDraw.Draw(pil_image)
        for (top, right, bottom, left) in face_locations:
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
            # print(image[left:right][top:bottom])
            x=image[top:bottom,left:right]
        pil_image.show()
        cv2.imwrite(os.path.join(path2 , "face.jpg"), x)
        redirect(url_for('start'))

    return render_template('start.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)
