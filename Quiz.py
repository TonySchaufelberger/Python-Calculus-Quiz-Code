import tkinter as tk

LARGE_FONT = ("Verdana", 12)

class rootFrame(tk.Tk):
        """"""
        def __init__(self, *args, **kwargs):
                tk.Tk.__init__(self, *args, **kwargs)
                container = tk.Frame(self)
                container.pack(side="top", fill="both", expand=True)
                container.grid_rowconfigure(0, weight=1)
                container.grid_columnconfigure(0, weight=1)
                container.grid_columnconfigure(1, weight=1)

                self.frames = {}
                frame = startingPage(container, self)
                self.frames[startingPage] = frame
                frame.grid(row=0, column=0, sticky="nsew")

                self.show_frame(startingPage)

        def show_frame(self, cont):
                frame = self.frames[cont]
                frame.tkraise()

def test(message):
        print(message)

class startingPage(tk.Frame):
        """"""
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                label = tk.Label(self, text="This is the start page", font=LARGE_FONT)
                label.grid(row=0,column=0)

                button = tk.Button(self, text="Next", command=lambda: test("hi"))
                button.grid(row=0,column=1)

class selectionPage(tk.Frame):
        """"""
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                label = tk.Label(self, text="This is the section page", font=LARGE_FONT)
                label.pack(pady=10,padx=10)

quiz = rootFrame()
quiz.geometry("500x300")
quiz.mainloop()
