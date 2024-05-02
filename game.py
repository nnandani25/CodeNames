from nltk.corpus import wordnet as wn
import random
from card import Card
from player import Player
class Game:
    def __init__(self, filename):
        # Load the words from file
        self.words = self.load_words(filename)

        # self.synonyms = self.get_synonyms()

        # self.cards = [Card(word) for word in random.sample(self.words,25)]
        good_words = []
        for word in self.words:
            card = Card(word)
            card.get_synonyms()
            if len(card.synonyms) != 0:
                good_words.append(word)

        self.all_words = random.sample(good_words,25)
        self.cards = [Card(word) for word in self.all_words]
        # for card in self.cards:
        #     print(card.word.upper(), card.get_synonyms(), "\n")
        
        random.shuffle(self.cards)
        self.p1_words = self.cards[0:9]
        self.p2_words = self.cards[9:18]
        self.assasin_card = self.cards[18]
        self.blank_cards = self.cards[19:]
        self.player1 = Player("player1")
        self.player2 = Player("player2")
        self.current_word = None


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
    

    def give_clue(self, player, opponent):  
        available_cards = []
        if player == self.player1:
            for card in self.p1_words:
                if card.is_guessed == False:
                    available_cards.append(card)
        
        else:
            for card in self.p2_words:
                if card.is_guessed == False:
                    available_cards.append(card)
        print("Avail:", [x.word for x in available_cards])

        if len(available_cards) == 0:
            self.checkwin(player, opponent)

        self.current_word = random.choice(available_cards)

        # print("WORD", self.current_word.word)
        hint_word = self.current_word.get_best_synonym()
        print(self.current_word.word)
        

        # print("HINT: ", hint_word.word)
        return hint_word
    
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

        # Weighitng them
        # FInds a word similar to yours and oppositve of the other ones
    # def word_score(hint):
    #     score = 0
    #     for word in pos_words:
    #         score += self.calculate_similarity(hint, word)

    #     for word in neg_words:
    #         score -= self.calculate_similarity(hint, word)
    #     return score
        
        # picks the word with the highest score, using word_score, keeps track
        # return max(possible_words, key=word_score)
        # lowest common hypernym


    def guess(self):
        is_valid = False
        while not is_valid:
            guess = input("Guess: ")
            is_valid = True

            if guess not in self.all_words:
                    print("Please enter a card on the board.")
                    is_valid = False
                    continue

            for card in self.cards:
                if guess.lower() == card.word.lower():
                    if card.is_guessed:
                        print("\nThis card has been guessed already.\n")
                        is_valid = False
                        break
        return guess

    def print_intstructions(self):
        # Instructions
        print("\nWelcome to Contexto!")
        print("Blank:", end =" ")
        for blank in self.blank_cards:
            print(blank.word, end=" ")

        print("\nPlayer 1:", end=" ")
        for p1c in self.p1_words:
            print(p1c.word, end=" ")

        print("\nPlayer 2:", end=" ")
        for p2c in self.p2_words:
            print(p2c.word, end = " ")

        print("\nDeath: ", self.assasin_card.word)
        print("")
    
    def checkwin(self, current_player, opponent):
        # winner = False
        if current_player == self.player1:
            won = True
            for card in self.p1_words:
                if card.is_guessed == False:
                    won = False

            # if current_player.score == len(self.p1_words):
            if won == True:
                print("\n", current_player.name.upper(), "UNCOVERED ALL OF THEIR CARDS\n")
                print(current_player.name, "'s Score:", current_player.score)
                print(opponent.name, "'s Score:", opponent.score, "\n")
                return True
                # return
        else:
            if current_player.score == len(self.p2_words):
                won = True
                for card in self.p2_words:
                    if card.is_guessed == False:
                        won = False

                if won == True:
                    print("\n", current_player.name.upper(), "UNCOVERED ALL OF THEIR CARDS\n")
                    print(current_player.name, "'s Score:", current_player.score)
                    print(opponent.name, "'s Score:", opponent.score, "\n")
                    return True
                    # return


        print(current_player.name, "'s Score:", current_player.score)
        print(opponent.name, "'s Score:", opponent.score)
        return False
    def run(self):
        """
        Main game loop. Runs until 
        the user quits or guesses the 
        word correctly
        """
        self.print_intstructions()
        current_player = self.player1
        opponent = self.player2
        random.shuffle(self.cards)
        
        # # Main game loop
        while True:
            # print(self.cards)
            count = 0
            for i in self.cards:
                # print(i.word, end="\t\t")
                print(f'{i.word:20}', end='')
                count+=1
                if count%5 == 0:
                    print("\n")
            
            print(current_player.name,"'s turn")

            print("HINT:", self.give_clue(current_player, opponent))

            guess = self.guess()

            for card in self.cards:
                if guess.lower() == card.word.lower():
                    if card == self.assasin_card:
                        print("You selected the assasin card...\n")
                        print("\nGAME OVER\n")
                        print(current_player.name, "'s Score:", current_player.score)
                        print(opponent.name, "'s Score:", opponent.score, "\n")

                        if current_player.score > opponent.score:
                            print(current_player.name, "wins!")
                        
                        else:
                            print(opponent.name, "wins!")
                        return
                    
                    if guess == self.current_word.word:
                        current_player.score += 1
                        print("Nice Job!")

                    else:
                        if card in self.p1_words and current_player == self.player1:
                            self.player1.score += 1
                            print("That's not the word I was thinking of, but that is one of your words!")
                        
                        elif card in self.p2_words and current_player == self.player2:
                            self.player2.score += 1
                            print("That's not the word I was thinking of, but that is one of your words!")
                
                        elif card in self.p2_words and current_player == self.player1:
                            print("You picked your opponent's card...")
                            self.player2.score += 1

                        elif card in self.p1_words and current_player == self.player2:
                            print("You picked your opponent's card...")
                            self.player1.score += 1

                        else:
                            print("\nYou picked a nuetral card.\n")
                    
                    card.is_guessed = True
                    card.word = card.word.upper()

            if(self.checkwin(current_player, opponent)):
                break
            temp = current_player
            current_player = opponent
            opponent = temp
            

if __name__ == "__main__":
    contexto_game = Game("/Users/navyan21/Desktop/School 2023-2024/ATCS/Labs/Unit07/IntroToNLP/data/words.txt")
    contexto_game.run()


# Erros:
# - some hints come out to the actual word or as None
# - guess again if the card has already been guessed
# - tie