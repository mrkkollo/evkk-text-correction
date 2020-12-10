import re


class NorvigEstnltkCore:

    def __init__(self):
        self.probability_dict = None
        self.study = None


    def words(self, text):
        return re.findall(r'\w+', text.lower())


    def P(self, word):
        """Probability of `word`."""
        "check if the üäöõ words count in as well"
        N = sum(self.study.values())
        return self.study[word] / N


    def correction(self, word):
        """Most probable spelling correction for word."""
        return max(self.candidates(word), key=self.P)


    def correction_with_ngrams(self, word, word_before):
        possible_corrections = self.candidates(word)

        corrections_dict = {}
        for correction in possible_corrections:
            corrections_dict.update({correction: self.P(correction)})

        for correct in possible_corrections:

            if (word_before, correct) in self.probability_dict.keys():
                corrections_dict[correct] += self.probability_dict[(word_before, correct)]

        return sorted(corrections_dict.items(), key=lambda key_value: key_value[1])[len(corrections_dict) - 1][0]


    def candidates(self, word):
        """Generate possible spelling corrections for word."""
        edits = self.edits1(word)
        known = self.known(edits)
        return list(known) + [word]


    def known(self, words):
        """The subset of `words` that appear in the dictionary of WORDS."""
        return set(w for w in words if w in self.study)


    def edits1(self, word):
        """All edits that are one edit away from `word`."""
        letters = 'abcdefghijklmnopqrstuvwxyzõüäö'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)


    def edits2(self, word):
        """All edits that are two edits away from `word`."""
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))
