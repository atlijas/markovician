from nltk.tokenize import sent_tokenize

def get_file(file):
    with open(file, 'r', encoding='utf-8') as infile:
        infile = infile.read()
    return infile

file_string = get_file('test_files/pride.txt')
tokenized = sent_tokenize(file_string)

with open('filename.txt', 'w', encoding='utf-8') as file:
    for i in tokenized:
        file.write('BEG_SENT ' + i + '\n')
