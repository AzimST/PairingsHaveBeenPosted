'''
Created on Jan 27, 2018

@author: Yishan McNabb
'''
class Player:
    def __init__(self,name):
        self.name = name
        self.wins = []
        self.losses = []
        self.ties = []
        self.tiebreaker = ''

    def to_dict(self):
        return {
                "name": self.name, 
                "wins": self.wins, 
                "losses": self.losses, 
                "ties": self.ties, 
                "tiebreaker": self.tiebreaker
                }
    
    
    def __str__(self):
        return "Player Name: " + str(self.name) + " Player Wins: " + str(self.get_wins_name()) + " Player Losses: " + str(self.get_losses_name()) + " Player Ties: " + str(self.ties)
	
    def get_losses_name(self):
        loss_str = ""
        try:
            for i in self.losses:
                loss_str +=f"{i.name},"
            # loss_str = ",".join(self.losses)
        except:
            loss_str = "No wins"
        return loss_str
    
    def get_wins_name(self):
        wins_str = ""
        try:
            for i in self.wins:
                wins_str +=f"{i.name}," 
            # wins_str = ",".join(self.wins)
        except:
            wins_str = "No wins"
        return wins_str
        # wins_str = ",".join(self.wins)
        # return wins_str


    def get_number(self):
        return self.num_wins()
    
    def get_points(self):
        return len(self.wins)*3 + len(self.ties)
    
    def num_wins(self):
        return len(self.wins)
    
    def num_losses(self):
        return len(self.losses)
    
    def num_ties(self):
        return len(self.ties)
    
    def add_win(self, opponent):
        self.wins.append(opponent)

    def add_loss(self, opponent):
        self.losses.append(opponent)

    def add_tie(self, opponent):
        self.ties.append(opponent)

    
    def get_opponents(self):
        played = []
        for player in self.wins:
            if player != "BYE":
                played.append(player)
        
        for player in self.losses:
            played.append(player)
        
        for player in self.ties:
            played.append(player)
    
        return played
