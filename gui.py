import tkinter as ttk
import httplib2
import urllib
import json
from tkinter import filedialog
import pandas as pd
from ProgramOptions import ProgramOptions
from ProgramVariables import ProgramVariables
from Sumula import Sumula
from handlers import *

def show_login_screen(window, programOptions):
    loginFrame = ttk.Frame(window, padx=10, pady=10)
    #pack loginFrame on top of window
    loginFrame.pack(fill='y', expand=True)
    loginButton = ttk.Button(
        loginFrame,
        text = 'Fazer Login',
        command=lambda: handle_login_button(programOptions, window, loginFrame))

    emailEntry = ttk.Entry(
        loginFrame,
        textvariable= ttk.Variable(window, name="loginEmail"))

    passwordEntry = ttk.Entry(
        loginFrame,
        textvariable= ttk.Variable(window, name="loginPassword"))

    ttk.Label(loginFrame, text="Login").grid(row=0, column=0, columnspan= 2)
    ttk.Label(loginFrame, text="E-mail:").grid(row=1, column=0)
    ttk.Label(loginFrame, text="Senha:").grid(row=2, column=0)

    emailEntry.grid(row=1, column=1)
    passwordEntry.grid(row=2, column=1)
    loginButton.grid(row=3, column=0, columnspan=2)

    ttk.Label(loginFrame,textvariable=ttk.Variable(window, name='loginErrorText')).grid(row=4, column=0, columnspan=2)
    
    loginFrame.wait_window()
    
def show_options_frame(window, serieOption, uploadPoints, uploadGames):
    optionsFrame = ttk.Frame(window, padx=10, pady=10)
    optionsFrame.pack(fill='y', expand=True)

    ttk.Label(optionsFrame, text='Opções').grid(row=0, column=0, columnspan=2, padx=10, pady=2)
    ttk.Label(optionsFrame, text='Escolha a série:').grid(row=1, column=0, padx=10, pady=2)
    ttk.Label(optionsFrame, text='Fazer upload dos:').grid(row=1, column=1, padx=10, pady=2)

    ttk.Radiobutton(
        optionsFrame, 
        text='Serie A', 
        variable= serieOption,
        value='seriea').grid(row=2, column=0, sticky='w', padx=10, pady=2)
    ttk.Radiobutton(
        optionsFrame, 
        text='Serie B', 
        variable= serieOption,
        value='serieb').grid(row=3, column=0, sticky='w', padx=10, pady=2)
    ttk.Radiobutton(
        optionsFrame, 
        text='Feminino', 
        variable= serieOption,
        value='feminino').grid(row=4, column=0, sticky='w', padx=10, pady=2)

    ttk.Checkbutton(
        optionsFrame,
        text='Pontuações',
        variable= uploadPoints
    ).grid(row=2, column=1, sticky='w', padx=10, pady=2)

    ttk.Checkbutton(
        optionsFrame,
        text='Jogos',
        variable= uploadGames
    ).grid(row=3, column=1, sticky='w', padx=10, pady=2)
    
def show_files_frame(window, programVariables):
    filesFrame = ttk.Frame(window)
    filesFrame.pack(fill='y', expand=True)

    ttk.Label(filesFrame, text='Escolher Súmulas').grid(row=0, column=0)
    ttk.Button(
        filesFrame,
        text='Selecionar Arquivos',
        command=lambda: handle_file_search(programVariables, window)).grid(row=1, column=0)
    ttk.Message(filesFrame, textvariable= ttk.Variable(window, name='sumulaNameText')).grid(row=2, column= 0)

def show_log_frame(window):
    logFrame = ttk.Frame(window)
    logFrame.pack(side='bottom', fill='both', expand=True)

    ttk.Label(logFrame, text='Log:').pack()
    scrollbarY = ttk.Scrollbar(logFrame, orient='vertical')
    scrollbarX = ttk.Scrollbar(logFrame, orient='horizontal')
    scrollbarY.pack(side='right', fill='y')
    scrollbarX.pack(side='bottom', fill='x')
    logText = ttk.Listbox(logFrame, yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
    logText.pack(side = 'left', fill='both', expand=True, padx=5, pady=5)
    scrollbarY.config(command=logText.yview)
    scrollbarX.config(command=logText.xview)
    return logText

def show_match_player_screen(matchPlayerFrame, programVariables, logText, player, errorRepublic):
    ttk.Label(matchPlayerFrame, text='Escolha o jogador da partida').grid(row=0, column=0, columnspan=2)
    ttk.Label(matchPlayerFrame, text=f'{player[0]} - {player[1]}').grid(row=1, column=0)
    
    playersFrame = ttk.Frame(matchPlayerFrame)
    playersFrame.grid(row=1, column=1)
    playerId = ttk.IntVar(matchPlayerFrame, name='playerId')   
    row = 0
    for replublicPlayer in errorRepublic['players']:
        ttk.Radiobutton(
            playersFrame,
            text=replublicPlayer['name'],
            variable=playerId,
            value=replublicPlayer['id']).grid(row=row, column=0, sticky='w')
        row += 1
    ttk.Button(matchPlayerFrame, text='Confirmar', command=lambda: handle_match_player_button(programVariables, logText, playerId, player, matchPlayerFrame)).grid(row=row, column=0, columnspan=2)