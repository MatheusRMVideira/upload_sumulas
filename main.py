import tkinter as ttk
from ProgramOptions import ProgramOptions
from ProgramVariables import ProgramVariables
from gui import *


window = ttk.Tk()
window.title('Upload de Sumulas 2023')
window.geometry('800x600')

                        
programOptions = ProgramOptions()
programVariables = ProgramVariables()

if(programOptions.bearerToken == ""):
    show_login_screen(window, programOptions)
    
uploadPoints = ttk.IntVar(window)
if(programOptions.uploadScores):
    uploadPoints.set(1)
else:
    uploadPoints.set(0)
    
uploadGames = ttk.IntVar(window)
if(programOptions.uploadGames):
    uploadGames.set(1)
else:
    uploadGames.set(0)
    
serieOption = ttk.Variable(window)
serieOption.set(programOptions.serie)


show_options_frame(window, serieOption, uploadPoints, uploadGames)

show_files_frame(window, programVariables)

ttk.Button(
        window,
        text='Fazer Upload',
        command=lambda: handle_upload(programOptions, programVariables, window, logText, uploadPoints, uploadGames, serieOption)
    ).pack(fill='x', expand=True)

logText = show_log_frame(window)

if(programOptions.bearerToken != ""):
    logText.insert('end', 'Login Realizado: ' + programOptions.loginEmail)
    logText.insert('end', 'Bearer: ' + programOptions.bearerToken)


window.mainloop()