
import cv2
import easygui
import numpy as np
import imageio
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

top = tk.Tk()
top.geometry('400x400')
top.title('Cartoonify your Image!')
top.configure(background='white')

label = Label(top, background='#CDCDCD', font=('calibri',20,'bold'))

def upload():
    # Select image
    image_path = filedialog.askopenfilename()
    if image_path:
        cartoonify(image_path)
    else:
        print("No image selected")

def cartoonify(image_path):
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    if original_image is None:
        print("Can't open image. Try again.")
        return

     # Convert image to grayscale
    gray = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)

    # Apply median blur to smooth the image
    blurred = cv2.medianBlur(gray, 5)

    # Create edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Create a color image using bilateral filter
    color = cv2.bilateralFilter(original_image, 9, 300, 300)

    # Combine edges and color image
    cartoon_image = cv2.bitwise_and(color, color, mask=edges)

    # Display cartoon image
    cartoon_image = cv2.cvtColor(cartoon_image, cv2.COLOR_BGR2RGB)
    cartoon_image = Image.fromarray(cartoon_image)
    cartoon_image = ImageTk.PhotoImage(cartoon_image)

    label.configure(image=cartoon_image)
    label.image = cartoon_image
    label.pack(side=TOP, pady=10)
def save_cartoon():
    save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
    if save_path:
        cv2.imwrite(save_path, cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR))
        print(f"Image saved at {save_path}")
    # Create upload button
upload_btn = Button(top,text="Cartoonify an Image",command=upload,padx=10,pady=5)
upload_btn.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
upload_btn.pack(side=TOP,pady=50)
save_btn = Button(top,text="Save Cartoon Image",command=save_cartoon,padx=10,pady=5)
save_btn.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
save_btn.pack(side=TOP,pady=10)
top.mainloop()

