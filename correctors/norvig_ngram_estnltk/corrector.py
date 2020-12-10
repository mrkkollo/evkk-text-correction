import logging
import pathlib
from collections import Counter

from estnltk import Text
from nltk import ngrams

from correctors.norvig_ngram_estnltk.core import NorvigEstnltkCore
from helpers import Correction


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', )


class PeterNorvigNgramCorrector(NorvigEstnltkCore):
    DEFAULT_CORPUS_PATH = "texts/training_texts/norvig_corpus.txt"
    DEFAULT_MAPPING_PATH = "models/texts/training_texts/word_mapping.csv"


    def __init__(self, corpus_path: str = DEFAULT_CORPUS_PATH, correction_mapping_path: str = DEFAULT_MAPPING_PATH):
        super(PeterNorvigNgramCorrector, self).__init__()
        self.corpus_path = corpus_path
        self.probability_dict = self._return_probability_dict()
        self.study = self._get_study()
        self.word_mapping = PeterNorvigNgramCorrector.load_mapper_resources(correction_mapping_path)


    @staticmethod
    def load_mapper_resources(file_path: str):
        path = pathlib.Path(file_path)
        if path.exists() and path.suffix == ".csv":
            logging.debug("Starting loading the word mapping for preprocessing!")
            mapping = []
            with open(file_path, "r", encoding="utf8") as fp:
                for line in fp:
                    mistake, correct = line.split(",")
                    mistake, correct = mistake.strip(), correct.strip()
                    mapping.append((mistake, correct))
            logging.debug("Finished loading the word mapping for preprocessing!")
            return mapping
        else:
            raise FileNotFoundError("Could not find the CSV file with the path: {}!".format(file_path))


    @staticmethod
    def make_n_gramlist(text, n=2):
        nngramlist = []
        for s in ngrams(text.split(), n=n):
            nngramlist.append(s)
        return nngramlist


    def _return_probability_dict(self):
        text = open(self.corpus_path, "r", encoding="UTF-8").readline()

        probability_dict = {}
        n_gram_corpus = PeterNorvigNgramCorrector.make_n_gramlist(text)
        words = Counter(text.split(" "))
        phrases = Counter(n_gram_corpus)

        for phrase in phrases:
            probability_dict.update({phrase: phrases[phrase] / words[phrase[0]]})

        return probability_dict


    def _get_study(self):
        """File of the base corpus."""
        return Counter(self.words(open(self.corpus_path, encoding="utf-8").read()))


    def preprocess_text(self, original_text: str):
        logging.debug("Replacing the words in the text by the defined mappings from the file as a preprocessing step!")
        processed_text = original_text
        for mistake, correct in self.word_mapping:
            processed_text = processed_text.replace(mistake, correct)
        logging.debug("Finished replacing the words!")
        return processed_text


    def correct_text(self, text: str):
        text = self.preprocess_text(text)

        tokens = self.words(text)
        candidates = {}

        estnltk_wrapper = Text(" ".join(tokens))
        data = estnltk_wrapper.get.spelling.spelling_suggestions.as_dataframe
        marks = data['spelling']
        fixed = tokens[0] + " "

        i = 2
        for index in range(1, len(tokens)):
            word = tokens[index]
            word_before = fixed.split(" ")[index - 1]
            corrected = self.correction_with_ngrams(word, word_before)
            if not marks[index] and word != corrected:
                fixed += corrected + " "
                if word != corrected and self.candidates(word):
                    candidates[word] = self.candidates(word)
            else:
                fixed += word + " "

            i += 1

        return Correction(original=text, correction=fixed, candidates=candidates)


if __name__ == '__main__':
    norvig = PeterNorvigNgramCorrector(correction_mapping_path="texts/training_texts/word_mapping.csv")
    correction = norvig.correct_text("Ma kaisin poes!")
    pass
