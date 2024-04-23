from nltk.corpus import wordnet as wn
import random
from card import Card
from player import Player
class Game:
    def __init__(self, filename):
        # Load the words from file
        self.words = self.load_words(filename)

        self.synonyms = self.get_synonyms()

        self.cards = [Card(word) for word in random.sample(self.words,25)]
        
        random.shuffle(self.cards)
        self.p1_words = self.cards[0:9]
        self.p2_words = self.cards[9:18]
        self.assasin_card = self.cards[18]
        self.blank_cards = self.cards[19:]
        self.player1 = Player("player1")
        self.player2 = Player("player2")


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
    
    def get_synonyms(self):
        """
        Generates all synonyms for self.word
        based off of WordNet

        Returns:
            list[str]: A list of synonyms for self.word
        """
        synonyms = []
        
        # TODO: Complete this function

        # Loop through all the synsets for the word
        for syn in wn.synsets(self.word):
            # Loop through all lemmas in the synset
            for lemma in syn.lemmas():
                if lemma.name() not in synonyms:
                    synonyms.append(lemma.name())
        synonyms.remove(self.word)
        return synonyms

    def give_clue(self):
        
        hint_word = random.choice(self.synonyms)
        while hint_word == self.word or hint_word in self.word:
            hint_word = random.choice(self.synonyms)

            w1 = wn.synsets(self.word)[0]
            w2 = wn.synsets(hint_word)[0]
            score = w1.wup_similarity(w2)
            print(str(hint_word) + " has a score of " + str(score))
            self.synonyms.remove(hint_word)
        
        return hint_word
    
    def calculate_similarity(self, guess, mode=0):
        """
        Calculates and returns the similarity of 
        guess and self.word.

        Args:
            guess (str): The user's guess
            mode (int, optional): How to calculate similarity. Defaults to 0.
             0: Wu-Palmer Similarity 

        Returns:
            float: similarity score
        """
        # TODO: Complete this function
        w1 = wn.synsets(self.word)[0]
        w2 = wn.synsets(guess)[0]
        score = w1.wup_similarity(w2)

        
        return score
    

    def run(self):
        """
        Main game loop. Runs until 
        the user quits or guesses the 
        word correctly
        """

        # Instructions
        print("\nWelcome to Contexto!")
        print("Blank:", self.copy_cards)
        print("Player 1", self.p1_words)
        print("Player 2", self.p2_words)
        print("Death", self.assasin_card)

        turn = self.player1
        # # Main game loop
        while True:
            print(self.cards)
            self.give_clue()
            guess = input("Guess: ")

            for card in self.cards:
                if guess == card:
                    if card.is_guessed == True:
                        print("NO")
                        break
                    
                    elif card == self.assasin_card:
                        print("DEAD")
                        break
                    
                    elif card in self.p1_words and turn == self.player1:
                        print("YAY")
                        card.is_guessed = True
                        self.player1.score += 1
                        turn = self.player2
                        break
                    
                    elif card in self.p2_words and turn == self.player2:
                        print("YAY")
                        card.is_guessed = True
                        self.player2.score += 1
                        turn = self.player1
                        break
            


            # TODO: Complete the options
            if guess == "h":
                # self.get_a_hint()

            elif guess == "q":
                print(self.word)
                break
            
            elif guess == self.word:
                print("Yay you win!!!")
                break
            
            else:
                print(self.calculate_similarity(guess))
                # guess = input("Guess a word, enter 'h' for a hint, or enter 'q' to reveal the answer: ")



if __name__ == "__main__":
    contexto_game = Game("/Users/navyan21/Desktop/School 2023-2024/ATCS/Labs/Unit07/IntroToNLP/data/words.txt")
        # "data/words.txt")
    contexto_game.run()

