import pandas as pd

class Sumula():
    def __init__(self):
        self.homeName = ''
        self.awayName = ''
        self.homeScore = 0
        self.awayScore = 0
        self.homePlayers = []
        self.awayPlayers = []
        self.homeRepublic = []
        self.awayRepublic = []
        
    def excel_to_object(self, excel, logText):
        self.homeName = excel.iloc[1,1]
        self.awayName = excel.iloc[22,1]
        scoreText = excel.iloc[0,1]
        self.homeScore = int(scoreText.split('x')[0])
        self.awayScore = int(scoreText.split('x')[1])
        self.homeRepublic = [0, self.homeName, self.homeScore]
        self.awayRepublic = [0, self.awayName, self.awayScore]
        
        homePlayers = []
        for i in range(2, 22):
            if not pd.isna(excel.iloc[i, 3]):
                homePlayers.append([0, excel.iloc[i,1], excel.iloc[i,0]])
        self.homePlayers = homePlayers
        logText.insert('end', 'Republica: ' + self.homeName)
        logText.yview('end')
        for i in range(0, len(homePlayers)):
            logText.insert('end', 'Jogador: ' + str(homePlayers[i]))
            logText.yview('end')
            
        awayPlayers = []
        for i in range(23, 43):
            if not pd.isna(excel.iloc[i, 3]):
                awayPlayers.append([0, excel.iloc[i,1], excel.iloc[i,0]])
        self.awayPlayers = awayPlayers
        logText.insert('end', 'Republica: ' + self.awayName)
        logText.yview('end')
        for i in range(0, len(awayPlayers)):
            logText.insert('end', 'Jogador: ' + str(awayPlayers[i]))
            logText.yview('end')