import prompt
import goody
import file
import random
import Player
import sys

class Tournament:
    def __init__(self):
        self.num_rounds = 0
        self.dropped_players = []
        self.players = []
        self.round_number = 1
        self.pairs = None

    def _check_if_played_before(self, player1, player2):
        for opponent in player1.get_opponents():
            if player2 == opponent:
                return True
        return False

    def _sort_seats(self, seats):
        def sum_points(seat):
            total_points = 0
            try:
                total_points = seat[0].get_points() + seat[1].get_points()
            except AttributeError:
                total_points = seat[0].get_points()
            return total_points
        return sorted(seats, key=lambda x: -sum_points(x))

    def _players_to_seats(self, players):
        seats = []
        for i in range(0, len(players), 2):
            try:
                seats.append([players[i], players[i + 1]])
            except IndexError:
                seats.append([players[i], "BYE"])
        return seats

    def _loss_fn(self, players):
        loss = 0
        seats = self._players_to_seats(players)
        for seat in seats:
            if self._check_if_played_before(seat[0], seat[1]):
                loss += 100000
            try:
                loss += (seat[0].get_points() - seat[1].get_points()) ** 2
            except AttributeError:
                loss += seat[0].get_points() * 10
        return loss

    def _pair_round(self, players):
        min_loss = float('inf')
        players_copy = list(players)
        for i in range(1000):
            random.shuffle(players)
            players = sorted(players, key=lambda x: -x.get_points())
            loss = self._loss_fn(players)
            if loss < min_loss:
                return self._players_to_seats(players)
        
        min_updated = True
        iteration = 0
        while min_updated:
            min_updated = False
            for i in range(len(players) * 100 * (2 ** iteration)):
                random.shuffle(players)
                loss = self._loss_fn(players)
                if loss < min_loss:
                    print('New minimum found at iteration', iteration)
                    min_loss = loss
                    players_copy = list(players)
                    iteration += 1
                    min_updated = True
                    break

        if min_loss == float('inf'):
            assert False, "Error: All players have already played against each other."
        
        print("Minimum loss:", min_loss)
        return self._sort_seats(self._players_to_seats(players_copy))

    def print_pairings(self, seats):
        for i, seat in enumerate(seats):
            try:
                print(
                    "Table", i + 1, seat[0].name,
                    "(", seat[0].get_points(), ") VS.", 
                    seat[1].name, "(", seat[1].get_points(), ")"
                )
            except AttributeError:
                print(
                    "Table", i + 1, seat[0].name,
                    "(", seat[0].get_points(), ") VS. BYE"
                )

    def _get_number_string(self, players):
        return ''.join(str(player.get_number()) for player in players)

    def _check_for_same_pairs(self, seats):
        try:
            for x, y in seats:
                if x in y.get_opponents():
                    return True
            return False
        except AttributeError:
            return False

    def _calculate_num_rounds(self):
        ppl = len(self.players)
        self.num_rounds = 0
        while 2 ** self.num_rounds < ppl:
            self.num_rounds += 1

    def end_of_round_cleanup(self):
        while True:
            dropping = prompt.for_string(
                "Enter the (name of a player) who is dropping or (p)air next round or view (s)tandings or (a)dd a new player",
                is_legal=lambda x: x in [y.name for y in self.players]
                or x == "p"
                or x == "s"
                or x == "a",
                error_message="Invalid player name or not (p), (s), or (a)",
            )
            if dropping == "p":
                break
            elif dropping == "s":
                self.calculate_standings()
                self.print_standings()
            elif dropping == "a":
                new_player = Player.Player(input("Enter the name of the new player: "))
                
                num_byes = prompt.for_int("\
                Enter the number of byes this player has (if any). \
                For example if this player is entering with a round 1 loss, enter 0.\
                If this player is entering round 2 with a 1-0 record enter 1",
                is_legal=lambda x : x < self.num_rounds, 
                error_message='A player should not have more byes than the total number of rounds.')
                
                for i in range(num_byes):
                    new_player.wins.append('BYE') 
                self.players.append(new_player)

            else:
                for i in range(len(self.players)):
                    if dropping == self.players[i].name:
                        print(self.players[i].name, "has been dropped.")
                        self.dropped_players.append(self.players[i])
                        self.players[i].name = '#' + self.players[i].name
                        del self.players[i]
                        break
            print()

    def get_results(self):
        still_playing = set(range(1, len(self.pairs) + 1))
        while len(still_playing) > 0:
            print("Waiting for results from tables", still_playing)
            table = prompt.for_int(
                "Enter a table number to report results",
                is_legal=lambda x: x in still_playing,
                error_message="Enter a table that has not finished their match.",
            )
            table -= 1
            winner = prompt.for_string(
                "Enter a winner (" + str(self.pairs[table][0].name) + ") or (" + str(self.pairs[table][1].name) + ") or (tie)",
                is_legal=lambda x: x == self.pairs[table][0].name or x == self.pairs[table][1].name or x == "tie",
                error_message="Please enter the winner's full name or tie",
            )
            if winner == "tie":
                self.pairs[table][0].ties.append(self.pairs[table][1])
                self.pairs[table][1].ties.append(self.pairs[table][0])
            else:
                if winner == self.pairs[table][0].name:
                    self.pairs[table][0].wins.append(self.pairs[table][1])
                    self.pairs[table][1].losses.append(self.pairs[table][0])
                else:
                    self.pairs[table][1].wins.append(self.pairs[table][0])
                    self.pairs[table][0].losses.append(self.pairs[table][1])

            still_playing.remove(table + 1)
            print()

    def calculate_standings(self):
        try:
            for player in self.players:
                player.tiebreaker = ""
                player.tiebreaker += str(player.get_points())
            for player in self.players:
                if self.get_opponents_win_percentage(player) == 0:
                    player.tiebreaker += "000"
                else:
                    player.tiebreaker += str(
                        int(round(self.get_opponents_win_percentage(player), 3) * 1000)
                    )
                num_opponents = 0
                percentage = 0
                for opponent in player.wins + player.losses + player.ties:
                    if opponent != "BYE":
                        percentage += self.get_opponents_win_percentage(opponent)
                        num_opponents += 1
                if percentage / num_opponents == 0:
                    player.tiebreaker += "000"
                else:
                    player.tiebreaker += str(
                        int(round(percentage / num_opponents, 3) * 1000)
                    )
        except ZeroDivisionError:
            player.tiebreaker = "0000000"

    def get_opponents_win_percentage(self, player):
        num_opponents = 0
        percentage = 0
        for opponent in player.wins + player.losses + player.ties:
            if opponent != "BYE":
                percentage += self.get_win_percentage(opponent)
                num_opponents += 1
        return percentage / num_opponents

    def get_win_percentage(self, player):
        return player.num_wins() / (player.num_wins() + player.num_losses() + player.num_ties())

    def print_standings(self):
        players = sorted(self.players, key=lambda x: -int(x.tiebreaker))
        for i, player in enumerate(players):
            print(i + 1, player.name, "Tie-breaker:", player.tiebreaker)

    def write_to_file(self, round):
        with open(f"{round}", "w") as savefile:
            savefile.write(str(round) + "\n")
            for player in self.players + self.dropped_players:
                savefile.write(player.name + ",")
            savefile.write("\n")
            for player in self.players + self.dropped_players:
                savefile.write("%" + player.name + "\n")
                savefile.write("$wins\n")
                for opponent in player.wins:
                    savefile.write("BYE\n" if opponent == "BYE" else opponent.name + "\n")
                savefile.write("$losses\n")
                for opponent in player.losses:
                    savefile.write(opponent.name + "\n")
                savefile.write("$ties\n")
                for opponent in player.ties:
                    savefile.write(opponent.name + "\n")

    def append_pairings_to_file(self, filename, pairs):
        with open(filename, "a") as savefile:
            savefile.write("*pairs:")
            for pair in pairs:
                savefile.write(pair[0].name + "," + ("BYE" if pair[1] == "BYE" else pair[1].name) + ",")

    def run_tournament(self):
        self._calculate_num_rounds()
        print("Playing", self.num_rounds, "rounds today.")
        for round_index in range(self.round_number, self.num_rounds + 1):
            print("\n--------------Round", round_index, "Pairings--------------")
            if self.pairs is None:
                self.pairs = self._pair_round(self.players)
            self.print_pairings(self.pairs)
            self.get_results()
            self.end_of_round_cleanup()
            self.round_number += 1
            self.pairs = None
        print("Final Standings:")
        self.print_standings()

    def run_from_file(self, filename):
        playerdict = {"BYE": "BYE"}
        round_num = 0
        with open(filename, "r") as savefile:
            round_num = int(savefile.readline().rstrip())
            playerNames = savefile.readline().rstrip().split(",")[:-1]
            for name in playerNames:
                playerdict[name] = Player.Player(name)
            for line in savefile:
                line = line.rstrip()
                if not line:
                    pass
                elif line.startswith("%"):
                    currentPlayer = line[1:]
                elif line.startswith("$"):
                    entryCategory = line[1:]
                elif line.startswith("*"):
                    people = line.split(":")[1].split(",")[:-1]
                    for i in range(0, len(people), 2):
                        self.pairs.append([playerdict[people[i]], playerdict[people[i + 1]]])
                else:
                    if entryCategory == "wins":
                        playerdict[currentPlayer].wins.append(playerdict[line])
                    elif entryCategory == "losses":
                        playerdict[currentPlayer].losses.append(playerdict[line])
                    elif entryCategory == "ties":
                        playerdict[currentPlayer].ties.append(playerdict[line])

        self.players = list(playerdict.values())
        for player in self.players:
            if player.name.startswith("#"):
                self.dropped_players.append(player)
                self.players.remove(player)
        self.run_tournament()

    def print_welcome_screen(self):
        print("Welcome to Tournament Software!\n")
        print("---------------How To Use---------------\n")
        print("1. Press s or n to either load a saved tournament or start a new one.")
        print("2. Find the PutYourTournamentParticipantsHere.txt file and enter participans on separate lines.")
        print("3. Follow on screen prompts to run tournament, all command available are enclosed in ().\n")

def main():
    tournament = Tournament()
    tournament.print_welcome_screen()
    shouldLoadFromSavefile = prompt.for_string(
        "Do you want to start a (n)ew tournament or (r)eload a tournament?",
        is_legal=lambda x: x in ["r", "n"],
        error_message="Please enter n or r.",
    )
    if shouldLoadFromSavefile == "r":
        fileStr = prompt.for_string("Enter the (round number) you want to reload from")
        tournament.run_from_file(fileStr)
    else:
        fob = goody.safe_open(
            "Press enter once all your partipants are in PutYourTournamentParticipantsHere",
            "r",
            "Error finding/opening the file.",
            default="PutYourTournamentParticipantsHere.txt",
        )
        tournament.players = file.get_names(fob)
        while len(tournament.players) < 4:
            print("\nYou need at least 4 players to start a tournament.")
            input()
            fob.close()
            fob = goody.safe_open(
                "Save the file!",
                "r",
                "Error finding/opening the file.",
                default="PutYourTournamentParticipantsHere.txt",
            )
            tournament.players = file.get_names(fob)

        while True:
            for player in tournament.players:
                print(player.name)
            start = prompt.for_string(
                "Start tournament? Enter (y)es or (n)o",
                is_legal=lambda x: x in ["y", "n"],
                error_message="Please enter y or n.",
            )
            if start == "y":
                tournament.run_tournament()
                break
            else:
                sys.exit("Ok, no rush! Restart the program when you're ready!") 

if __name__ == "__main__":
    main()
