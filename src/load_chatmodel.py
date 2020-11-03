import torch 
from torch.nn import functional as f 
from torch import nn 
from models import Encoder, Decoder
from data import main_data

data = main_data()
max, vocab_enc, vocab_dec = data.len_all()

class Encoder(nn.Module):
    def __init__(self, input_size, embedding_size, hidden_size, num_layers, p):
        super(Encoder, self).__init__()
        self.dropout = nn.Dropout(p)
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.embedding = nn.Embedding(input_size, embedding_size)
        self.rnn = nn.LSTM(embedding_size, hidden_size, num_layers, dropout=p)

    def forward(self, x):
        # x shape: (seq_length, N) where N is batch size

        embedding = self.dropout(self.embedding(x))
        # embedding shape: (seq_length, N, embedding_size)

        outputs, (hidden, cell) = self.rnn(embedding)
        # outputs shape: (seq_length, N, hidden_size)

        return hidden, cell


class Decoder(nn.Module):
    def __init__(
        self, input_size, embedding_size, hidden_size, output_size, num_layers, p
    ):
        super(Decoder, self).__init__()
        self.dropout = nn.Dropout(p)
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.embedding = nn.Embedding(input_size, embedding_size)
        self.rnn = nn.LSTM(embedding_size, hidden_size, num_layers, dropout=p)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x, hidden, cell):
        
        x = x.unsqueeze(0)

        embedding = self.dropout(self.embedding(x))
        outputs, (hidden, cell) = self.rnn(embedding, (hidden, cell))
        predictions = self.fc(outputs)
        predictions = predictions.squeeze(0)

        return predictions, hidden, cell

def load():

    encoder_net = Encoder(vocab_enc, 150, 200, 1, 0.3).to("cpu")
    decoder_net = Decoder(vocab_dec,150,200,vocab_dec,1,0.3,).to("cpu")
    encoder_net.state_dict(torch.load("/home/aradhya/Desktop/hacks/model_for_faq_encoder.pt"))
    decoder_net.state_dict(torch.load("/home/aradhya/Desktop/hacks/model_for_faq_decoder.pt"))

    return encoder_net, decoder_net

