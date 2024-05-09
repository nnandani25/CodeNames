from nltk.corpus import wordnet as wn
import random
from card import Card
from player import Player
class Game:
    def __init__(self, filename):
        # Load the words from file
        self.words = self.load_words(filename)
        good_words = []

        # Ensures that the words have synonyms
        for word in self.words:
            card = Card(word)

            card.get_synonyms()
            if len(card.synonyms) != 0:
                good_words.append(word)

        # Creates the deck of cards with 25 words
        self.all_words = random.sample(good_words,25)
        self.cards = [Card(word) for word in self.all_words]
        
        # Shuffles the deck
        random.shuffle(self.cards)
        self.p1_words = self.cards[0:9]
        self.p2_words = self.cards[9:18]
        self.assasin_card = self.cards[18]
        self.blank_cards = self.cards[19:]
        self.player1 = Player("player1")
        self.player2 = Player("player2")
        self.current_word = None
        self.curr_words = []
        self.current_player = None
        self.opponent = None
        self.num_words = 0
        self.game_over = False
        self.difficulty = 0

        # Sets the types for the words
        for card in self.p1_words:
            card.type = 1
        
        for card in self.p2_words:
            card.type = 2

        for card in self.blank_cards:
            card.type = 3
        
        self.assasin_card.type = 4

    def load_words(self, filename):
        """
        Loads the words from the provided file

        Args:
            filename (str): Filepath for the words

        Returns:
            list[str]: list of lowercase words
        """
        with open(filename, 'r') as file:
            words = [line.lower().strip() for line in file.readlines()]
        return words
    
    def get_available_cards(self, player):
        # Gets a list of cards which have not been guessed based on the player
        available_cards = []
        if player == self.player1:
            for card in self.p1_words:
                if card.is_guessed == False:
                    available_cards.append(card)
        
        else:
            for card in self.p2_words:
                if card.is_guessed == False:
                    available_cards.append(card)
        return available_cards

    def give_clue(self, player, opponent):  
        available_cards = self.get_available_cards(player)
        if len(available_cards) == 0:
            self.checkwin(player, opponent)

        # Selects a random card from the avaiable cards
        self.current_word = random.choice(available_cards)

        # Finds all of the words that are similar in the players cards
        sim_words = self.current_word.most_sim_words(available_cards)

        # If there are no similar words, it gives the player 1 word to guess
        if len(sim_words) == 0:
            hint_word = self.current_word.get_best_synonym()
            sim_words.append(hint_word)
        
        # Otherwise, it prints out the number of cards they need to guess and finds a hint word
        else:
            sim_words.append(self.current_word)
            self.curr_words.extend(sim_words)
            hint_word = self.common_word(sim_words)

        return hint_word, len(sim_words)
    

    def common_word(self, sim_cards):
        # Finds the lowest common hypernym for the common words
        lst = []
        for i in range(len(sim_cards)-1):
            synset = wn.synsets(sim_cards[i].word)[0]
            synset2 = wn.synsets(sim_cards[i+1].word)[0]
            lst.extend((wn.synset(synset.name()).lowest_common_hypernyms(wn.synset(synset2.name()))))

        # Makes the hint one of the words from the list of lowest common hypernyms
        hint = (random.choice(lst)).name()
        pos = hint.find('.')
        x = slice(0, pos)
        clue = hint[x]
        while clue.lower() == self.current_word.word.lower():
            hint = (random.choice(lst)).name()
            pos = hint.find('.')
            x = slice(0, pos)

        return hint[x]


    def guess(self):
        # Checks if the guess is valid and if not makes the user guess again
        is_valid = False
        while not is_valid:
            guess = input("\nGuess: ")
            is_valid = True

            # Checks if the card is on the board
            if guess not in self.all_words:
                    print("\nPlease enter a card on the board.")
                    is_valid = False
                    continue

            # Checks if the card has been guessed and if so, prompts the user for another guess
            for card in self.cards:
                if guess.lower() == card.word.lower():
                    if card.is_guessed:
                        print("\nThis card has been guessed already.")
                        is_valid = False
                        break

        return self.find_card(guess)


    
    def checkwin(self, current_player, opponent):
        # Checks various things for wins and returns the winner
        # Checks if the assasin card has been guessed
        if self.assasin_card.is_guessed:
            return opponent
        
        #  Checks who's score is larger
        if current_player.score > opponent.score:
            return current_player
        
        else:
            return opponent
    
    def is_game_over(self):
        # Checks if the game is over
        # Checks if the assasin card has been guessed
        if self.assasin_card.is_guessed == True:
            return True
        
        # Checks if the players score is the same as the length of their cards
        if self.player1.score == len(self.p1_words):
            return True
        
        if self.player2.score == len(self.p2_words):
            return True
    
        return False

    def find_card(self, guess):
        # Finds the card of the guess
        player_card = None
        for card in self.cards:
            if guess == card.word:
                player_card = card
        
        return player_card
    

    def print_intstructions(self):
        # Prints the instructions
        print("\nWelcome to Code Names!")
        print("\n\nHow to play:\n")
        print("As the computer, I have selected certain cards for each player and you have to guess which card"
               " is yours based on a hint \nthat I give you, but one card is the assasin card and if you guess that you will die")
        print("\nI will try to group the cards together under one hint and if I do that, I will tell you the amount of cards you can guess")
        print("\nGuesses:")
        print("1. If you guess the correct card, your score increases and it is the next players turn")
        print("2. If you guess the correct card and the hint was for multiple cards you can guess again")
        print("3. If you guess your opponents card, your opponent gets a point")
        print("4. If you guess a nuetral card, no one gets a point")
        print("5. If you guess the assasin card, the game ends\n")
        print("To guess, click on a card and look at the console for further instructions\n")

    def setup(self):
        # Prints instructions, gets users names
        self.print_intstructions()
        self.player1.name = input(("Player 1 Name: "))
        self.player2.name = input(("Player 2 Name: "))
        print("")

        # Instanciates variables
        self.current_player = self.player1
        self.current_player.type = 1
        self.current_player.color = "blue"
        self.opponent = self.player2
        self.opponent.type = 2
        self.opponent. color = "red"
        random.shuffle(self.cards)
    
    def change_turn(self):
        # Prints the scores of the players
        print(self.current_player.name.upper(), "Score:", self.current_player.score)
        print(self.opponent.name, "Score:", self.opponent.score, "\n")   
        
        # Checks if the game is over and if it is, runs end_game         
        if self.is_game_over():
            self.end_game()
            return
        
        # Switches who is the current player and who is the opponent
        temp = self.current_player
        self.current_player = self.opponent
        self.opponent = temp
        self.run_turn()
    
    def end_game(self):
        # Checks who won and prints it
        winner = self.checkwin(self.current_player, self.opponent)
        print(winner.name, "WINS!!")
        # Sets game_over to true so the front end knows to end the game
        self.game_over = True


    def make_guess(self, guess):
        # Gets the card for guess
        guess = self.find_card(guess)
        guess.is_guessed = True

        # If the guess was the assasin card, ends the game
        if guess.type == 4:
            print("You selected the assasin card...\n")
            self.end_game()

        # If the guess was one of the players cards, increases score and reduced num_words
        elif guess.type == self.current_player.type:
            self.current_player.score += 1
            self.num_words -= 1
            print("Nice Job!")
            if self.num_words == 0:
                self.change_turn()
            else:
                print("You still have", self.num_words, "more words under this theme.")

        # If the guess was the opponents card, tells them, increases opponents score, and changes turn
        elif guess.type == self.opponent.type:
                print("You picked your opponent's card...")
                self.opponent.score += 1
                self.change_turn()

        # Otherwise, the card is nuetral
        else:
            print("You picked a neutral card.")
            self.change_turn()
    
    def run_turn(self):
        # Prints the players name, their clues, and their number of cards
        print(self.current_player.name.strip().upper(),"'s TURN (", self.current_player.color, ")")
        print("──────────────────────────")
        clue, self.num_words = self.give_clue(self.current_player, self.opponent)
        print("Hint:", clue)
        print("Number of Cards:", self.num_words)
