# abbrev-seacher
A tool to search valid letter combinations for a given sentence, which can be used as the abbreviation.

## Installation

- Get it
```bash
# from Github
git clone https://github.com/QGrain/abbrev-searcher.git

# from PyPI
# current not supported
pip install abbrev-searcher
```

- Dependencies
```bash
pip install -r requirements.txt
```

## Usage

```bash
# abbrev_searcher would take the upper letters as candidates first
# if there is no upper letter in the word, it would take every lower letter as candidates.
cd abbrev_searcher
python abbrev_searcher.py -w The words tO be AbbreViated
```

## Contribution

Feel free to raise Issues and PRs.