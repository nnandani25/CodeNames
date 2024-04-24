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
        self.all_words = random.sample(self.words,25)
        self.cards = [Card(word) for word in self.all_words]
        
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
    
    def get_synonyms(self, word):
        """
        Generates all synonyms for self.word
        based off of WordNet

        Returns:
            list[str]: A list of synonyms for self.word
        """
        synonyms = []
        
        # Loop through all the synsets for the word
        for syn in wn.synsets(word):
            # Loop through all lemmas in the synset
            for lemma in syn.lemmas():
                if lemma.name() not in synonyms:
                    synonyms.append(lemma.name().lower())
        
        if word in synonyms:
            synonyms.remove(word)
        print("word:", word)

        most_sim = None
        highest_sim = -100
        for i in synonyms:
            if self.calculate_similarity(i, word) > highest_sim:
                highest_sim = self.calculate_similarity(i, word)
                most_sim = i
        # print("Most_sim", most_sim)
        return most_sim

    def give_clue(self, player):  
        available_cards = []
        if player == self.player1:
            for card in self.p1_words:
                if card.is_guessed == False:
                    available_cards.append(card)
        
        else:
            for card in self.p2_words:
                if card.is_guessed == False:
                    available_cards.append(card)
        self.current_word = random.choice(available_cards)
        print("WORD", self.current_word.word)
        hint_word = self.get_synonyms(self.current_word.word)
        print("HINT: ", hint_word)
        # return "Hint:" + hint_word


        # hint_word = random.choice(self.synonyms)
        # while hint_word == self.word or hint_word in self.word:
        #     hint_word = random.choice(self.synonyms)

        #     w1 = wn.synsets(self.word)[0]
        #     w2 = wn.synsets(hint_word)[0]
        #     score = w1.wup_similarity(w2)
        #     print(str(hint_word) + " has a score of " + str(score))
        #     self.synonyms.remove(hint_word)
        
        # return hint_word
    
    def calculate_similarity(self, guess, card, mode=0):
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
        w1 = wn.synsets(card)[0]
        w2 = wn.synsets(guess)[0]
        score = w1.wup_similarity(w2)

        
        return score
    
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




    def run(self):
        """
        Main game loop. Runs until 
        the user quits or guesses the 
        word correctly
        """

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

        current_player = self.player1
        opponent = self.player2
        random.shuffle(self.cards)
        
        # # Main game loop
        while True:
            # print(self.cards)
            count = 0
            for i in self.cards:
                print(i.word, end="\t\t")
                count+=1
                if count%5 == 0:
                    print("\n")
            
            print(current_player.name,"'s turn")

            self.give_clue(current_player)

            guess = input("Guess: ")

            if guess not in self.all_words:
                while guess not in self.all_words:
                    print("Please enter a card on the board.")
                    guess = input("Guess: ")
            
            for card in self.cards:
                if guess == card.word:
                    if card.is_guessed == True:
                        print("\nThis card has been guessed already.\n")
                        break
                    
                    elif card == self.assasin_card:
                        print("You selected the assasin card...\n")
                        print("\nGAME OVER\n")
                        print(current_player.name, "'s Score:", current_player.score)
                        print(opponent.name, "'s Score:", opponent.score, "\n")

                        if current_player.score > opponent.score:
                            print(current_player.name, "wins!")
                        
                        else:
                            print(opponent.name, "wins!")
                        

                        return
                    
                    if guess == self.current_word:
                        current_player.score += 1
                        print("Nice Job!")

                    elif card in self.p1_words and current_player == self.player1:
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

            print(current_player.name, "'s Score:", current_player.score)
            print(opponent.name, "'s Score:", opponent.score)
            temp = current_player
            current_player = opponent
            opponent = temp
            
                

            # # TODO: Complete the options
            # if guess == "h":
            #     # self.get_a_hint()

            # elif guess == "q":
            #     print(self.word)
            #     break
            
            # elif guess == self.word:
            #     print("Yay you win!!!")
            #     break
            
            # else:
            #     print(self.calculate_similarity(guess))
                # guess = input("Guess a word, enter 'h' for a hint, or enter 'q' to reveal the answer: ")



if __name__ == "__main__":
    contexto_game = Game("/Users/navyan21/Desktop/School 2023-2024/ATCS/Labs/Unit07/IntroToNLP/data/words.txt")
        # "data/words.txt")
    contexto_game.run()


# Erros:
# - some hints come out to the actual word
# - when the user enters the correct word, the computer outputs, "thats not what I was thinking, but it is in your cards" b/c of cards vs. word