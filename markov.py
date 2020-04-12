from string import punctuation
from collections import Counter, defaultdict
import random
import re
import numpy
punctuation += '«»´'

class WordProcessor:
    def __init__(self, n=0, text=None, no_punct=True, chunks=False,
                 ngrams=False, linebreaks=False):
        self.n = n
        self.no_punct = no_punct
        self.linebreaks = linebreaks
        self.text = self.get_file(text).split()
        if chunks:
            self.chunks = [w for w in zip(*[iter(self.text)] * n)]
        if ngrams:
            self.ngrams = [w for w in self.gen_ngrams(n)]

    def get_file(self, file):
        with open(file, 'r', encoding='utf-8') as txt:
            if self.linebreaks:
                txt = txt.read()
            else:
                txt = txt.read().replace('\n', ' ')
            if self.no_punct:
                txt = txt.translate(str.maketrans('', '', punctuation))
        return txt

    def gen_ngrams(self, n):
        tokens = self.text
        for i in range(len(tokens)-n):
            yield tokens[i], tokens[i+1:i+n]

class MarkovChain:
    def __init__(self, file, n_chunks=0):
        self.n_chunks = n_chunks
        self.processed_words = WordProcessor(n=self.n_chunks, text=file,
                                             chunks=True, no_punct=False)
        self.word_list = defaultdict(Counter)
        self.inital_state = ''
        prev = self.inital_state

        for chunk in self.processed_words.chunks:
            sent_end = chunk[-1] in '.'

            if sent_end:
                chunk = chunk[:-1]
            self.word_list[prev].update([chunk])

            if sent_end:
                self.word_list[chunk].update([self.inital_state])
                prev = self.inital_state
            else:
                prev = chunk

        self.word_list = {key: (list(value.keys()), list(value.values()))
                          for key, value in self.word_list.items()}


    def get_next_state_random(self, state):
        return random.choices(*self.word_list[state])[0]

    def get_next_state(self, state):
        index = numpy.argmax(self.word_list[state][1])
        return self.word_list[state][0][index]

    def gen_sents(self):
        sentence = []
        current_state = self.inital_state
        beg_sent_counter = 0
        while beg_sent_counter <= 1:
            randomizer = 1
            if randomizer == 0:
                current_state = self.get_next_state(current_state)
                sentence.append(current_state)
            elif randomizer == 1:
                randomizer = random.sample([0, 1], 1)[0]
                current_state = self.get_next_state_random(current_state)
                sentence.append(current_state)
            if 'BEG_SENT' in current_state:
                beg_sent_counter += 1
        sentence = ' '.join([' '.join(tup) for tup in sentence]).split()
        return sentence

    def format_sent(self):
        sent = []
        sent_to_app = ''
        for element in self.gen_sents():
            if element != 'BEG_SENT':
                sent_to_app += element + ' '
            elif element == 'BEG_SENT':
                sent.append(sent_to_app)
                sent_to_app = ''
        sent = ' '.join(sent)
        if not sent.endswith(' . ') or not sent.endswith('.'):
            sent += '.'
        sent = re.sub(r'\s+([,?.!:“"])', r'\1', sent)
        sent = sent[1:-1]
        return sent


if __name__ == '__main__':
    pass
