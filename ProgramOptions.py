import tkinter as ttk
import httplib2
import urllib
import json
import os

class ProgramOptions():
    def __init__(self):
        try:
            file = open('config.json')
            # if file has information, read it
            if os.stat('config.json').st_size > 0:
                config = json.load(file)
            else:
                config = {}
            if 'uploadScores' not in config:
                config['uploadScores'] = True
            if 'uploadGames' not in config:
                config['uploadGames'] = True
            if 'loginEmail' not in config:
                config['loginEmail'] = ''
            if 'bearerToken' not in config:
                config['bearerToken'] = ''
            if 'serie' not in config:
                config['serie'] = ''
            self.uploadScores = config['uploadScores']
            self.uploadGames = config['uploadGames']
            self.loginEmail = config['loginEmail']
            self.loginPassword = ''
            self.bearerToken = config['bearerToken']
            self.serie = config['serie']
        except FileNotFoundError:
            # Create a new config file
            file = open('config.json', 'w')
            self.uploadScores = True
            self.uploadGames = True
            self.loginEmail = ''
            self.bearerToken = ''
            self.serie = ''
        
    def loginRequest(self, window):
        url = "https://www.interrep.com.br/api/"
        http = httplib2.Http()
        formData = {'email': self.loginEmail, 'password': self.loginPassword}
        content = http.request(url + 'session/login',
                               method='POST',
                               headers={'Content-Type': 'application/x-www-form-urlencoded'},
                               body=urllib.parse.urlencode(formData))[1]
        response = json.loads(content.decode('utf-8'))
        print(response, self.loginEmail, self.loginPassword)
        if 'token' in response:
            self.bearerToken = response['token']
            ttk.Variable(window, name='LoginText').set('Login:' + self.loginEmail)
            self.save_to_file()
            
            return True
        
        ttk.Variable(window, name='LoginErrorText').set(response['error'])
        return False
    
    def save_to_file(self):
        file = open('config.json', 'w')
        config = {'uploadScores': self.uploadScores,
                  'uploadGames': self.uploadGames,
                  'loginEmail': self.loginEmail,
                  'bearerToken': self.bearerToken,
                  'serie': self.serie}
        serializedConfig = json.dumps(config)
        file.write(serializedConfig)
            
