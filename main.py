import json
import string


def get_character_occurrences(word_list: list):
    char_occ_dict = dict.fromkeys(string.ascii_lowercase, 0)  # creates dict of each letter for key and 0 for val
    for word in word_list:
        used_chars = set()
        for char in word:
            if char not in used_chars:
                used_chars.add(char)
                char_occ_dict[char] = char_occ_dict[char] + 1
            # Right now we don't handle repeat letters because it's complicated
    return char_occ_dict


def calc_next_word(word_list: list):
    char_occ_dict = get_character_occurrences(word_list)
    word_scores = dict.fromkeys(word_list, 0)
    for word in word_list:
        used_chars = set()
        for char in word:
            if char not in used_chars:
                used_chars.add(char)
                word_scores[word] = word_scores[word] + char_occ_dict[char]
            # Right now we don't handle repeat letters because it's complicated
    word_scores_reversed = list((value, key) for key, value in word_scores.items())
    return sorted(word_scores_reversed, reverse=True)[0][1]


def clean_word_list(word_list: list, spot_tuples: list, char_list: list, wrong_list: list):
    for wrong_char in wrong_list:
        word_list = [word for word in word_list if wrong_char not in word]
    for char, idx in spot_tuples:
        word_list = [word for word in word_list if char == word[idx]]
    for char, idx in char_list:
        word_list = [word for word in word_list if char in word and char != word[idx]]

    return word_list


if __name__ == '__main__':
    CORRECT_SPOT = 'g'
    CORRECT_LETTER = 'y'
    WRONG = 'w'
    MAX_GUESSES = 6
    current_guess = 1
    word_list = json.load(open('five-letter-words.json'))['words']
    word_list.sort()

    while current_guess <= MAX_GUESSES:
        next_word = calc_next_word(word_list)
        print(next_word)
        result_string = input()
        current_guess = current_guess + 1
        if result_string == "fin":
            exit()

        spot_tuples = list()
        char_tuples = list()
        wrong_list = list()
        for i in range(5):
            if result_string[i] == CORRECT_SPOT:
                spot_tuples.append((next_word[i], i))
            elif result_string[i] == CORRECT_LETTER:
                char_tuples.append((next_word[i], i))
            elif result_string[i] == WRONG:
                wrong_list.append(next_word[i])
            else:
                print(f"ERROR: YOU GAVE A LETTER I DON'T UNDERSTAND: {result_string[i]}")
        word_list = clean_word_list(word_list, spot_tuples, char_tuples, wrong_list)
