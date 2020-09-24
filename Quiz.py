from variables import *
import math, random, json, webbrowser
import tkinter as tk
from tkinter import simpledialog, ttk
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
# Code sourced from https://github.com/ifwe/digsby/blob/f5fe00244744aa131e07f09348d10563f3d8fa99/digsby/src/gui/native/win/winfonts.py#L15
FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20

def loadfont(fontpath, private=True, enumerable=False):
    '''
    Makes fonts located in file `fontpath` available to the font system.

    `private`     if True, other processes cannot see this font, and this 
                  font will be unloaded when the process dies
    `enumerable`  if True, this font will appear when enumerating fonts

    See https://msdn.microsoft.com/en-us/library/dd183327(VS.85).aspx

    '''
    if isinstance(fontpath, bytes):
        pathbuf = create_string_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
    elif isinstance(fontpath, str):
        pathbuf = create_unicode_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('fontpath must be of type str or unicode')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)

loadfont("Montserrat-Regular.ttf")
loadfont("Roboto-Regular.ttf")

LARGE_FONT = ("Roboto", 12)
REGULAR_FONT = ("Montserrat Regular", 10)
SMALL_FONT = ("Montserrat Regular", 8)
LIGHT_THEME = {"COLOR_PRIMARY": "#fafafa", "color_font": "#000000"}
DARK_THEME = {"COLOR_PRIMARY": "#121212", "color_font": "#6695ed"}
CORRECT_COLOUR = "#91f78f"
INCORRECT_COLOUR = "#f77c7c"
THEMING = (LIGHT_THEME, DARK_THEME)
MAX_NAME_LENGTH = 16
SPECIAL_CHARACTERS = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "=", "`", "~", "<", ">",
                      "/", "?", ";", "[", "]", "{", "}", "|", "\\", "'", '"', ",", "."]

def combine_funcs(*funcs):
        """A function designed to return multiple functions for the tkinter button commands"""
        def combined_func(*args, **kwargs):
                for f in funcs:
                        f(*args, **kwargs)
        return combined_func

def row_column_configure(parent, rows, columns):
        for i in range(rows):
                parent.rowconfigure(i, weight=1)
        for j in range(columns):
                parent.columnconfigure(j, weight=1)

def open_help():
        webbrowser.open("https://github.com/TonySchaufelberger/Python-Calculus-Quiz-Code", new=2)

def help_callback(event):
        open_help()

def check_name_entry(text):
        # Stops name entry from allowing numbers or special characters
        for letter in text:
            if letter in SPECIAL_CHARACTERS or letter.isdigit() or len(text) > MAX_NAME_LENGTH:
                return False
        return True

class UserData():
        """"""

        def __init__(self, name, score=0, number_correct=0, grade="Not Achieved", year=13, sections=["Not attempted"]):
                # Stores each user with selected variables
                self.name = name
                self.score = score
                self.number_correct = number_correct
                self.grade = grade
                self.year = year
                self.sections = sections

                self.ongoing = True
                self.question = 0

        def user_write(self):
                # Writes the user to the json file by converting the json into a python dictionary, appending the user and then rewriting the json
                with open("user_data.json", "r+") as json_file:
                        dic = json.load(json_file)
                        i = 2
                        original_name = self.name
                        while original_name in dic["users"]:
                                # Makes it so that repeated names are valid
                                original_name = self.name
                                original_name = "{}({})".format(self.name, i)
                                i += 1
                        self.name = original_name
                        user_data = {self.name: {"name": self.name, "score": self.score, "number_correct": self.number_correct, "grade": self.grade, "year": self.year, "sections": ", ".join(self.sections)}}
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
                self.minsize(500, 300)
                self.maxsize(1000, 600)
                self.bind('<F1>', help_callback)

                topbar = tk.Frame(self)
                topbar.pack(side="top", fill="both", expand=False)

                # Menubar is for file, scoreboard, options and help access
                menubar = tk.Menu(topbar)
                filemenu = tk.Menu(menubar, tearoff=0)
                filemenu.add_command(label="New User", command=lambda: self.new_user(tk.messagebox.askyesno("Confirmation", message="New User?")), font=SMALL_FONT)
                self.load_user = tk.Menu(filemenu, tearoff=0)
                filemenu.add_cascade(label="Load User", menu=self.load_user, font=SMALL_FONT, state=tk.DISABLED)
                #self.load_user_set()
                                
                menubar.add_cascade(label="File", menu=filemenu, font=SMALL_FONT)
                optionmenu = tk.Menu(menubar, tearoff=0)
                thememenu = tk.Menu(filemenu, tearoff=0)
                thememenu.add_command(label="Light Theme", command=lambda: self.set_theme(0))
                thememenu.add_command(label="Dark Theme", command=lambda: self.set_theme(1))
                optionmenu.add_cascade(label="Themes", menu=thememenu, font=SMALL_FONT)
                menubar.add_cascade(label="Options", menu=optionmenu, font=SMALL_FONT)
                scoremenu = tk.Menu(menubar, tearoff=0)
                scoremenu.add_command(label="Show Scores", command=lambda: self.score_popup(), font=SMALL_FONT)
                menubar.add_cascade(label="Scoreboards", menu=scoremenu, font=SMALL_FONT)
                menubar.add_command(label="(F1) Help", command=lambda: open_help(), font=SMALL_FONT)
                self.config(menu=menubar)

                self.style = ttk.Style()
                self.theme_number = tk.IntVar(self, 0)
                
                # I've converted container to self.container so I can access it in a different method
                self.container = tk.Frame(self)
                self.container.pack(side="right", fill="both", expand=True)
                self.configure_theme()
                row_column_configure(self.container, 1, 1)
                self.complex_test = tk.BooleanVar(self)
                self.differentiation_test = tk.BooleanVar(self)
                self.integration_test = tk.BooleanVar(self)
                self.section_check = tk.BooleanVar(self)
                self.score = tk.IntVar(self, 0)
                self.number_correct = tk.IntVar(self, 0)
                self.grade = tk.StringVar(self, "Not Attempted")
                self.year = tk.IntVar(self, 13)
                self.users = {}
                self.user_saved = False
                self.current_user = tk.StringVar(self)
                self.frames = {}

                self.initialize_frames()

                self.show_frame(StartingPage)

        def initialize_frames(self):
                for f in (StartingPage, SelectionPage, EndPage):
                        frame = f(self.container, self)
                        self.frames[f] = frame
                        frame.grid(row=0, column=0, sticky="nsew")

        def show_frame(self, cont):
                frame = self.frames[cont]
                frame.tkraise()

        def set_theme(self, theme_chosen_number):
                if tk.messagebox.askyesno("Warning", message="Warning: this will restart the quiz and remove all progress. Proceed?"):
                        self.theme_number.set(theme_chosen_number)
                        self.initialize_frames()
                        self.configure_theme()
                        self.show_frame(StartingPage)

        """def load_user_set(self, new_user=None):
                with open("user_data.json", "r+") as json_file:
                        data = json.load(json_file)
                        users = {k : v for k, v in sorted(data['users'].items())}
                        if bool(users):
                                if new_user != None:
                                        for i in range(len(users)-1):
                                                self.load_user.delete([user for user in users if user!=new_user][i])
                                for user in users:
                                        self.load_user.add_command(label=user)"""

        def configure_theme(self):
                self.style.configure('TButton', font=SMALL_FONT, background=THEMING[self.theme_number.get()]["COLOR_PRIMARY"])
                self.style.configure('TLabel', foreground=THEMING[self.theme_number.get()]["color_font"], background=THEMING[self.theme_number.get()]["COLOR_PRIMARY"])
                self.style.configure('TMenubutton', font=SMALL_FONT, foreground=THEMING[self.theme_number.get()]["color_font"], background=THEMING[self.theme_number.get()]["COLOR_PRIMARY"])
                self.style.configure('TCheckbutton', font=SMALL_FONT, foreground=THEMING[self.theme_number.get()]["color_font"], background=THEMING[self.theme_number.get()]["COLOR_PRIMARY"])
                self.style.configure('TRadiobutton', font=SMALL_FONT, foreground=THEMING[self.theme_number.get()]["color_font"], background=THEMING[self.theme_number.get()]["COLOR_PRIMARY"])
                self.container.config(bg=THEMING[self.theme_number.get()]["COLOR_PRIMARY"])

        def score_popup(self):
                popup_box = tk.Tk()
                tk.Tk.wm_title(popup_box, "Scoreboard")

                def remove_user(dictionary, user, json_file, value, reset_all=False):
                        # This function removes the selected user by remaking the entire list without the selected user
                        # If everything needs to be reset, the reset_all parameter is on
                        if value:
                                json_file.close()
                                with open("user_data.json", "w") as json_file_write:
                                        new_dictionary = {i:dictionary[i] for i in dictionary if i!=user}
                                        json_file_write.seek(0)
                                        new_data = {'users': new_dictionary}
                                        if reset_all:
                                                new_data = {'users': {}}
                                        json.dump(new_data, json_file_write, indent=4)
                                        json_file_write.close()
                                popup_box.destroy()
                                self.score_popup()

                i = 1
                name_title = ttk.Label(popup_box, text="Name", font=LARGE_FONT)
                score_title = ttk.Label(popup_box, text="Score", font=LARGE_FONT)
                correct_title = ttk.Label(popup_box, text="Number Correct", font=LARGE_FONT)
                grade_title = ttk.Label(popup_box, text="Grade", font=LARGE_FONT)
                year_title = ttk.Label(popup_box, text="Year", font=LARGE_FONT)
                sections_title = ttk.Label(popup_box, text="Sections", font=LARGE_FONT)
                name_title.grid(row=0, column=0)
                score_title.grid(row=0, column=1)
                correct_title.grid(row=0, column=2)
                grade_title.grid(row=0, column=3)
                year_title.grid(row=0, column=4)
                sections_title.grid(row=0, column=5)
                with open("user_data.json", "r+") as json_file:
                        data = json.load(json_file)
                        users = {k : v for k, v in sorted(data['users'].items())}
                        reset_button = ttk.Button(popup_box, text="Reset All", command=lambda: remove_user(users, "", json_file, tk.messagebox.askyesno("Confirmation", message="Reset all Users?"), True))
                        reset_button.grid(row=0, column=6)
                        for user in users:
                                # For each user, define their values and show them.
                                user_name = tk.StringVar(popup_box)
                                user_name.set(users[user]['name'])
                                user_score = tk.IntVar(popup_box)
                                user_score.set(users[user]['score'])
                                user_correct = tk.IntVar(popup_box)
                                user_correct.set(users[user]['number_correct'])
                                user_grade = tk.StringVar(popup_box)
                                user_grade.set(users[user]['grade'])
                                user_year = tk.IntVar(popup_box)
                                user_year.set(users[user]['year'])
                                user_sections = tk.StringVar(popup_box)
                                user_sections.set(users[user]['sections'])
                                delete_user = ttk.Button(popup_box, text="Remove Score", command=lambda user=user: remove_user(users, user, json_file, tk.messagebox.askyesno("Confirmation", message="Remove User?")))
                                name_label = ttk.Label(popup_box, text=user_name.get(), font=REGULAR_FONT)
                                name_label.grid(row=i, column=0)
                                score_label = ttk.Label(popup_box, text=user_score.get(), font=REGULAR_FONT)
                                score_label.grid(row=i, column=1)
                                score_label = ttk.Label(popup_box, text=user_correct.get(), font=REGULAR_FONT)
                                score_label.grid(row=i, column=2)
                                grade_label = ttk.Label(popup_box, text=user_grade.get(), font=REGULAR_FONT)
                                grade_label.grid(row=i, column=3)
                                year_label = ttk.Label(popup_box, text=user_year.get(), font=REGULAR_FONT)
                                year_label.grid(row=i, column=4)
                                sections_label = ttk.Label(popup_box, text=user_sections.get(), font=REGULAR_FONT)
                                sections_label.grid(row=i, column=5)
                                delete_user.grid(row=i, column=6)
                                i += 1
                row_column_configure(popup_box, i, 6)
                popup_box.geometry("800x"+str(50*i))
                popup_box.resizable(False, False)
                popup_box.mainloop()

        def generate_quiz(self, *question_lists):
                """This method is the same as the for loop in the __init__, except it passes each question as its own instance
                It takes from a question_list generated from the types of question chosen by the user"""
                self.checkbox_frame = tk.Frame(self, bg='blue')
                self.checkbox_frame.pack(expand=True, side="left", fill='both')
                self.checkbox_questions = {}
                
                length, section_length = len(question_lists[0])*10, 10
                for question in range(length):
                        # Initialize checkboxes
                        self.checkbox_questions[str(question+1)] = tk.StringVar(self, "Not Completed")
                        question_label = ttk.Button(self.checkbox_frame, text="Question " + str(question+1), command=lambda question=question: self.show_frame("QuestionPage"+str(question)))
                        question_label.grid(row=question, column=0)
                        
                        check_label = ttk.Label(self.checkbox_frame, textvariable=self.checkbox_questions[str(question+1)])
                        check_label.grid(row=question, column=1)
                self.done_label = ttk.Label(self.checkbox_frame, text="Please answer all questions to end the quiz.")
                self.done_label.grid(row=length+2, column=0, columnspan=2)
                self.confirm_button = ttk.Button(self.checkbox_frame, text="Confirm", command=lambda: self.end_quiz(), state=tk.DISABLED)
                self.confirm_button.grid(row=length+1, column=0, columnspan=2)
                difficulty, difficulty_before = "easy", ""
                new_list = [{"easy": [], "medium": [], "hard": []}, {"easy": [], "medium": [], "hard": []}, {"easy": [], "medium": [], "hard": []}]
                modifier = 1
                # The question_i variable is reset when there is a change in difficulty
                question_i = 0
                for question in range(length):
                        difficulty_before = difficulty
                        """The 'i' variable is used to determine which question list the question is taken from.
                        When sections are off, it's random. When they are on, it is in order."""
                        if self.section_check.get() == False:
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

                        frame = QuestionPage(self.container, self, question, question_i, score_modifier, length, new_list[i_2][difficulty], self.checkbox_questions[str(question+1)])
                        self.frames["QuestionPage" + str(question)] = frame
                        frame.grid(row=0, column=0, sticky="nsew")

                        question_i += 1

        def start_quiz(self):
                section_list = self.check_section()
                if section_list == []:
                        tk.messagebox.showwarning("Warning", message="Please select a question type.")
                else:
                        self.generate_quiz(section_list)
                        self.show_frame("QuestionPage0")

        def end_quiz(self):
                self.check_score()
                self.show_answers()
                self.show_frame(EndPage)

        def check_answer(self, answer, correct_answer, score_modifier, page, end_number, checkbox_item):
                """Checks if the answer selected by a button is correct"""
                self.users[self.current_user.get()].question = page.number
                page.chosen_answer = answer
                checkbox_item.set("Skipped")
                if page.chosen_answer != "0":
                        checkbox_item.set("Answered")
                if answer == correct_answer:
                        page.score = 1 * score_modifier
                        page.correct += 1
                else:
                        page.score = 0
                        page.correct = 0
                if all(i.get() == "Answered" for i in self.checkbox_questions.values()):
                        self.confirm_button.config(state=tk.NORMAL)
                        self.done_label.config(text="The quiz can be ended.")
                else:
                        self.confirm_button.config(state=tk.DISABLED)
                        self.done_label.config(text="Please answer all questions to end the quiz.")

        def check_score(self):
                current_score = 0
                number_correct = 0
                for i in self.frames:
                        if isinstance(i, str):
                                current_score += self.frames[i].score
                                number_correct += self.frames[i].correct
                self.users[self.current_user.get()].score = current_score
                self.users[self.current_user.get()].number_correct = number_correct
                self.number_correct.set(number_correct)
                self.score.set(current_score)

                if self.users[self.current_user.get()].score < (0.2 * len(self.users[self.current_user.get()].sections) * 20) or self.users[self.current_user.get()].score == 0:
                        self.grade.set("Not Achieved")
                elif self.users[self.current_user.get()].score < (0.4 * len(self.users[self.current_user.get()].sections) * 20):
                        self.grade.set("Achieved")
                elif self.users[self.current_user.get()].score < (0.7 * len(self.users[self.current_user.get()].sections) * 20):
                        self.grade.set("Merit")
                else:
                        self.grade.set("Excellence")
                self.users[self.current_user.get()].grade = self.grade.get()
                self.checkbox_frame.pack_forget()
                self.save_user()

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
                self.users[self.current_user.get()].sections = [section for section in [complex_numbers, differentiation, integration] if isinstance(section, str)]
                return sections

        def show_answers(self):
                i = len(self.frames) - 4
                chosen_questions = []
                while i > -1:
                        question_page = self.frames["QuestionPage" + str(i)]
                        question = question_page.question_list[question_page.question_i]['question']
                        correct_answer = question_page.question_list[question_page.question_i]["answers"][question_page.question_list[question_page.question_i]["correct_answer"]]
                        chosen_answer = question_page.question_list[question_page.question_i]["answers"][question_page.chosen_answer]
                        chosen_questions.append([question,correct_answer,chosen_answer])
                        i = i - 1
                return chosen_questions

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

        def save_user(self):
                if self.current_user.get() != "" and self.user_saved == False:
                        self.users[self.current_user.get()].user_write()
                        #self.load_user_set(self.current_user.get())
                        self.user_saved = True
            

        def new_user(self, value):
                if self.restart(value):
                        self.save_user()
                        self.user_saved = False
                        self.current_user.set("")
                        self.show_frame(StartingPage)
        
        def quit(self, value):
                if value:
                        self.destroy()

class StartingPage(tk.Frame):
        """This page contains a next button to the selection page"""
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                self.config(bg=THEMING[controller.theme_number.get()]["COLOR_PRIMARY"])
                row_column_configure(self, 3, 5)
                top_frame = tk.Frame(self, bg=THEMING[controller.theme_number.get()]["COLOR_PRIMARY"])
                row_column_configure(top_frame, 1, 1)
                top_frame.pack(fill="both", expand=True, padx=5, pady=10)
                label = ttk.Label(top_frame, text="Welcome to NCEA Level 3 Calculus External Revision Quiz.", font=LARGE_FONT)
                label.grid(row=0, column=0, columnspan=5)

                bottom_frame = tk.Frame(self)
                bottom_frame.pack(fill="both", expand=True)
                name = tk.StringVar(controller)
                year_list = (0, 13, 12, 11, 10, 9)
                year_dropdown = ttk.OptionMenu(bottom_frame, controller.year, *year_list)
                year_dropdown.grid(row=1, column=4)
                name_title = ttk.Label(bottom_frame, text="Name:", font=REGULAR_FONT)
                name_title.grid(row=1, column=0)
                year_title = ttk.Label(bottom_frame, text="Year:", font=REGULAR_FONT)
                year_title.grid(row=1, column=3)
                name_validation = self.register(check_name_entry)
                name_entry = ttk.Entry(bottom_frame, validate="all", validatecommand=(name_validation, "%P"), background="grey", textvariable=name, font=REGULAR_FONT)
                name_entry.grid(row=1, column=1)

                def save_name(saved_name):
                        if saved_name.get() == "":
                                tk.messagebox.showwarning("Warning", message="Please give a name.")
                        else:
                                controller.current_user.set(saved_name.get())
                                controller.users[saved_name.get()] = UserData(saved_name.get())
                                controller.users[saved_name.get()].year = controller.year.get()
                                saved_name.set("")
                                controller.show_frame(SelectionPage)

                next_button = ttk.Button(bottom_frame, text="Next", command=lambda: save_name(name))
                next_button.grid(row=2, column=4)
                button = ttk.Button(bottom_frame, text="Quit", command=lambda: controller.quit(tk.messagebox.askyesno("Confirmation", message="Quit?")))
                button.grid(row=2, column=0)

class SelectionPage(tk.Frame):
        """This page contains check buttons to toggle which type of question will be asked in the quiz
        It toggles if the question_list will include complex, differentiation and/or integration, and whether it's separated by section"""
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                self.config(bg=THEMING[controller.theme_number.get()]["COLOR_PRIMARY"])
                row_column_configure(self, 8, 4)
                label = ttk.Label(self, text="Select which sections you want to test", font=LARGE_FONT)
                label.grid(row=0, column=1, columnspan=2, sticky="nsew")

                complex_check = ttk.Checkbutton(self, text="Test Complex Numbers?", variable=controller.complex_test)
                differentiation_check = ttk.Checkbutton(self, text="Test Differentiation?", variable=controller.differentiation_test)
                integration_check = ttk.Checkbutton(self, text="Test Integration?", variable=controller.integration_test)
                complex_check.grid(row=1, rowspan=2, column=1, sticky="nsew")
                differentiation_check.grid(row=3, rowspan=2, column=1, sticky="nsew")
                integration_check.grid(row=5, rowspan=2, column=1, sticky="nsew")
                section_check_on = ttk.Radiobutton(self, text="Sections On", variable=controller.section_check, value=False)
                section_check_off = ttk.Radiobutton(self, text="Sections Off", variable=controller.section_check, value=True)
                section_check_on.grid(row=2, column=2, sticky="nsew")
                section_check_off.grid(row=4, column=2, sticky="nsew")

                button = ttk.Button(self, text="Start Quiz", command=lambda: controller.start_quiz())
                button.grid(row=7, column=1, columnspan=2, sticky="ew")

class QuestionPage(tk.Frame):
        """This is the general frame for questions, which will change depending on the number and type of question asked
        There will always be multiple instances of this object
        For each instance of a QuestionPage, the number increments by one, which takes the next question in the question_list
        This question_list is generated based on the checkboxes the user checked before"""
        def __init__(self, parent, controller, number, question_i, score_modifier, end_number, question_list, checkbox_item):
                tk.Frame.__init__(self, parent)
                self.config(bg=THEMING[controller.theme_number.get()]["COLOR_PRIMARY"])
                self.number = number
                self.question_list = question_list
                self.question_i = question_i
                row_column_configure(self, 6, 4)
                text = "Question " + str(number+1) + "/" + str(end_number)
                label = ttk.Label(self, text=text, font=LARGE_FONT)
                label.grid(row=0, column=0, columnspan=4)
                type_label = ttk.Label(self, text=self.question_list[question_i]["type"], font=REGULAR_FONT)
                type_label.grid(row=0, rowspan=2, column=0)
                user_label = ttk.Label(self, text="User: " + controller.current_user.get(), font=REGULAR_FONT)
                user_label.grid(row=0, rowspan=2, column=3)

                self.score = 0
                self.correct = 0
                self.chosen_answer = ""

                """Essentially, each question is index 0 of the shuffled list. At the end, this index is deleted, so that old index 1 becomes index 0.
                This way, no question is repeated."""
                question = ttk.Label(self, text=self.question_list[question_i]['question'], font=REGULAR_FONT)
                question.grid(row=1, column=0, columnspan=4)

                if number == end_number - 1:
                        next_page = "QuestionPage" + str(number)
                else:
                        next_page = "QuestionPage" + str(number+1)

                """The for loop here generates buttons of each answer. Each button has the command to check if it was right, and then move to the next frame.
                I've put this into a for loop to make it easier to program"""
                answer = {}
                i, j = 0.6, 0
                answers_frame = tk.Frame(self, background=THEMING[controller.theme_number.get()]["COLOR_PRIMARY"])
                for letter in ['a','b','c','d']:
                        answer[letter] = ttk.Button(answers_frame, text=self.question_list[question_i]['answers'][letter], command=lambda letter=letter, correct_letter=self.question_list[question_i]["correct_answer"], next_page=next_page: combine_funcs(controller.check_answer(letter, correct_letter, score_modifier, self, end_number, checkbox_item), controller.show_frame(next_page)))
                        answer[letter].grid(row=round(i), column=[1,2,1,2][j], pady=2, padx=2)
                        i += 0.5
                        j += 1
                answers_frame.grid(row=2, column=1, columnspan=2)

                back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("QuestionPage" + str(number-1) if number != 0 else "QuestionPage" + str(number)))
                back_button.grid(row=3, column=1)
                skip_button = ttk.Button(self, text="Skip", command=lambda next_page=next_page: combine_funcs(controller.check_answer('0', 1, score_modifier, self, end_number, checkbox_item), controller.show_frame(next_page)))
                skip_button.grid(row=3, column=2)
                popup_button = ttk.Button(self, text="Restart", command=lambda: controller.restart(tk.messagebox.askyesno("Confirmation", message="Restart?")))
                popup_button.grid(row=5, column=0, sticky="e")
                quit_button = ttk.Button(self, text="Quit", command=lambda: controller.quit(tk.messagebox.askyesno("Confirmation", message="Quit?")))
                quit_button.grid(row=5, column=3, sticky="w")

class EndPage(tk.Frame):
        """"""
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                self.config(bg=THEMING[controller.theme_number.get()]["COLOR_PRIMARY"])
                row_column_configure(self, 5, 5)

                user_title = ttk.Label(self, text="User: ", font=LARGE_FONT)
                user_title.grid(row=0, column=1)
                name_title = ttk.Label(self, textvariable=controller.current_user, font=LARGE_FONT)
                name_title.grid(row=0, column=2)
                score_title = ttk.Label(self, text="End score: ", font=LARGE_FONT)
                score_title.grid(pady=10,padx=10, row=1, column=1)
                final_score = ttk.Label(self, textvariable=controller.score, font=LARGE_FONT)
                final_score.grid(row=1, column=2)
                number_correct_title = ttk.Label(self, text="Number Correct: ", font=LARGE_FONT)
                number_correct_title.grid(row=2, column=1)
                number_correct = ttk.Label(self, textvariable=controller.number_correct, font=LARGE_FONT)
                number_correct.grid(row=2, column=2)
                grade = ttk.Label(self, textvariable=controller.grade, font=LARGE_FONT)
                grade.grid(row=3, column=1, columnspan=2)
                show_answers_button = ttk.Button(self, text="Show Answers", command=lambda: self.show_questions(controller))
                show_answers_button.grid(row=4, column=1, columnspan=2)
                new_quiz_button = ttk.Button(self, text="Start Again?", command=lambda: controller.new_user(tk.messagebox.askyesno("Confirmation", message="Start a new quiz?")))
                new_quiz_button.grid(row=5, column=1)
                quit_button = ttk.Button(self, text="Quit", command=lambda: controller.quit(tk.messagebox.askyesno("Confirmation", message="Quit?")))
                quit_button.grid(row=5, column=2)

        def show_questions(self, cont):
                answers_box = tk.Tk()
                tk.Tk.wm_title(answers_box, "Answers")
                scrollbar = tk.Scrollbar(answers_box)
                scrollbar.pack(side="right", fill="y")
                list_box = tk.Listbox(answers_box, yscrollcommand=scrollbar.set, font=REGULAR_FONT)
                list_box.pack(expand=True, fill="both")
                question_list = cont.show_answers()
                j=0
                for i in question_list:
                        if i[1] == i[2]:
                                answer_is = "CORRECT"
                                colour = CORRECT_COLOUR
                        else:
                                answer_is = "INCORRECT"
                                colour = INCORRECT_COLOUR
                        list_box.insert(0, "")
                        list_box.insert(0, "Correct answer: " + i[1] + ", Your answer: " + i[2])
                        list_box.itemconfig(0, {'bg': colour})
                        list_box.insert(0, "Question: " + i[0] + " " + answer_is)
                        list_box.itemconfig(0, {'bg': colour})
                        j+=1
                scrollbar.config(command=list_box.yview)
                answers_box.geometry("600x200")
                answers_box.resizable(False, False)
                answers_box.mainloop()

quiz = RootFrame()
quiz.mainloop()
