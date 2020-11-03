from nltk.corpus import stopwords
from torch.utils.data import Dataset
import torch 
import pandas as pd 
import numpy as np 
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

'''
This file loads in the
sentiment data
-->
preprocesses that data 
for the neural network
adn prepares for batching

'''


class main_data(Dataset):
    def __init__(self):
        super(main_data,self).__init__()
        self.df = pd.read_csv('Hack_IIIT/data/processed_sent.csv')
        self.text = np.array(self.df['Text'])
        self.label = np.array(self.df['Label'])
        self.text = [x for x in self.text if x not in stopwords.words('english')]
        self.token()

    def token(self):
        self.tok = Tokenizer(num_words=10000,
                            filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                            lower=True)
        self.tok.fit_on_texts(self.text)
        self.vocab_size = len(self.tok.word_index)

        self.xs = self.tok.texts_to_sequences(self.text)

        self.xs = pad_sequences(self.xs, maxlen=50, padding='pre')

        self.xs, self.ys =  torch.tensor(self.xs, dtype=torch.long), torch.tensor(self.label)

    def __len__(self):
        return len(self.df)
    
    def __getitem__(self,xid):
        return self.xs[xid], self.ys[xid]







