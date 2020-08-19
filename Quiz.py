from variables import *
import math, random, json
import tkinter as tk
from tkinter import simpledialog, ttk

LARGE_FONT = ("Verdana", 12)

def combine_funcs(*funcs):
        """A function designed to return multiple functions for the tkinter button commands"""
        def combined_func(*args, **kwargs):
                for f in funcs:
                        f(*args, **kwargs)
        return combined_func

class UserData():
        """"""

        def __init__(self, name, score=0, grade="Not Achieved", sections=["Not attempted"]):
                self.name = name
                self.score = score
                self.grade = grade
                self.sections = sections

                self.ongoing = True
                self.question = 0

        def user_write(self):
                if self.score < (0.2 * len(self.sections) * 20) or self.score == 0:
                        self.grade = "Not Achieved"
                elif self.score < (0.4 * len(self.sections) * 20):
                        self.grade = "Achieved"
                elif self.score < (0.8 * len(self.sections) * 20):
                        self.grade = "Merit"
                else:
                        self.grade = "Excellence"

                with open("user_data.json", "r+") as json_file:
                        dic = json.load(json_file)
                        user_data = {self.name: {"name": self.name, "score": self.score, "grade": self.grade, "sections": ", ".join(self.sections)}}
                        dic["users"].update(user_data)
                        json_file.seek(0)
                        json.dump(dic, json_file, indent=4)

class RootFrame(tk.Tk):
        """The frame that stores all important information, and is parent to all other frames
        The show_frame method raises the selected frame to the top
        The generate_quiz method generates a series of frames each containing a unique question, based on the types of questions selected"""

        def __init__(self, *args, **kwargs):
                tk.Tk.__init__(self, *args, **kwargs)
                tk.Tk.iconbitmap(self, default="")
                tk.Tk.wm_title(self, "Level 3 Calculus Revision Quiz")

                topbar = tk.Frame(self)
                topbar.pack(side="top", fill="both", expand=True)
                
                menubar = tk.Menu(self)
                filemenu = tk.Menu(menubar, tearoff=0)
                filemenu.add_command(label="New User", command=lambda: self.new_user(tk.messagebox.askyesno(self, message="New User?")))
                menubar.add_cascade(label="File", menu=filemenu)
                scoremenu = tk.Menu(menubar, tearoff=0)
                scoremenu.add_command(label="Scores", command=lambda: self.score_popup())
                menubar.add_cascade(label="Scoreboards", menu=scoremenu)
                self.config(menu=menubar)

                # I've converted container to self.container so I can access it in a different method
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
                self.users = {}
                self.current_user = ""

                self.frames = {}

                for f in (StartingPage, SelectionPage, EndPage):
                        frame = f(self.container, self)
                        self.frames[f] = frame
                        frame.grid(row=0, column=0, sticky="nsew")

                self.show_frame(StartingPage)

        def show_frame(self, cont):
                frame = self.frames[cont]
                frame.tkraise()

        def score_popup(self):
                popup_box = tk.Tk()
                popup_box.geometry("500x300")

                def remove_user(data, dictionary, user, json_file, value):
                        if value:
                                json_file.close()
                                with open("user_data.json", "w") as json_file_write:
                                        new_dictionary = {i:dictionary[i] for i in dictionary if i!=user}
                                        json_file_write.seek(0)
                                        new_data = {'users': new_dictionary}
                                        json.dump(new_data, json_file_write, indent=4)
                                        json_file_write.close()
                                popup_box.destroy()
                                self.score_popup()

                i = 0
                with open("user_data.json", "r+") as json_file:
                        data = json.load(json_file)
                        users = data['users']
                        for user in data['users']:
                                user_name = tk.StringVar(popup_box)
                                user_name.set(users[user]['name'])
                                user_score = tk.IntVar(popup_box)
                                user_score.set(users[user]['score'])
                                user_grade = tk.StringVar(popup_box)
                                user_grade.set(users[user]['grade'])
                                user_sections = tk.StringVar(popup_box)
                                user_sections.set(users[user]['sections'])

                                delete_user = ttk.Button(popup_box, text="Remove User", command=lambda: remove_user(data, users, user, json_file, tk.messagebox.askyesno(self, message="Remove User?")))
                        
                                name_label = ttk.Label(popup_box, text=user_name.get())
                                name_label.grid(row=i, column=0)
                                score_label = ttk.Label(popup_box, text=user_score.get())
                                score_label.grid(row=i, column=1)
                                grade_label = ttk.Label(popup_box, text=user_grade.get())
                                grade_label.grid(row=i, column=2)
                                sections_label = ttk.Label(popup_box, text=user_sections.get())
                                sections_label.grid(row=i, column=3)
                                delete_user.grid(row=i, column=4)
                        
                                i += 1
                popup_box.mainloop()

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
                                score_modifier = 1
                        elif question <= modifier * section_length + medium_length:
                                difficulty = "medium"
                                score_modifier = 2
                        else:
                                difficulty = "hard"
                                score_modifier = 3

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

                        frame = QuestionPage(self.container, self, question, question_i, score_modifier, length, new_list[i_2][difficulty])
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

        def check_answer(self, answer, correct_answer, score_modifier, page, end_number):
                """Checks if the answer selected by a button is correct"""
                self.users[self.current_user].question = page.number
                if answer == correct_answer:
                        page.correct = 1 * score_modifier
                else:
                        page.correct = 0
                if self.users[self.current_user].question == end_number - 1:
                        self.check_score()

        def check_score(self):
                current_score = 0
                for i in self.frames:
                        if isinstance(i, str):
                                current_score += self.score.get()+self.frames[i].correct
                self.users[self.current_user].score = current_score
                self.score.set(current_score)

        def check_section(self):
                sections = []
                complex_numbers, differentiation, integration = None, None, None
                if self.complex_test.get() == True:
                        sections += [complex_questions]
                        complex_numbers = "Complex Numbers"
                if self.differentiation_test.get() == True:
                        sections += [differentiation_questions]
                        differentiation = "Differentiation"
                if self.integration_test.get() == True:
                        sections += [integration_questions]
                        integration = "Integration"
                self.users[self.current_user].sections = [section for section in [complex_numbers, differentiation, integration] if isinstance(section, str)]
                return sections

        def restart(self, value):
                if value:
                        self.score.set(0)
                        i = len(self.frames) - 4
                        while i > 0:
                                j = "QuestionPage" + str(i)
                                del self.frames[j]
                                i = i - 1
                        self.show_frame(SelectionPage)
                        return True

        def new_user(self, value):
                if self.restart(value):
                        self.users[self.current_user].user_write()
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

                name = tk.StringVar(controller)

                entry = ttk.Entry(self, textvariable=name)
                entry.pack()

                def save_name(saved_name):
                        controller.current_user = saved_name
                        controller.users[saved_name] = UserData(saved_name)

                next_button = ttk.Button(self, text="Next", command=lambda: combine_funcs(save_name(name.get()), controller.show_frame(SelectionPage)))
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
        def __init__(self, parent, controller, number, question_i, score_modifier, end_number, question_list):
                tk.Frame.__init__(self, parent)
                self.number = number
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
                        answer[letter] = ttk.Button(self, text=self.question_list[question_i]['answers'][letter], command=lambda letter=letter, correct_letter=self.question_list[question_i]["correct_answer"], next_page=next_page: combine_funcs(controller.check_answer(letter, correct_letter, score_modifier, self, end_number), controller.show_frame(next_page)))
                        answer[letter].pack()

                back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("QuestionPage" + str(number-1)))
                back_button.pack()
                skip_button = ttk.Button(self, text="Skip", command=lambda next_page=next_page: combine_funcs(controller.check_answer(1, 0, self, end_number), controller.show_frame(next_page)))
                skip_button.pack()
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
                button = ttk.Button(self, text="New quiz", command=lambda: controller.new_user(tk.messagebox.askyesno(self, message="Start again?")))
                button.pack()
                button = ttk.Button(self, text="Quit", command=lambda: controller.quit(tk.messagebox.askyesno(self, message="Quit?")))
                button.pack()

quiz = RootFrame()
quiz.geometry("500x300")
quiz.mainloop()
