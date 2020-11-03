from torch import nn as nn
from torch.nn import functional as f 
import torch 

'''
Model for
Giving best recommendations

'''


class sentiment(nn.Module):
    def __init__( self, embed_size, num_layers, vocab_size, hidden_size ):
        super(sentiment, self).__init__()
        self.embed_size = embed_size
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size

        self.emebd = nn.Embedding(self.vocab_size, self.embed_size)
        self.gru = nn.GRU(self.embed_size, self.hidden_size, num_layers=1, bidirectional=True, batch_first=True)
        self.fc1 = nn.Linear(in_features=15000, out_features=6)
        self.drop = nn.Dropout()
        self.flat = nn.Flatten()        # self.norm = nn.BatchNorm1d()

    def forward(self,input):
        out = self.drop(self.emebd(input))

        out, _ = self.gru(out)
        flat_out = self.fc1(self.flat(out))

        return flat_out
