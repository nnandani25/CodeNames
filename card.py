from nltk.corpus import wordnet as wn
class Card:
    def __init__(self, word):
        self.type = None
        self.word = word
        self.is_guessed = False
        self.synonyms = []
        self.symbol = None

    def get_synonyms(self):
        lst = []
        for w in wn.synonyms(self.word.lower()):
            lst.extend([x.lower().strip() for x in w])
        
        lst = [x for x in lst if x not in self.word and self.word not in x]
        if len(lst) == 0:
            lst = self.get_hypernyms(lst)

        # for j in lst:
        #     if j in self.word:
        #         lst.remove(j)

        #     elif self.word in j:
        #         lst.remove(j)
        lst = [x for x in lst if x not in self.word and self.word not in x]
        self.synonyms = lst
        return lst

    def get_hypernyms(self, lst):
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
        synset = wn.synsets(self.word)
        for s in synset:
            for h in s.hyponyms():
                for lemma in h.lemmas():
                  lst.append(lemma.name().lower())
        # print("HYPO", lst)
        return lst

    def get_best_synonym(self):
        syn = self.get_synonyms()
        # syn.remove(self.word)
        most_sim = syn[0]
        highest_sim = -100
        for i in syn:
            if self.calculate_similarity(i, self.word) > highest_sim:
                highest_sim = self.calculate_similarity(i, self.word)
                most_sim = i
                
        # print(syn)
        # print("Word:", self.word)
        return most_sim
    

    def calculate_similarity(self, guess, card, mode=0):
        w1 = wn.synsets(card)[0]
        w2 = wn.synsets(guess)[0]
        score = w1.wup_similarity(w2)
        return score