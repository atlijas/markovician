# Markovician

Markovician is a tool that utilizes Markov chains, produced from any given
text file, to generate brand new sentences.

### Basic usage

```python
from markov import MarkovChain
Markov = MarkovChain(file = 'test_files/pride_tokenized.txt', n_chunks = 2)
generated_text = (Markov.format_sent())
print(generated_text)
```
The higher `n_chunks`, the more realistic the output (which also makes Markovician
likelier to produce an already existing sentence). This can be prevented by
comparing the generated sentence to existing sentences, as seen in [tester.py](tester.py).
