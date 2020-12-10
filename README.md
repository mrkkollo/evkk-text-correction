# Installation

* Run ```conda env install -f environment.yaml``` to create the Python environment.


# Usage
NOTE: Make sure that the required resources are either in their folders or specified in the constructor of the corrector.
Details about the required resources will be in the "Correctors" section of this documentation.

* Run ```conda activate evkk``` to activate the Python environment in your terminal.
* Create an object from the corrector you wish to use and then call out it's .correct_text() function, 
* .correct_text() will return an instance of the Correction class.

# Correctors
All correctors include the option to apply preprocessing with the use_preprocessing argument (by default True).
As of 12.11.2020 this only includes replacing common word mistakes that are predefined in a .csv file.

## Jamspell Corrector

### Required Resources
* Binary JamSpell model, by default: "models/estonski.bin"
* CSV file containing common mistakes and their corrections which will be replaced before applying the model. By default at: "texts/training_texts/word_mapping.csv"

### Description

Uses the Peter Norvig algorithm with 3-grams along with memory optimization processes to avoid Out-Of-Memory errors.
Works by loading the trained model file into memory. For training you need a corpus of grammatically correct text (plain text format)
and a text file containing the alphabet of the language in question (training itself is not supported in this project).

If you wish to use model binaries that exist outside of the repository, you MUST add the path of the model binary and word mapping CSV file
to the corrector as arguments.

```python
from correctors.jamspell.corrector import JamspellCorrector
corrector = JamspellCorrector(model_path='models/estonski.bin', correction_mapping_path="texts/training_texts/word_mapping.csv")
correction = corrector.correct_text("Ma kaisin poes!", use_preprocessing=True)

print(correction.corrected_tokens)
print(correction.correction)
print(correction.original)
```

## Peter Norvig Ngram + EstNLTK Corrector

### Required Resources
* CSV file containing common mistakes and their corrections which will be replaced before applying the model. By default at: "texts/training_texts/word_mapping.csv"
* Reference corpus of grammatically correct text in plain-text format with each instance of text separated by a new line.

### Description

Uses the EstNLTK spelling correction as a basis, applies the Peter Norvig algorithm along with simple Ngram matching
to tokens that EstNLTK fails to match properly (returns multiple candidates). 

If using the correctors outside of the repository, you MUST add the paths to the model binary and word mapping CSV file
to the corrector.

```python
from correctors.norvig_ngram_estnltk.corrector import PeterNorvigNgramCorrector
corrector = PeterNorvigNgramCorrector(corpus_path='some/path/corpus.txt', correction_mapping_path="texts/training_texts/word_mapping.csv")
correction = corrector.correct_text("Ma kaisin poes!", use_preprocessing=True)

print(correction.corrected_tokens)
print(correction.correction)
print(correction.original)
```