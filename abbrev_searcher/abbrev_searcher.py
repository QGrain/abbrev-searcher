import argparse
import itertools
from nltk.corpus import words
from nltk.data import find
from nltk import download
from tqdm import tqdm
from googletrans import Translator
from concurrent.futures import ProcessPoolExecutor, as_completed

def check_and_download_nltk_data():
    """
    Checks if the 'words' corpus is available in nltk, and downloads it if not.
    """
    try:
        find('corpora/words.zip')
    except LookupError:
        download('words')

def is_valid_word(word):
    """
    Checks if a word is a valid English word.

    Args:
        word (str): The word to check.

    Returns:
        bool: True if the word is valid, False otherwise.
    """
    return word.lower() in words.words()

def generate_valid_words(sets):
    """
    Generates all valid English word combinations from the provided sets of letters.

    Args:
        sets (list of list of str): A list of lists, where each inner list contains possible letters for each position in the word.

    Returns:
        list of str: A list of valid English words formed by combining letters from each set in the provided order.
    """
    # Generate all possible combinations
    combinations = [''.join(item) for item in itertools.product(*sets)]

    # Use ProcessPoolExecutor to filter valid words concurrently
    with ProcessPoolExecutor() as executor:
        is_valid = list(tqdm(executor.map(is_valid_word, combinations), total=len(combinations)))
    
    return [combinations[i] for i in range(len(combinations)) if is_valid[i]]

def translate_to_chinese(word):
    """
    Translates a single English word to Chinese.

    Args:
        word (str): The English word to translate.

    Returns:
        tuple: The original word and its Chinese translation.
    """
    translator = Translator()
    translation = translator.translate(word, dest='zh-CN').text
    return word, translation

def create_letter_sets(original_words):
    """
    Creates letter sets for generating word combinations based on given words.

    Args:
        original_words (list of str): List of words to derive letter sets from.

    Returns:
        list of list of str: A list of lists, where each inner list contains possible letters for each position in the word.
    """
    letter_sets = []
    for word in original_words:
        unique_letters = set(word)
        letter_set = [letter for letter in unique_letters if letter.isupper()]
        if not letter_set:
            letter_set = unique_letters
        letter_sets.append(letter_set)
    return letter_sets

def format_group_name(original_words, word):
    """
    Formats a new group name by replacing letters in original words with corresponding letters in the given word.

    Args:
        original_words (list of str): The original list of words.
        word (str): The new word to format.

    Returns:
        str: The formatted group name.
    """
    assert len(original_words) == len(word)
    formatted_words = []
    for i in range(len(word)):
        original_word = original_words[i].lower()
        new_letter = word[i].upper()
        formatted_word = original_word.replace(word[i].lower(), new_letter, 1)
        formatted_words.append(formatted_word)
    return ' '.join(formatted_words)

if __name__ == "__main__":
    # Check and download nltk data
    check_and_download_nltk_data()

    parser = argparse.ArgumentParser('Automatically search the abbreviation for group name, version')
    parser.add_argument('-w', '--words', type=str, nargs='+', help='sperated words to be abbreviated, e.g. Software and SysTem security')
    args = parser.parse_args()

    # Define the original words
    original_words = args.words or ['HeRe', 'are', 'THe', 'Default', 'words']
    letter_sets = create_letter_sets(original_words)

    # Find valid word combinations
    print('[Searching valid combinations...]')
    valid_combinations = generate_valid_words(letter_sets)

    # Use ProcessPoolExecutor to translate words concurrently
    print('[Translating...]')
    translations = []
    with ProcessPoolExecutor() as executor:
        future_to_word = {executor.submit(translate_to_chinese, word): word for word in valid_combinations}
        for future in tqdm(as_completed(future_to_word), total=len(future_to_word)):
            word, translation = future.result()
            translations.append((word, translation))

    # Print valid words with their translations and formatted group names
    for word, translation in translations:
        print(f"{word} {translation} {format_group_name(original_words, word)}")
