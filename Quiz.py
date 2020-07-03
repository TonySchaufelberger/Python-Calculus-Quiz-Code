import tkinter as tk

class section():
        """"""
        
        def __init__ (self, questions, question_type):
                self.questions = questions
                self.question_type = question_type

class rootFrame(tk.Frame):
        """"""
        
        def __init__ (self, parent, *args, **kwargs):
                tk.Frame.__init__(self, parent, *args, **kwargs)
                self.parent = parent
                self.introFrame = introFrame(self)
                self.questionFrame = questionFrame(self)
                
        def grid_frame (frame):
                pass
                
        def storeInformation ():
                pass
        
class introFrame(tk.Frame):
        """"""
        
        def __init__ (self, parent, *args, **kwargs):
                tk.Frame.__init__(self, parent, *args, **kwargs)
                pass
                
class questionFrame(tk.Frame):
        """"""
        
        def __init__ (self, *question_list):
                self.question_list = question_list
                pass
                
        def grid_multiple ():
                for i in questions:
                        self.grid_frame(i);

root = tk.Tk()
rootFrame(root).pack(side="top", fill="both", expand=True)
root.mainloop()
