# Installation

* Run ```conda env create -f environment.yaml``` to create the Python environment.
* In case of gcc errors when installing jamspell, make sure you have gcc and g++ installed on your system, for Debian ```sudo apt update && sudo apt install gcc g++``` is sufficient.

# Usage
NOTE: Make sure that the required resources are either in their folders or specified in the constructor of the corrector.
Details about the required resources will be in the "Correctors" section of this documentation.

* Run ```conda activate evkk``` to activate the Python environment in your terminal.
* Create an object from the corrector you wish to use and then call out it's .correct_text() function, 
* .correct_text() will return an instance of the Correction class.


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