# Import the required Libraries
from tkinter import *
from PIL import Image, ImageTk


# Create an instance of tkinter frame
top = Tk()

# Set the geometry of tkinter frame
top.geometry("750x270")

# Create a canvas
canvas = Canvas(top, width=600, height=400)
canvas.pack()

# Load an image in the script
img = Image.open("tree_image.jpg")
# Resize the Image using resize method
resized_image = img.resize((300, 205))
new_image = ImageTk.PhotoImage(resized_image)

# Add image to the Canvas Items
# canvas.create_image(10, 10, anchor=NW, image=new_image)

frame = Frame(top, width=600, height=400)
frame.pack()
frame.place(x=500)

# Create a Label Widget to display the text or Image
label = Label(frame, image=new_image)
label.pack()

top.mainloop()
