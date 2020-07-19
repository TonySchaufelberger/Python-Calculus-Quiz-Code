import random
import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)

complex_questions = (
  {
    "question": "What is the conjugate of 1 + 2i?",
    "answers": {
      "a": '2i',
      "b": '(-1 - 2i)',
      "c": '(-1 + 2i)',
      "d": '(1 - 2i)'
    },
    "correct_answer": 'd'
  },
  {
    "question": "Simplify (i^3).",
    "answers": {
      "a": '(-i)',
      "b": '(i)',
      "c": '(-1)',
      "d": '(1)'
    },
    "correct_answer": 'a'
  }
)

def combine_funcs(*funcs):
        """A function designed to return multiple functions for the tkinter button commands"""
        def combined_func(*args, **kwargs):
                for f in funcs:
                        f(*args, **kwargs)
        return combined_func

def randomizer(*questions):
        """A function which randomizes a list, and returns the randomized list"""
        randomized_questions = random.sample(range(0, int(len(questions))+1), int(len(questions))+1)
        return randomized_questions

class ok_popup:
        """Simply opens a new tkinter window when called. Its only button/method is the OK button."""
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
        """A child of the ok_popup class, inherits everything but changes the buttons into Yes and No,
        Yes: closes all windows
        No: closes only the popup
        The yes_function method is used for the yes button, is overrided in the child class"""
        def __init__(self, msg, parent):
                self.parent = parent
                super().__init__(msg)

        def buttons(self, msg):
                button = ttk.Button(self.popup_box, text="Yes", command=combine_funcs(self.parent.destroy, self.popup_box.destroy))
                button2 = ttk.Button(self.popup_box, text="No", command=self.popup_box.destroy)
                button.pack()
                button2.pack()

        def yes_function(self):
                pass

class cancel_popup(quit_popup):
        """A child of the quit_popup, inherits the same buttons but adds new functionality for the first button
        Yes: yes_function
        No: closes the popup"""
        def __init__(self, msg, parent, func):
                self.func = func
                super().__init(msg, parent)

        def yes_function(self):
                pass


class rootFrame(tk.Tk):
        """The frame that stores all important information, and is parent to all other frames
        The show_frame method raises the selected frame to the top
        The generate_quiz method generates a series of frames each containing a unique question, based on the types of questions selected"""

        def __init__(self, *args, **kwargs):
                tk.Tk.__init__(self, *args, **kwargs)
                tk.Tk.iconbitmap(self, default="")
                tk.Tk.wm_title(self, "Level 3 Calculus Revision Quiz")

                # I've converted container to self.container so I can access it in a different method, hopefully I will find a way to revert it
                self.container = tk.Frame(self)
                self.container.pack(side="top", fill="both", expand=True)
                self.container.grid_rowconfigure(0, weight=1)
                self.container.grid_columnconfigure(0, weight=1)
                self.container.grid_columnconfigure(1, weight=1)

                self.complex_test = tk.BooleanVar(self)
                self.differentiation_test = tk.BooleanVar(self)
                self.integration_test = tk.BooleanVar(self)

                self.frames = {}

                for f in (startingPage, selectionPage):
                        frame = f(self.container, self)
                        self.frames[f] = frame
                        frame.grid(row=0, column=0, sticky="nsew")

                self.show_frame(startingPage)

        def show_frame(self, cont):
                frame = self.frames[cont]
                frame.tkraise()

        def generate_quiz(self, questions):
                """This method is the same as the for loop in the __init__, except it passes each question as its own instance"""
                for question in range(10):
                        frame = questionPage(self.container, self, question)
                        self.frames["questionPage" + str(question)] = frame
                        frame.grid(row=0, column=0, sticky="nsew")

class startingPage(tk.Frame):
        """This page contains a next button to the selection page"""
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                label = ttk.Label(self, text="This is the start page", font=LARGE_FONT)
                label.grid(row=0,column=0)

                button = ttk.Button(self, text="Next", command=lambda: controller.show_frame(selectionPage))
                button.grid(row=0,column=1)

                popup_button = ttk.Button(self, text="popup", command=lambda: quit_popup("close", controller))
                popup_button.grid(row=0,column=2)

class selectionPage(tk.Frame):
        """This page contains check buttons to toggle which type of question will be asked in the quiz"""
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                label = ttk.Label(self, text="This is the section page", font=LARGE_FONT)
                label.pack(pady=10,padx=10)

                complex_check = ttk.Checkbutton(self, text="Test Complex Numbers?", variable=controller.complex_test)
                differentiation_check = ttk.Checkbutton(self, text="Test Differentiation?", variable=controller.differentiation_test)
                integration_check = ttk.Checkbutton(self, text="Test Integration?", variable=controller.integration_test)
                complex_check.pack()
                differentiation_check.pack()
                integration_check.pack()

                button = ttk.Button(self, text="Start Quiz", command=lambda: combine_funcs(controller.generate_quiz(0), controller.show_frame("questionPage0")))
                button.pack()

class questionPage(tk.Frame):
        """This is the general frame for questions, which will change depending on the number and type of question asked
        There will always be multiple instances of this object"""
        def __init__(self, parent, controller, number):
                tk.Frame.__init__(self, parent)
                text = "A question" + str(number+1)
                label = ttk.Label(self, text=text, font=LARGE_FONT)
                label.pack(pady=10,padx=10)

                button = ttk.Button(self, text="next question", command=lambda: controller.show_frame("questionPage" + str(number+1)))
                button.pack()

quiz = rootFrame()
quiz.geometry("500x300")
quiz.mainloop()
