import tkinter as ttk
from tkinter import filedialog
from tkinter import messagebox
import httplib2
import json
import urllib
import pandas as pd
from Sumula import Sumula
import gui

def handle_login_button(programOptions, window, topLevelLogin):
    programOptions.loginEmail = ttk.Variable(window, name='loginEmail').get()
    programOptions.loginPassword = ttk.Variable(window, name='loginPassword').get()
    if programOptions.loginRequest(window):
        topLevelLogin.destroy()

def handle_file_search(programVariables, window):
    programVariables.sumulasList = filedialog.askopenfilenames(defaultextension=".xlsm", filetypes=[("Excel files", "*.xlsm")], title="Selecione a sumula", initialdir="~/Downloads")
    sumulaListText = ''
    for file in programVariables.sumulasList:
        filename = file.split('/')[-1]
        sumulaListText += filename + '\n'
    ttk.Variable(window, name='sumulaNameText').set(sumulaListText)
    
def handle_upload(programOptions, programVariables, window, logText, uploadPoints, uploadGames, serieOption):
    DRY = False
    if programOptions.bearerToken == "":
        logText.insert('end', 'Realize o login primeiro')
        logText.yview('end')
        return
    update_variables(programOptions, window, uploadPoints, uploadGames, serieOption)
    logText.insert('end', 'Inserindo em: ' + programOptions.serie)
    logText.insert('end', 'Upload de pontos: ' + str(programOptions.uploadScores))
    logText.insert('end', 'Upload de jogos: ' + str(programOptions.uploadGames))
    logText.yview('end')
    programOptions.save_to_file()
    
    scan_files(programVariables, logText)
    
    error = get_all_republics(programOptions, programVariables, logText)
    if(error):
        logText.insert('end', 'Erro ao dar fetch das republicas')
        logText.yview('end')
        return
    error = match_republics(programVariables, logText)
    if(error):
        logText.insert('end', 'Erro ao encontrar republicas')
        logText.yview('end')
        return
    logText.insert('end', 'Republicas encontradas')
    logText.yview('end')
        
    if(programOptions.uploadScores):
        logText.insert('end', 'Encontrando Jogadores')
        logText.yview('end')
        error, errorPlayers = match_players(programVariables, logText)
        if(error):
            logText.insert('end', 'Erro ao encontrar jogadores')
            logText.yview('end')
            res = messagebox.askyesno('Erro', 'Erro ao encontrar jogadores, deseja encontrar manualmente?')
            if res:
                matchPlayerWindow = ttk.Toplevel(window)
                for player in errorPlayers:
                    errorRepublic = None
                    for republic in programVariables.allRepublicList:
                        if republic['name'] == player[1]:
                            errorRepublic = republic
                            break
                    if errorRepublic == None:
                        logText.insert('end', f'Erro ao encontrar república: {player[1]}, do jogador {player[0]}')
                        continue
                    matchPlayerFrame = ttk.Frame(matchPlayerWindow)
                    matchPlayerFrame.pack(fill='both', expand=True)
                    gui.show_match_player_screen(matchPlayerFrame, programVariables, logText, player, errorRepublic)
                    matchPlayerFrame.wait_window()
                matchPlayerWindow.destroy()
            else:
                logText.insert('end', 'Cancelando upload')
                return
        logText.insert('end', 'Jogadores encontrados')
        logText.yview('end')
        
    logText.insert('end', 'Inserindo sumulas')
    logText.yview('end')
    if(DRY == False):
        if(programOptions.uploadScores):
            error, errorPlayers = upload_points(programOptions, programVariables, logText)
            if(error):
                logText.insert('end', 'Erro ao inserir pontos')
                logText.insert('end', 'Jogadores com erro:')
                logText.yview('end')
                for player in errorPlayers:
                    logText.insert('end', player)
                    logText.yview('end')
                return
        if(programOptions.uploadGames):
            error, errorRepublics = upload_games(programOptions, programVariables, logText)
            if(error):
                logText.insert('end', 'Erro ao inserir jogos')
                logText.insert('end', 'Republicas com erro:')
                logText.yview('end')
                for republic in errorRepublics:
                    logText.insert('end', republic)
                    logText.yview('end')
                return
    logText.insert('end', 'Sumulas inseridas com sucesso')
    logText.yview('end')
    
def update_variables(programOptions, window, uploadPoints, uploadGames, serieOption):
    programOptions.uploadScores = True if uploadPoints.get() == 1 else False
    programOptions.uploadGames = True if uploadGames.get() == 1 else False
    programOptions.serie = serieOption.get()
    
def get_all_players(programOptions, programVariables, logText):
    url = "https://www.interrep.com.br/api/"
    http = httplib2.Http()
    content = http.request(url + programOptions.serie + '/players/active',
                           method='GET',
                           headers={'Content-Type': 'application/x-www-form-urlencoded',
                                        'Authorization': 'Bearer ' + programOptions.bearerToken})[1]
    response = json.loads(content.decode('utf-8'))
    logText.insert('end', 'Quant. de jogadores: ' + str(len(response)))
    logText.yview('end')
    programVariables.allPlayerList = response
    
def scan_files(programVariables, logText):
    programVariables.sumulaObjectsList = []
    for file in programVariables.sumulasList:
        logText.insert('end', 'Lendo arquivo: ' + file.split('/')[-1])
        logText.yview('end')
        excel = pd.read_excel(file, sheet_name='Planilha1')
        sumulaObject = Sumula()
        sumulaObject.excel_to_object(excel, logText)
        programVariables.sumulaObjectsList.append(sumulaObject)
        
def match_players(programVariables, logText):
    error = False
    errorPlayers = []
    for sumula in programVariables.sumulaObjectsList:
        #Search in home republic
        homeRepublic = None
        for republic in programVariables.allRepublicList:
            if sumula.homeName == republic['name']:
                homeRepublic = republic
        if homeRepublic == None:
            error = True
            return error, errorPlayers
        for programPlayer in sumula.homePlayers:
            for sitePlayer in homeRepublic['players']:
                if sitePlayer['name'].upper() in programPlayer[1].upper():
                    programPlayer[0] = sitePlayer['id']
        
        #Search in away republic
        awayRepublic = None
        for republic in programVariables.allRepublicList:
            if sumula.awayName == republic['name']:
                awayRepublic = republic
        if awayRepublic == None:
            error = True
            return error, errorPlayers
        for programPlayer in sumula.awayPlayers:
            for sitePlayer in awayRepublic['players']:
                if sitePlayer['name'].upper() in programPlayer[1].upper():
                    programPlayer[0] = sitePlayer['id']
        
        #Error handling
        for player in sumula.homePlayers:
            if player[0] == 0:
                logText.insert('end', 'Jogador nao encontrado: ' + player[1] + ' - ' + sumula.homeName)
                logText.yview('end')
                error = True
                errorPlayers.append([player[1], sumula.homeName])
        
        #Error handling
        for player in sumula.awayPlayers:
            if player[0] == 0:
                logText.insert('end', 'Jogador nao encontrado: ' + player[1] + ' - ' + sumula.awayName)
                logText.yview('end')
                error = True
                errorPlayers.append([player[1], sumula.awayName])
                
    return error, errorPlayers

def upload_points(programOptions, programVariables, logText):
    error = False
    errorPlayers = []
    url = "https://www.interrep.com.br/api/"
    http = httplib2.Http()
    for sumula in programVariables.sumulaObjectsList:
        for player in sumula.homePlayers:
            body = {'players': player[0], 'points': player[2]}
            content = http.request(url + programOptions.serie + '/players/scores',
                                   method='PUT',
                                   headers={'Content-Type': 'application/x-www-form-urlencoded',
                                            'Authorization': 'Bearer ' + programOptions.bearerToken},
                                      body=urllib.parse.urlencode(body))[1]
            response = json.loads(content.decode('utf-8'))
            # if response does not contain key 'id' then there was an error
            if 'name' not in response:
                logText.insert('end', response)
                logText.yview('end')
                error = True
                errorPlayers.append([player[1], sumula.homeName])
            
        for player in sumula.awayPlayers:
            body = {'players': player[0], 'points': player[2]}
            content = http.request(url + programOptions.serie + '/players/scores',
                                   method='PUT',
                                   headers={'Content-Type': 'application/x-www-form-urlencoded',
                                            'Authorization': 'Bearer ' + programOptions.bearerToken},
                                      body=urllib.parse.urlencode(body))[1]
            response = json.loads(content.decode('utf-8'))
            # if response does not contain key 'id' then there was an error
            if 'id' not in response:
                logText.insert('end', response)
                logText.yview('end')
                error = True
                errorPlayers.append([player[1], sumula.awayName])
                
    return error, errorPlayers
        
def get_all_republics(programOptions, programVariables, logText):
    error = False
    url = "https://www.interrep.com.br/api/"
    http = httplib2.Http()
    content = http.request(url + programOptions.serie + '/republics/',
                           method='GET',
                           headers={'Content-Type': 'application/x-www-form-urlencoded',
                                    'Authorization': 'Bearer ' + programOptions.bearerToken})[1]
    if content == b'' or content == None:
        logText.insert('end', 'Erro ao buscar republicas')
        logText.yview('end')
        error = True
        return error
    response = json.loads(content.decode('utf-8'))
    logText.insert('end', 'Quant. de republicas: ' + str(len(response)))
    logText.yview('end')
    programVariables.allRepublicList = response
    if(len(response) == 0):
        logText.insert('end', 'Nenhuma republica encontrada')
        logText.yview('end')
        error = True
    return error
    
def match_republics(programVariables, logText):
    error = False
    for sumula in programVariables.sumulaObjectsList:
        for republic in programVariables.allRepublicList:
            if republic['name'].upper() in sumula.homeName.upper() or sumula.homeName.upper() in republic['name'].upper():
                sumula.homeRepublic[0] = republic['id']
            if republic['name'].upper() in sumula.awayName.upper() or sumula.awayName.upper() in republic['name'].upper():
                sumula.awayRepublic[0] = republic['id']
                
        if sumula.homeRepublic[0] == 0:
            logText.insert('end', 'Republica nao encontrada: ' + sumula.homeName)
            logText.yview('end')
            error = True
        if sumula.awayRepublic[0] == 0:
            logText.insert('end', 'Republica nao encontrada: ' + sumula.awayName)
            logText.yview('end')
            error = True
    
    return error

def upload_games(programOptions, programVariables, logText):
    error = False
    errorGames = []
    url = "https://www.interrep.com.br/api/"
    http = httplib2.Http()
    for sumula in programVariables.sumulaObjectsList:
        errorSumula = False
        body = {'republic_home_id': sumula.homeRepublic[0], 'republic_away_id': sumula.awayRepublic[0], 'time': '00:00', 'place': 'Dr Soccer'}
        content = http.request(url + programOptions.serie + '/games/',
                               method='POST',
                               headers={'Content-Type': 'application/x-www-form-urlencoded',
                                        'Authorization': 'Bearer ' + programOptions.bearerToken},
                               body=urllib.parse.urlencode(body))[1]
        response = json.loads(content.decode('utf-8'))
        if 'id' not in response:
            logText.insert('end', response)
            logText.yview('end')
            error = True
            errorSumula = True
            errorGames.append([sumula.homeName, sumula.awayName])
        if not errorSumula:
            # Create score
            body = {'score_home': sumula.homeScore, 'score_away': sumula.awayScore}
            content = http.request(url + programOptions.serie + '/games/' + str(response['id']),
                                   method='PUT',
                                   headers={'Content-Type': 'application/x-www-form-urlencoded',
                                            'Authorization': 'Bearer ' + programOptions.bearerToken},
                                    body=urllib.parse.urlencode(body))[1]
            response = json.loads(content.decode('utf-8'))
            if 'id' not in response:
                logText.insert('end', response)
                logText.yview('end')
                error = True
                errorGames.append([sumula.homeName, sumula.awayName])
    return error, errorGames

def handle_match_player_button(programVariables, logText, playerId, player, matchPlayerFrame):
    playerId = playerId.get()
    if playerId == '':
        logText.insert('end', 'Selecione um jogador')
        logText.yview('end')
        return
    for sumula in programVariables.sumulaObjectsList:
        for republicPlayer in sumula.homePlayers:
            if republicPlayer[0] == 0:
                if republicPlayer[1] == player[0]:
                    republicPlayer[0] = int(playerId)
        for republicPlayer in sumula.awayPlayers:
            if republicPlayer[0] == 0:
                if republicPlayer[1] == player[0]:
                    republicPlayer[0] = int(playerId)
    return matchPlayerFrame.destroy()