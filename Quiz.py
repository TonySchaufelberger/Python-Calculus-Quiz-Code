import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)

def combine_funcs(*funcs):
        def combined_func(*args, **kwargs):
                for f in funcs:
                        f(*args, **kwargs)
        return combined_func

class ok_popup:
        """"""
        def __init__(self, msg):
                self.msg = msg
                self.popup_box = tk.Tk()
                self.popup_box.wm_title("Warning")
                label = ttk.Label(self.popup_box, text=msg, font=LARGE_FONT)
                label.pack(side="top", fill="x")
                self.buttons(self.msg)
                self.popup_box.mainloop()

        def buttons(self, msg):
                button = ttk.Button(self.popup_box, text="OK", command=self.popup_box.destroy)
                button.pack()

class quit_popup(ok_popup):
        """"""
        def __init__(self, msg, parent):
                self.parent = parent
                super().__init__(msg)

        def buttons(self, msg):
                button = ttk.Button(self.popup_box, text="Yes", command=combine_funcs(self.parent.destroy, self.popup_box.destroy))
                button2 = ttk.Button(self.popup_box, text="No", command=self.popup_box.destroy)
                button.pack()
                button2.pack()

class cancel_popup(quit_popup):
        """"""
        def __init__(self, msg, parent, func):
                self.func = func
                super().__init(msg, parent)

        def yes_function(self):
                pass


class rootFrame(tk.Tk):
        """"""
        def __init__(self, *args, **kwargs):
                tk.Tk.__init__(self, *args, **kwargs)
                tk.Tk.iconbitmap(self, default="")
                tk.Tk.wm_title(self, "Level 3 Calculus Revision Quiz")
                container = tk.Frame(self)
                container.pack(side="top", fill="both", expand=True)
                container.grid_rowconfigure(0, weight=1)
                container.grid_columnconfigure(0, weight=1)
                container.grid_columnconfigure(1, weight=1)

                self.frames = {}

                for f in (startingPage, selectionPage):
                        frame = f(container, self)
                        self.frames[f] = frame
                        frame.grid(row=0, column=0, sticky="nsew")

                self.show_frame(startingPage)

        def show_frame(self, cont):
                frame = self.frames[cont]
                frame.tkraise()

class startingPage(tk.Frame):
        """"""
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                label = ttk.Label(self, text="This is the start page", font=LARGE_FONT)
                label.grid(row=0,column=0)

                button = ttk.Button(self, text="Next", command=lambda: controller.show_frame(selectionPage))
                button.grid(row=0,column=1)

                popup_button = ttk.Button(self, text="popup", command=lambda: quit_popup("close", controller))
                popup_button.grid(row=0,column=2)


class selectionPage(tk.Frame):
        """"""
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                label = ttk.Label(self, text="This is the section page", font=LARGE_FONT)
                label.pack(pady=10,padx=10)

quiz = rootFrame()
quiz.geometry("500x300")
quiz.mainloop()
