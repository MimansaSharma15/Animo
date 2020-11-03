import torch
from torch.utils.data import Dataset
import pandas as pd 
import numpy as np 
from  tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

'''
processed_data is the csv file
containing questions and answers

-->
DF is created using this csv file
tensorflow.keras.preprocessing is used to tokenize 
and pad the sentences

-->
__getitem__() is  used by the dataloader to extract src & trg

'''


class main_data(Dataset):
    def __init__(self):
        super(main_data,self).__init__()
        self.df = pd.read_csv("/home/aradhya/Desktop/NLP/hack_iiit new/data/processed_faqs.csv")
        self.questions = self.df['Questions']
        self.answers = self.df['Answers']
        self.token()

    def token(self):
        self.tok_enc = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n')
        self.tok_enc.fit_on_texts(self.questions)
        self.questions = self.tok_enc.texts_to_sequences(self.questions)
        
        self.tok_dec = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n')
        self.tok_dec.fit_on_texts(self.answers)
        self.answers = self.tok_dec.texts_to_sequences(self.answers)


        self.questions = pad_sequences(self.questions,maxlen=100,padding='pre')
        self.answers = pad_sequences(self.answers,maxlen=100,padding='pre')
        
        self.src, self.trg = torch.tensor(self.questions,dtype=torch.long), torch.tensor(self.answers,dtype=torch.long)

    def len_all(self):
        return  len(self.src[0]), len(self.tok_enc.word_index), len(self.tok_dec.word_index) 

    def __len__(self):
        return len(self.src)

    def __getitem__(self,xid):
        return self.src[xid], self.trg[xid]


    