# http://norvig.com/mayzner.html

character_frequencies = {
    'a': 8.04,
    'c': 3.34,
    'b': 1.48,
    'e': 12.49,
    'd': 3.82,
    'g': 1.87,
    'f': 2.40,
    'i': 7.57,
    'h': 5.05,
    'k': 0.54,
    'j': 0.16,
    'm': 2.51,
    'l': 4.07,
    'o': 7.64,
    'n': 7.23,
    'q': 0.12,
    'p': 2.14,
    's': 6.51,
    'r': 6.28,
    'u': 2.73,
    't': 9.28,
    'w': 1.68,
    'v': 1.05,
    'y': 1.66,
    'x': 0.23,
    'z': 0.09,
    ' ': 19.19,
}

digram_frequencies = {
    'en': 1.45,
    'co': 0.79,
    've': 0.83,
    'ed': 1.17,
    'is': 1.13,
    'ea': 0.69,
    'al': 1.09,
    'ce': 0.65,
    'an': 1.99,
    'as': 0.87,
    'ar': 1.07,
    'at': 1.49,
    'io': 0.83,
    'in': 2.43,
    'ic': 0.70,
    'li': 0.62,
    'es': 1.34,
    'er': 2.05,
    'le': 0.83,
    're': 1.85,
    'll': 0.58,
    'nd': 1.35,
    'ne': 0.69,
    'ng': 0.95,
    'to': 1.04,
    'ra': 0.69,
    'th': 3.56,
    'ti': 1.34,
    'te': 1.20,
    'nt': 1.04,
    'ri': 0.73,
    'be': 0.58,
    'ur': 0.54,
    'ch': 0.60,
    'de': 0.76,
    'it': 1.12,
    'hi': 0.76,
    'ha': 0.93,
    'he': 3.07,
    'me': 0.79,
    'on': 1.76,
    'om': 0.55,
    'ro': 0.73,
    'ma': 0.57,
    'of': 1.17,
    'st': 1.05,
    'si': 0.55,
    'ou': 0.87,
    'or': 1.28,
    'se': 0.93,
}

word_frequencies = {
    'and': 3.04,
    'all': 0.28,
    'would': 0.20,
    'when': 0.20,
    'is': 1.13,
    'it': 0.77,
    'an': 0.37,
    'as': 0.77,
    'are': 0.50,
    'have': 0.37,
    'in': 2.27,
    'if': 0.21,
    'from': 0.47,
    'for': 0.88,
    'their': 0.29,
    'there': 0.22,
    'had': 0.35,
    'been': 0.22,
    'to': 2.60,
    'which': 0.42,
    'you': 0.31,
    'has': 0.22,
    'was': 0.74,
    'more': 0.21,
    'be': 0.65,
    'we': 0.28,
    'his': 0.49,
    'that': 1.08,
    'who': 0.20,
    'but': 0.38,
    'they': 0.33,
    'not': 0.61,
    'one': 0.29,
    'with': 0.70,
    'by': 0.63,
    'he': 0.55,
    'a': 2.06,
    'on': 0.62,
    'her': 0.22,
    'i': 0.52,
    'of': 4.16,
    'no': 0.19,
    'will': 0.20,
    'this': 0.51,
    'so': 0.19,
    'can': 0.22,
    'were': 0.31,
    'the': 7.14,
    'or': 0.49,
    'at': 0.46,
}


def score_single_characters(text):
    score = 0
    for test_char in text:
        current_char = test_char.lower()
        if current_char in character_frequencies:
            score += character_frequencies[current_char]
    return score


def score_digrams(text):
    score = 0
    for i in range(len(text)):
        current_digram = text[i:i+2].lower()
        if current_digram in digram_frequencies:
            score += digram_frequencies[current_digram]
    return score


def score_words(text):
    cleaned_text = ''.join([i.lower() for i in text if i in character_frequencies])
    score = 0
    words = cleaned_text.split()
    for w in words:
        if w in word_frequencies:
            score += word_frequencies[w]
    return score


def score_text(text):
    return sum([
        score_single_characters(text),
        score_digrams(text),
        score_words(text)
    ])
