from sys import platform
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font, os
from PIL import Image, ImageTk
import core

class GUI():
    def __init__(self, root):
        self.root = root
        root.title("pix2msch")
        root.resizable(False, False)
        root.geometry("600x500")

        photo = PhotoImage(file = "background.png")
        background = Label(root, image = photo)
        background.image = photo
        background.place(x = -2, y = -2)
        
        font = tkinter.font.Font(family="Consolas", size=12)
        
        self.dither = IntVar(value=1)
        self.dither_c = Checkbutton(
        root, font = font, text="Dithering",
        bg = "#35373C", fg = "#B7BBCE",
        activebackground="#515359", activeforeground="#cccccc", bd = 0,
        selectcolor="#515359",
        var = self.dither
        )
        self.dither_c.place(x = 300, y = 375)
        
        self.name = StringVar()
        self.path = StringVar()
        self.transparency = StringVar()
        
        name_entry = Entry(root, font = font, width = 25, bg = "#35373C", fg = "#B7BBCE", textvariable = self.name)
        name_entry.place(x = 300, y = 278)
        
        path_entry = Entry(root, font = font, width = 25, bg = "#35373C", fg = "#B7BBCE", textvariable = self.path)
        path_entry.place(x = 300, y = 308)
        
        transparency_entry = Entry(root, font = font, width = 25, bg = "#35373C", fg = "#B7BBCE", textvariable = self.transparency)
        transparency_entry.place(x = 300, y = 338)
        
        name_entry.insert(0, "schematic")
        if platform == "windows":
            path_entry.insert(0, "%appdata%\\Mindustry\\schematics")
        elif platform == "linux":
            path_entry.insert(0, "~/.local/share/Mindustry/schematics/")
        else:
            path_entry.insert(0, "Enter Mindustry schematic path...")
         
        transparency_entry.insert(0, "127")
        
        self.open_image_b = Button(root, font = font, command=self.open_image, text = "Open Image...", bg = "#35373C", fg = "#B7BBCE", activebackground="#515359", activeforeground="#cccccc", bd = 0)
        self.open_image_b.place(x = 300, y = 240, anchor = CENTER)
        
        convert_b = Button(root, command=self.convert, font = font, text = "Convert to msch...", bg = "#35373C", fg = "#B7BBCE", activebackground="#515359", activeforeground="#cccccc", bd = 0)
        convert_b.place(x = 350, y = 450, anchor = CENTER)
        
        preview_b = Button(root, command=self.preview, font = font, text = "Preview", bg = "#35373C", fg = "#B7BBCE", activebackground="#515359", activeforeground="#cccccc", bd = 0)
        preview_b.place(x = 200, y = 450, anchor = CENTER)
        
        
        
    def open_image(self):
        root.update()
        self.file = filedialog.askopenfilename()
        self.open_image_b.configure(text = self.file)
        try:
            self.image = Image.open(self.file)
        except:
            self.open_image_b.configure(text = "Invalid Image file!")
            
        root.update()
        
    def convert(self):
        try:
            int(self.transparency.get())
            self.image
            if int(self.transparency.get()) > 255:
                messagebox.showerror("Error", "Transparency Treshold must not exceed 255")
                raise Exception
            elif int(self.transparency.get()) < 0:
                messagebox.showerror("Error", "Transparency Treshold must not be negative")
                raise Exception
            if not(os.path.isdir(os.path.expandvars(self.path.get()))):
                messagebox.showerror("Error", "Invalid path")
                raise Exception
            if self.name.get() == "":
                messagebox.showerror("Error", "Please enter a name")
                raise Exception
        except AttributeError:
            messagebox.showerror("Error", "No image selected")
        except ValueError:
            messagebox.showerror("Error", "Transparency Treshold must be a number")
        else:
            try:
                core.imgtomsch(self.file, self.name.get(), self.path.get(), self.dither.get(), int(self.transparency.get()))
            except Exception as e:
                messagebox.showerror("oh no", e)
            else:
                messagebox.showinfo("Success", "Successfully converted image to msch")
    
    def preview(self):
        
        try:
            self.window.destroy()
        except:
            pass
        
        try:
            int(self.transparency.get())
            self.image
            if int(self.transparency.get()) > 255:
                messagebox.showerror("Error", "Transparency Treshold must not exceed 255")
                raise Exception
            elif int(self.transparency.get()) < 0:
                messagebox.showerror("Error", "Transparency Treshold must not be negative")
                raise Exception
        except AttributeError:
            messagebox.showerror("Error", "No image selected")
        except ValueError:
            messagebox.showerror("Error", "Transparency Treshold must be a number")
        else:
            targetsize = 700
            qimg = core.quantize(self.image, self.dither.get(), 127)[1]
            
            sizemultiplier = targetsize/max(qimg.size)
            self.window = Toplevel(root)
            self.window.geometry(str(int(qimg.size[0]*sizemultiplier)) + "x" + str(int(qimg.size[1]*sizemultiplier)))
            
            image = ImageTk.PhotoImage(qimg.resize((int(qimg.size[0]*sizemultiplier), int(qimg.size[1]*sizemultiplier))))
            background = Label(self.window, image = image)
            self.window.image = image
            self.window.resizable(False, False)
            background.place(x = -2, y = -2)

root = Tk()
try:
    GUI(root)
except Exception as e:
    messagebox.showerror("oh no", e)
root.mainloop()
