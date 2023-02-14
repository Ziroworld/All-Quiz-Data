from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar # progressbar is used for updating a bar
from PIL import Image, ImageTk

screen = Tk()

#IMage
Img = Image.open("E:\\1.Quiz\\newImg.png")
resizeImg = Img.resize((380,330))
convertedImg = ImageTk.PhotoImage( resizeImg )

# Making the window in middle
height = 500
width = 540
x = (screen.winfo_screenwidth()//2)-(width//2)
y = (screen.winfo_screenheight()//2)-(height//2)
screen.geometry('{}x{}+{}+{}'.format(width,height,x,y))
screen.overrideredirect(True) # to not diplay the top section

screen.config(background = "#251C28")
welcome_label = Label(text = "WELCOME TO THE QUIZ GAME", bg = "#251C28", font=("Bodoni MT", 18, "bold"), fg = "#FFF")
welcome_label.place(x = 80, y = 15)

# image placeholder
bg_label = Label(screen , image = convertedImg , bg="#251C28")
bg_label.place(x = 90 , y=65)

#setting up the progressBar
progress_label = Label(screen, text="Loading progress......",font=("Bodoni MT", 14, "bold"),fg = "#FFF",bg="#251C28")
progress_label.place(x = 170, y =420)

progress = ttk.Style()
progress.theme_use('clam')
progress.configure("red.Horizontal.TProgressbar", background = "#108cff")

progress = Progressbar(screen, orient = HORIZONTAL, length = 400, mode = "determinate", style = "red.Horizontal.TProgressbar")
progress.place(x=60,y = 450)

i = 0

# loop to start the progress
def load() :
    global i 
    if i <= 10 : 
        txt = 'Loading Progress......' + (str(10*i) +' %')
        progress_label.config(text = txt)
        progress_label.after(500,load)    
        progress['value'] = 10 * i
        i += 1
    else :
        print("hello world ")
        print("nilesh is an idiots ")
        pass
 
      
load()
screen.mainloop()