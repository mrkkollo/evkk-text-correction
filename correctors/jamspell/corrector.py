import logging
import pathlib
from typing import List

import jamspell

from helpers import Correction


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', )


class JamspellCorrector:
    DEFAULT_MAPPING_PATH = "texts/training_texts/word_mapping.csv"
    DEFAULT_MODEL_PATH = "models/estonski.bin"


    def __init__(self, model_path: str = DEFAULT_MODEL_PATH, correction_mapping_path: str = DEFAULT_MAPPING_PATH):
        self.corrector = jamspell.TSpellCorrector()
        self.word_mapping = JamspellCorrector.load_mapper_resources(correction_mapping_path)
        self.load_corrector_resources(model_path)


    def process_test_file(self, file_path: str, use_preprocessing: bool = True) -> List[Correction]:
        container = []
        path = pathlib.Path(file_path)
        if path.exists():
            with open(file_path, "r", encoding="utf8") as fp:
                for line in fp:
                    line = line.strip()
                    if line:
                        line_correction = self.correct_text(line, use_preprocessing=use_preprocessing)
                        container.append(line_correction)
            return container

        else:
            raise FileNotFoundError("Could not find the test file! Try using an absolute path perhaps!?")


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


    def load_corrector_resources(self, file_path: str):
        if pathlib.Path(file_path).exists():
            logging.debug("Loading the Jamspell model into memory! During first loads, this might take a while!")
            self.corrector.LoadLangModel(file_path)
            logging.debug("Finished the Jamspell model into memory!")
        else:
            raise FileNotFoundError("Could not find model with the path: {}!".format(file_path))


    def preprocess_text(self, original_text: str):
        logging.debug("Replacing the words in the text by the defined mappings from the file as a preprocessing step!")
        processed_text = original_text
        for mistake, correct in self.word_mapping:
            processed_text = processed_text.replace(mistake, correct)
        logging.debug("Finished replacing the words!")
        return processed_text


    def get_candidates_for_text(self, corrected_text: str):
        candidates = {}
        tokens = [token for token in corrected_text.split(" ")]
        for index, token in enumerate(tokens):
            if token not in candidates:
                candidates[token] = self.corrector.GetCandidates(tokens, index)
            else:
                candidates[token] += self.corrector.GetCandidates(tokens, index)
                candidates[token] = list(set(candidates[token]))
        return candidates


    def correct_text(self, original_text: str, use_preprocessing: bool = True):

        preocessed_text = self.preprocess_text(original_text) if use_preprocessing else original_text

        logging.debug("Applying the Jamspell model on the preprocessed text!")
        corrected_text = self.corrector.FixFragment(preocessed_text)
        logging.debug("Finished applying the Jamspell model, final result!")

        logging.debug("Getting the candidates.")
        candidates = self.get_candidates_for_text(corrected_text)
        logging.debug("Finished getting the candidates!")

        return Correction(original=original_text, correction=corrected_text, candidates=candidates)


if __name__ == '__main__':
    c = JamspellCorrector(correction_mapping_path="texts/training_texts/word_mapping.csv")
    correction = c.correct_text("Ma kaisin poes!")
    pass
