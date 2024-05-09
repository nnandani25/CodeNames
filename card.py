from nltk.corpus import wordnet as wn
import random
class Card:
    def __init__(self, word):
        self.type = None
        self.word = word
        self.is_guessed = False
        self.synonyms = []

    def get_synonyms(self):
        # Gets the synonyms for the words
        lst = []
        for w in wn.synonyms(self.word.lower()):
            lst.extend([x.lower().strip() for x in w])
        
        lst = [x for x in lst if x not in self.word and self.word not in x]

        # If the list is empty, looks for hypoernyms
        if len(lst) == 0:
            lst = self.get_hypernyms(lst)
        lst = [x for x in lst if x not in self.word and self.word not in x]
        self.synonyms = lst

        # Returns a list with snyonyms and potentially hypernyms and hyponyms
        return lst

    def get_hypernyms(self, lst):
        # In case there are no synonyms, looks for hypernyms
        synset = wn.synsets(self.word)
        for s in synset:
            for h in s.hypernyms():
                for lemma in h.lemmas():
                  lst.append(lemma.name().lower())
        # print("HYPER", lst)

        if len(lst) == 0:
            lst = self.get_hyponyms(lst)

        return lst

    def get_hyponyms(self, lst):
        # In case there are no hypernyms, looks for hyponyms
        synset = wn.synsets(self.word)
        for s in synset:
            for h in s.hyponyms():
                for lemma in h.lemmas():
                  lst.append(lemma.name().lower())
        return lst

    def get_best_synonym(self):
        # Finds the best synonym based on similarity
        syn = self.get_synonyms()
        most_sim = syn[0]
        highest_sim = -100
        for i in syn:
            if self.calculate_similarity(i, self.word) > highest_sim:
                highest_sim = self.calculate_similarity(i, self.word)
                most_sim = i
        return most_sim
    

    def calculate_similarity(self, guess, card, mode=0):
        # Calculates the similarity between two words
        w1 = wn.synsets(card)[0]
        w2 = wn.synsets(guess)[0]
        score = w1.wup_similarity(w2)
        return score
    

    def most_sim_words(self, available_cards):
        # Calculates the Wu-Palmer similarity and finds the words most similar in a players cards
        sim_cards = []
        for card in available_cards:
            score = card.calculate_similarity(self.word, card.word)
            # Adds it to the list of similar words it the similarity score is above 0.45 and less than 1
            if score >= 0.45 and score < 1:
                sim_cards.append(card)
        return sim_cards
    