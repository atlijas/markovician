from markov import MarkovChain
from difflib import SequenceMatcher
from nltk import sent_tokenize


def get_file(file):
    with open(file, 'r', encoding='utf-8') as infile:
        infile = infile.read()
    return sent_tokenize(infile)

Markov = MarkovChain(file = 'test_files/pride_tokenized.txt', n_chunks = 3)
all_sentences = get_file('test_files/pride_tokenized.txt')

if __name__ == '__main__':
    for i in range(20):
        all_similarities = []
        try:
            my_text = (Markov.format_sent())
            my_text_beg = 'BEG_SENT ' + my_text
            for sentence in all_sentences:
                similarity = SequenceMatcher(None, my_text_beg, sentence).ratio()
                all_similarities.append(similarity)
            if not any(s > 0.8 for s in all_similarities):
                print(my_text)
        except KeyError:
            pass
