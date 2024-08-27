import json
import random

# Kelime listesini JSON dosyasından yükleme
def load_words():
    with open("dictionary.json", "r", encoding="utf-8") as file:
        return json.load(file)

# Kelimeleri global bir değişkende saklama
words = load_words()

# Rastgele bir kelime seçme
def get_random_word():
    return random.choice(words)

# Rastgele bir kelimenin doğru cevabını ve yanlış cevap seçeneklerini alma
def get_quiz_options(correct_word):
    correct_answer = correct_word['translations'][0]
    wrong_answers = random.sample(
        [word['translations'][0] for word in words if word['word'] != correct_word['word']], 
        3
    )
    options = wrong_answers + [correct_answer]
    random.shuffle(options)

    return options
