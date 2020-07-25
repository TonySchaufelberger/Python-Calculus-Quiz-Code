import random
import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)

differentiation_questions = {"easy": [
  {
    "question": "differentiation:What is the conjugate of 1 + 2i?",
    "answers": {
      "a": '2i',
      "b": '(-1 - 2i)',
      "c": '(-1 + 2i)',
      "d": '(1 - 2i)'
    },
    "correct_answer": 'd'
  },
  {
    "question": "differentiation:Simplify (i^3).",
    "answers": {
      "a": '(-i)',
      "b": '(i)',
      "c": '(-1)',
      "d": '(1)'
    },
    "correct_answer": 'a'
  },
  {
    "question": "differentiation:easy3",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "differentiation:easy4",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "differentiation:easy5",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "differentiation:easy6",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  }],
        "medium": [
  {
    "question": "differentiation:test",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "differentiation:medium1",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "differentiation:medium2",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "differentiation:medium3",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "differentiation:medium4",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "differentiation:medium5",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "differentiation:medium6",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "differentiation:medium7",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  }],
        "hard": [
  {
    "question": "differentiation:hard1",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "differentiation:hard2",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "differentiation:hard3",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "differentiation:hard4",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  }]
}

integration_questions = {"easy": [
  {
    "question": "integration:What is the conjugate of 1 + 2i?",
    "answers": {
      "a": '2i',
      "b": '(-1 - 2i)',
      "c": '(-1 + 2i)',
      "d": '(1 - 2i)'
    },
    "correct_answer": 'd'
  },
  {
    "question": "integration:Simplify (i^3).",
    "answers": {
      "a": '(-i)',
      "b": '(i)',
      "c": '(-1)',
      "d": '(1)'
    },
    "correct_answer": 'a'
  },
  {
    "question": "integration:easy3",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "integration:easy4",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "integration:easy5",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "integration:easy6",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  }],
        "medium": [
  {
    "question": "integration:test",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "integration:medium1",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "integration:medium2",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "integration:medium3",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "integration:medium4",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "integration:medium5",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "integration:medium6",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "integration:medium7",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  }],
        "hard": [
  {
    "question": "integration:hard1",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "integration:hard2",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "integration:hard3",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "integration:hard4",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  }]
}

complex_questions = {
        "easy": [
  {
    "question": "complex:What is the conjugate of 1 + 2i?",
    "answers": {
      "a": '2i',
      "b": '(-1 - 2i)',
      "c": '(-1 + 2i)',
      "d": '(1 - 2i)'
    },
    "correct_answer": 'd'
  },
  {
    "question": "complex:Simplify (i^3).",
    "answers": {
      "a": '(-i)',
      "b": '(i)',
      "c": '(-1)',
      "d": '(1)'
    },
    "correct_answer": 'a'
  },
  {
    "question": "complex:easy3",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "complex:easy4",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "complex:easy5",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "complex:easy6",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  }],
        "medium": [
  {
    "question": "complex:test",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "complex:medium1",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "complex:medium2",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "complex:medium3",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "complex:medium4",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "complex:medium5",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "complex:medium6",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "complex:medium7",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  }],
        "hard": [
  {
    "question": "complex:hard1",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "complex:hard2",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "complex:hard3",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  },
  {
    "question": "complex:hard4",
    "answers": {
      "a": 'a',
      "b": 'b',
      "c": 'c',
      "d": 'd'
    },
    "correct_answer": 'a'
  }]
}

def combine_funcs(*funcs):
        """A function designed to return multiple functions for the tkinter button commands"""
        def combined_func(*args, **kwargs):
                for f in funcs:
                        f(*args, **kwargs)
        return combined_func

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

                self.section_check = tk.BooleanVar(self)

                self.score = tk.IntVar(self, 0)

                self.frames = {}

                for f in (startingPage, selectionPage):
                        frame = f(self.container, self)
                        self.frames[f] = frame
                        frame.grid(row=0, column=0, sticky="nsew")

                self.show_frame(startingPage)

        def show_frame(self, cont):
                frame = self.frames[cont]
                frame.tkraise()

        def generate_quiz(self, *question_lists):
                """This method is the same as the for loop in the __init__, except it passes each question as its own instance
                It takes from a quesiton_list generated from the types of question chosen by the user"""
                if self.section_check.get() == False:
                        new_list = {"easy": [], "medium": [], "hard":[]}
                        for question in range(10):
                                i = random.randint(0,len(question_lists)-1)
                                if question <= 3:
                                        difficulty = "easy"
                                elif question <= 8:
                                        difficulty = "medium"
                                else:
                                        difficulty = "hard"
                                random.shuffle(question_lists[i][difficulty])
                                new_list[difficulty] += [question_lists[i][difficulty][0]]

                                frame = questionPage(self.container, self, question, new_list[difficulty])
                                self.frames["questionPage" + str(question)] = frame
                                frame.grid(row=0, column=0, sticky="nsew")
                else:
                        pass

        def check_answer(self, answer, correct_answer):
                """Checks if the answer selected by a button is correct"""
                if answer == correct_answer:
                        self.score.set(self.score.get()+1)

        def check_section(self):
                sections = []
                if self.complex_test.get() == True:
                        sections += complex_questions
                if self.differentiation_test.get() == True:
                        sections += differentiation_questions
                if self.integration_test.get() == True:
                        sections += integration_questions
                return sections
                

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
        """This page contains check buttons to toggle which type of question will be asked in the quiz
        It toggles if the question_list will include complex, differentiation and/or integration, and whether it's separated by section"""
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

                section_check_on = ttk.Radiobutton(self, text="Sections On", variable=controller.section_check, value=True)
                section_check_off = ttk.Radiobutton(self, text="Sections Off", variable=controller.section_check, value=False)
                section_check_on.pack()
                section_check_off.pack()

                button = ttk.Button(self, text="Start Quiz", command=lambda: combine_funcs(controller.generate_quiz(controller.check_section()), controller.show_frame("questionPage0")))
                button.pack()

class questionPage(tk.Frame):
        """This is the general frame for questions, which will change depending on the number and type of question asked
        There will always be multiple instances of this object
        For each instance of a questionPage, the number increments by one, which takes the next question in the question_list
        This question_list is generated based on the checkboxes the user checked before"""
        def __init__(self, parent, controller, number, question_list):
                tk.Frame.__init__(self, parent)
                self.question_list = question_list
                text = "A question" + str(number+1)
                label = ttk.Label(self, text=text, font=LARGE_FONT)
                label.pack(pady=10,padx=10)

                """Essentially, each question is index 0 of the shuffled list. At the end, this index is deleted, so that old index 1 becomes index 0.
                This way, no question is repeated."""
                question = ttk.Label(self, text=self.question_list[0]['question'])
                question.pack()

                answer = {}
                """The for loop here generates buttons of each answer. Each button has the command to check if it was right, and then move to the next frame.
                I've put this into a for loop to make it easier to program"""
                for letter in ['a','b','c','d']:
                        answer[letter] = ttk.Button(self, text=self.question_list[0]['answers'][letter], command=lambda letter=letter, correct_letter=self.question_list[0]["correct_answer"]: combine_funcs(controller.check_answer(letter, correct_letter), controller.show_frame("questionPage" + str(number+1))))
                        answer[letter].pack()
                
                del self.question_list[0]

                answers_correct = ttk.Label(self, textvariable=controller.score)
                answers_correct.pack()


quiz = rootFrame()
quiz.geometry("500x300")
quiz.mainloop()
