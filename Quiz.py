from variables import *
import math
import random
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)

def combine_funcs(*funcs):
        """A function designed to return multiple functions for the tkinter button commands"""
        def combined_func(*args, **kwargs):
                for f in funcs:
                        f(*args, **kwargs)
        return combined_func

class RootFrame(tk.Tk):
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

                for f in (StartingPage, SelectionPage, EndPage):
                        frame = f(self.container, self)
                        self.frames[f] = frame
                        frame.grid(row=0, column=0, sticky="nsew")

                self.show_frame(StartingPage)

        def show_frame(self, cont):
                frame = self.frames[cont]
                frame.tkraise()

        def generate_quiz(self, *question_lists):
                """This method is the same as the for loop in the __init__, except it passes each question as its own instance
                It takes from a quesiton_list generated from the types of question chosen by the user"""
                length, section_length = len(question_lists[0])*10, 10
                new_list = [{"easy": [], "medium": [], "hard": []}, {"easy": [], "medium": [], "hard": []}, {"easy": [], "medium": [], "hard": []}]
                modifier = 1
                # The question_i variable is reset when there is a change in difficulty
                question_i = 0
                difficulty, difficulty_before = "easy", ""
                for question in range(length):

                        difficulty_before = difficulty

                        """The 'i' variable is used to determine which question list the question is taken from.
                        When sections are off, it's random. When they are on, it is in order."""
                        if self.section_check.get() == True:
                                modifier = math.floor(question / 10)
                                i = modifier
                                # The i_2 here selects the corresponding question type with the new list
                                i_2 = i
                                # The difficulty lengths are the same across 10 questions
                                easy_length, medium_length = 3, 7
                        else:
                                i = random.randint(0,len(question_lists[0])-1)
                                # Because the question types are random, it only uses it within the same dictionary in the list
                                i_2 = 0
                                # Difficulty lengths adjust depending on the quiz length
                                easy_length, medium_length = (length / 3), (3 * length / 4)
                                section_length = 0
                                        
                        if question <= modifier * section_length + easy_length:
                                difficulty = "easy"
                        elif question <= modifier * section_length + medium_length:
                                difficulty = "medium"
                        else:
                                difficulty = "hard"

                        # If there is a change in difficulty, reset question_i so that the question can properly index it
                        if difficulty_before != difficulty:
                                question_i = 0

                        random.shuffle(question_lists[0][i][difficulty])
                        # Checks to see if there is a duplicate, duplicate = shuffle again
                        while question_lists[0][i][difficulty][0] in new_list[i_2][difficulty]:
                                random.shuffle(question_lists[0][i][difficulty])
                        
                        new_list[i_2][difficulty] += [question_lists[0][i][difficulty][0]]
                        
                        if self.section_check.get() == False:
                                # When there are no sections, disable question_i functionality
                                question_i = len(new_list[i_2][difficulty]) - 1

                        frame = QuestionPage(self.container, self, question, question_i, length, new_list[i_2][difficulty])
                        self.frames["QuestionPage" + str(question)] = frame
                        frame.grid(row=0, column=0, sticky="nsew")

                        question_i += 1

        def start_quiz(self):
                section_list = self.check_section()
                if section_list == []:
                        tk.messagebox.showwarning(self, message="Please select a question type.")
                else:
                        self.generate_quiz(section_list)
                        self.show_frame("QuestionPage0")

        def check_answer(self, answer, correct_answer, page):
                """Checks if the answer selected by a button is correct"""
                if answer == correct_answer:
                        page.correct = 1
                else:
                        page.correct = 0

        def check_score(self):
                for i in self.frames:
                        if isinstance(i, str):
                                self.score.set(self.score.get()+self.frames[i].correct)

        def check_section(self):
                sections = []
                if self.complex_test.get() == True:
                        sections += [complex_questions]
                if self.differentiation_test.get() == True:
                        sections += [differentiation_questions]
                if self.integration_test.get() == True:
                        sections += [integration_questions]
                return sections

        def restart(self, value):
                if value:
                        self.score.set(0)
                        i = len(self.frames) - 4
                        while i > 0:
                                j = "QuestionPage" + str(i)
                                del self.frames[j]
                                i = i - 1
                        self.show_frame(StartingPage)
        
        def quit(self, value):
                if value:
                        self.destroy()

class StartingPage(tk.Frame):
        """This page contains a next button to the selection page"""
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                label = ttk.Label(self, text="This is the start page", font=LARGE_FONT)
                label.pack()

                next_button = ttk.Button(self, text="Next", command=lambda: controller.show_frame(SelectionPage))
                next_button.pack()

                button = ttk.Button(self, text="Quit", command=lambda: controller.quit(tk.messagebox.askyesno(self, message="Quit?")))
                button.pack()

class SelectionPage(tk.Frame):
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

                button = ttk.Button(self, text="Start Quiz", command=lambda: controller.start_quiz())
                button.pack()

class QuestionPage(tk.Frame):
        """This is the general frame for questions, which will change depending on the number and type of question asked
        There will always be multiple instances of this object
        For each instance of a QuestionPage, the number increments by one, which takes the next question in the question_list
        This question_list is generated based on the checkboxes the user checked before"""
        def __init__(self, parent, controller, number, question_i, end_number, question_list):
                tk.Frame.__init__(self, parent)
                self.question_list = question_list
                text = "A question" + str(number+1)
                label = ttk.Label(self, text=text, font=LARGE_FONT)
                label.pack(pady=10,padx=10)

                self.correct = 0

                """Essentially, each question is index 0 of the shuffled list. At the end, this index is deleted, so that old index 1 becomes index 0.
                This way, no question is repeated."""
                question = ttk.Label(self, text=self.question_list[question_i]['question'])
                question.pack()

                if number == end_number - 1:
                        next_page = EndPage
                else:
                        next_page = "QuestionPage" + str(number+1)

                """The for loop here generates buttons of each answer. Each button has the command to check if it was right, and then move to the next frame.
                I've put this into a for loop to make it easier to program"""
                answer = {}
                for letter in ['a','b','c','d']:
                        answer[letter] = ttk.Button(self, text=self.question_list[question_i]['answers'][letter], command=lambda letter=letter, correct_letter=self.question_list[question_i]["correct_answer"], next_page=next_page: combine_funcs(controller.check_answer(letter, correct_letter, self), controller.show_frame(next_page)))
                        answer[letter].pack()

                back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("QuestionPage" + str(number-1)))
                back_button.pack()

                popup_button = ttk.Button(self, text="Restart", command=lambda: controller.restart(tk.messagebox.askyesno(self, message="Restart?")))
                popup_button.pack()

                button = ttk.Button(self, text="Quit", command=lambda: controller.quit(tk.messagebox.askyesno(self, message="Quit?")))
                button.pack()

class EndPage(tk.Frame):
        """"""
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                label = ttk.Label(self, text="End score", font=LARGE_FONT)
                label.pack(pady=10,padx=10)

                answers_correct = ttk.Label(self, textvariable=controller.score)
                answers_correct.pack()
                
                button2 = ttk.Button(self, text="get score", command=lambda: controller.check_score())
                button2.pack()
                
                button = ttk.Button(self, text="Restart quiz", command=lambda: controller.restart(tk.messagebox.askyesno(self, message="Restart?")))
                button.pack()

                button = ttk.Button(self, text="Quit", command=lambda: controller.quit(tk.messagebox.askyesno(self, message="Quit?")))
                button.pack()

quiz = RootFrame()
quiz.geometry("500x300")
quiz.mainloop()
