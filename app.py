from tkinter import filedialog
import tkinter as tk
import cv2
import shutil
import os
from PIL import Image, ImageTk
from cartoonizer import cartoonize

file_path = -1
file_name = -1
# cap = cv2.VideoCapture(0)

video_selected = False
photo_selected = False

def browse_photo():
    global file_path
    global file_name
    file_path = filedialog.askopenfilename(initialdir='/',
                                           title='Select The Image',
                                           filetype=(('JPG Files', '*.jpg'),('all files', '*.*')))
    shutil.copy(file_path, 'Images')
    file_name = str(file_path).split('/')
    file_name = file_name[len(file_name)-1]
    img_pil = Image.open(file_path)
    resized = img_pil.resize((300, 400), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(resized)
    image_preview.config(image=img)
    image_preview.image = img
    global photo_selected, video_selected
    photo_selected = True
    video_selected = False

def browse_video():
    global file_path
    global file_name
    file_path = filedialog.askopenfilename(initialdir='/',
                                           title='Select The Image',
                                           filetype=(('mp4 Files', '*.mp4'),('all files', '*.*')))
    shutil.copy(file_path, 'Video')
    file_name = str(file_path).split('/')
    file_name = file_name[len(file_name)-1]
    load_video_frames()
    global video_selected , photo_selected
    video_selected = True
    photo_selected = False
    
    
def load_video_frames():
    n = 0

    if n == 0:
        cap = cv2.VideoCapture('Video/'+file_name)
        n+=1
    r = True
    image_preview.config(text='Video Selected')
    image_preview.text = 'Video Selected'

def onCartoonButtonClick():

    if file_path == -1:
        cartoon_preview.config(text='Select File to Cartoonize')
    else:
        if photo_selected:
            model_path = 'saved_models'
            load_folder = 'Images'
            save_folder = 'cartoonized_images'
            cartoonize(load_folder, save_folder, model_path)
            os.remove('Images/'+file_name)
            img_pil = Image.open('cartoonized_images/'+file_name)
            resized = img_pil.resize((300, 400), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(resized)
            cartoon_preview.config(image=img)
            cartoon_preview.image = img
        elif video_selected:
            i=0
            r = True
            if i == 0:
                cap = cv2.VideoCapture('Video/'+file_name)
            while r:

                r, frame = cap.read()
                try:
                    cv2.imwrite('Images/im'+str(i)+'.jpg', frame)
                    i+=1
                except:
                    continue

                if cv2.waitKey(0) == ord('q'):
                    break

            print('Frames Extracted')

            model_path = 'saved_models'
            load_folder = 'Images'
            save_folder = 'cartoonized_images_of_video'

            cartoonize(load_folder, save_folder, model_path)
            for x in range(i):
                os.remove('Images/im'+str(x)+'.jpg')




root = tk.Tk()
root.geometry('800x480')#w*h
root.title('Cartoonizer')
root.pack_propagate(False)
root.resizable(0,0)

image_frame = tk.LabelFrame(root, text='Image View:')
image_frame.place(height=300, width=400)

cartoon_frame = tk.LabelFrame(root, text='Cartoon Image:')
cartoon_frame.place(height=300, width=400, relx=0.5)

load_file_frame = tk.LabelFrame(root, text='File Path:')
load_file_frame.place(height=50, width=800, rely=0.75)

load_photo_btn = tk.Button(load_file_frame, text='Load Photo', command=browse_photo)
load_photo_btn.place(width=115, relx=0.2)

load_video_btn = tk.Button(load_file_frame, text='Load Video', command=browse_video)
load_video_btn.place(width=115, relx=0.6)

cartoonize_btn = tk.Button(root, text='Cartoonize', command=onCartoonButtonClick)
cartoonize_btn.place(height=50, width=800, rely=0.87)

cartoon_preview = tk.Label(cartoon_frame, text='Cartoon Image Preview')
cartoon_preview.place(height=300, width=400)

image_preview = tk.Label(image_frame, text='Selected Image Preview')
image_preview.place(height=300, width=400)

root.mainloop()