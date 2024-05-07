from nltk.corpus import wordnet as wn
import random
from card import Card
from player import Player
import re
class Game:
    def __init__(self, filename):
        # Load the words from file
        self.words = self.load_words(filename)
        good_words = []
        for word in self.words:
            card = Card(word)
            card.get_synonyms()
            if len(card.synonyms) != 0:
                good_words.append(word)

        self.all_words = random.sample(good_words,25)
        self.cards = [Card(word) for word in self.all_words]
        
        random.shuffle(self.cards)
        self.p1_words = self.cards[0:9]
        self.p2_words = self.cards[9:18]
        self.assasin_card = self.cards[18]
        self.blank_cards = self.cards[19:]
        self.player1 = Player("player1")
        self.player2 = Player("player2")
        self.current_word = None
        self.curr_words = []

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
        # print("Avail:", [x.word for x in available_cards])

        if len(available_cards) == 0:
            self.checkwin(player, opponent)

        self.current_word = random.choice(available_cards)
        # self.find_common_hypernyms(self.current_word, available_cards)


        sim_words = self.current_word.most_sim_words(available_cards)
        # print("Curr Word", self.current_word.word)
        # print("Sim", [x.word for x in sim_words])
        if len(sim_words) == 0:
            hint_word = self.current_word.get_best_synonym()
            sim_words.append(hint_word)
        
        else:
            sim_words.append(self.current_word)
            self.curr_words.extend(sim_words)
            hint_word = self.common_word(sim_words)

        # hint_word = self.current_word.get_best_synonym()
        # print(self.current_word.word)
        

        # print("HINT: ", hint_word.word)
        return hint_word, len(sim_words)
    

    def common_word(self, sim_cards):
        # print(len(sim_cards))

        lst = []
        for i in range(len(sim_cards)-1):
            synset = wn.synsets(sim_cards[i].word)[0]
            synset2 = wn.synsets(sim_cards[i+1].word)[0]
            # print(synset.name(), synset2.name())
     
            lst.extend((wn.synset(synset.name()).lowest_common_hypernyms(wn.synset(synset2.name()))))

    
        # print("COMS", lst)
        hint = (random.choice(lst)).name()
        pos = hint.find('.')
        x = slice(0, pos)


        return hint[x]



    def find_word(self, player):
        if player == self.player1:
            pos_words = self.p1_words
            neg_words = self.p2_words
        else:
            pos_words = self.p2_words
            neg_words = self.p1_words
        
        possible_words = set()
        for word in pos_words:
            for syn in wn.synsets(word.word):
                for lemma in syn.lemmas():
                        possible_words.add(lemma.name().lower())
        # Removes the pos words from the possible words set
        possible_words = possible_words.difference([word.word for word in pos_words])



    def guess(self):
        is_valid = False
        while not is_valid:
            guess = input("\nGuess: ")
            is_valid = True

            if guess not in self.all_words:
                    print("\nPlease enter a card on the board.")
                    is_valid = False
                    continue

            for card in self.cards:
                if guess.lower() == card.word.lower():
                    if card.is_guessed:
                        print("\nThis card has been guessed already.")
                        is_valid = False
                        break

        return self.find_card(guess)


    
    def checkwin(self, current_player, opponent):
        
        if self.assasin_card.is_guessed:
            return opponent
        
        if current_player.score > opponent.score:
            return current_player
        
        else:
            return opponent
        
    
    def is_game_over(self):
        if self.assasin_card.is_guessed == True:
            return True
        
        if self.player1.score == len(self.p1_words):
            return True
        
        if self.player2.score == len(self.p2_words):
            return True
    
        return False

    def find_card(self, guess):
        player_card = None
        for card in self.cards:
            if guess == card.word:
                player_card = card
        
        return player_card

    def display_board(self):
        count = 0
        print("┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐\n")

        for i in self.cards:
                # len = 0
                # while len < 5:
                #     print("┌─────────┐", end='')
                #     print("                  ", end='')
                #     len+=1

                print(f'│     {i.word:10}        ', end='')

                # print("│",i.word, "         |         ", end='')


                # print("│", end='')

                # print("+---------------+")
                # print("|               |")
                # print("|",i.word,           "|")
                # print("|               |")
                # print("+---------------+", end='')
                count+=1                
                if count%5 == 0:
                    print("│", end='')
                    print("\n")
        
        print("└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘\n")


    def print_intstructions(self):
        # Instructions
        print("\nWelcome to Code Names!")
        # print("Blank:", end =" ")
        # for blank in self.blank_cards:
        #     print(blank.word, end=" ")

        # print("\nPlayer 1:", end=" ")
        # for p1c in self.p1_words:
        #     print(p1c.word, end=" ")

        # print("\nPlayer 2:", end=" ")
        # for p2c in self.p2_words:
        #     print(p2c.word, end = " ")

        # print("\nDeath: ", self.assasin_card.word)
        # print("")

        print("\n\nHow to play:\n")
        print("As the computer, I have selected certain cards for each player and you have to guess which card"
               " is yours based on a hint \nthat I give you, but one card is the assasin card and if you guess that you will die")
        print("\nI will try to group the cards together under one hint and if I do that, I will tell you the amount of cards you can guess")
        print("\nGuesses:")
        print("1. if you guess the correct card, your score increases and it is the next players turn")
        print("2. if you guess the correct card and the hint was for multiple cards you can guess again")
        print("3. if you guess your opponents card, your opponent gets a point")
        print("4.if you guess a nuetral card, no one gets a point")
        print("5. if you guess the assasin card, the game ends\n")

    def run(self):
        """
        Main game loop. Runs until 
        the user quits or guesses the 
        word correctly
        """
        self.print_intstructions()
        self.player1.name = input(("Player 1 Name: "))
        self.player2.name = input(("Player 2 Name: "))
        print("")

        current_player = self.player1
        current_player.type = 1
        opponent = self.player2
        opponent.type = 2
        random.shuffle(self.cards)
    
        
        # # Main game loop
        while True:
            self.display_board()
            
            print(current_player.name.strip().upper(),"'s TURN")
            print("──────────────────────────")
            clue, num_words = self.give_clue(current_player, opponent)
            print("Hint:", clue)
            print("Number of Cards:", num_words)

            while num_words > 0:
                guess = self.guess()
                guess.is_guessed = True
                guess.word = guess.word.upper()

                if guess.type == 4:
                    print("\nYou selected the assasin card...\n")
                    break

                elif guess.type == current_player.type:
                    current_player.score += 1
                    print("\nNice Job!")
                    num_words -= 1
            
                elif guess.type == opponent.type:
                    print("\nYou picked your opponent's card...")
                    opponent.score += 1
                    break

                else:
                    print("\nYou picked a nuetral card.")
                    break

            print("\n")  
            print(current_player.name.upper(), "Score:", current_player.score)
            print(opponent.name, "Score:", opponent.score, "\n")
            if self.is_game_over():
                break
            temp = current_player
            current_player = opponent
            opponent = temp


        winner = self.checkwin(current_player, opponent)
        print(winner.name, "WINS!!")





if __name__ == "__main__":
    contexto_game = Game("/Users/navyan21/Desktop/School 2023-2024/ATCS/Labs/Unit07/IntroToNLP/data/words.txt")
    contexto_game.run()


# Erros:
# - tie
# - number of guesses if they get it right for coms
# - hints are not with the same words for coms 