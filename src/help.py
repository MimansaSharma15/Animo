from score_model import sentiment
from score_data import main_data
from torch import nn as nn
import torch
from torch.nn import functional as f
from tensorflow.keras.preprocessing.sequence import pad_sequences


'''
Analysis Of the text 
entered by the user
--->

Returns user score

'''

data = main_data()
vocab_size = data.vocab_size
tok = data.tok

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



class health_analysis(sentiment):
    def __init__(self,sent):
        super(health_analysis, self).__init__(embed_size=100, num_layers=1, vocab_size=vocab_size, hidden_size=150)
        self.model = sentiment(embed_size=100, num_layers=1, vocab_size=vocab_size, hidden_size=150)
        self.model.load_state_dict(torch.load("/home/aradhya/Desktop/hacks/model_score.pt"))
        self.model.eval()
        self.seq = tok.texts_to_sequences(sent)
        self.seq = torch.tensor(pad_sequences(self.seq, maxlen=50,padding='pre'),dtype=torch.long)

        self.model_result()     

    def model_result(self):
        self.analysis_lst = []
        _,predcition = torch.max(f.log_softmax(self.model(self.seq),dim=1),dim=1)
        self.analysis_lst.append(predcition.item())
    
    def recommend(self):
        
        for i in self.analysis_lst:
            if i == 4 or i==0 or i==1:
                return True
        return False

#         if predcition == 0:
#             return 'sadness'
# # 
#         if predcition == 1:
#             return "anger"
# # 
#         if predcition == 2:
#             return "love"
#         # 
#         if predcition == 3:
#             return "surprise"
# # 
#         if predcition == 4:
#             return "fear"
# # 
#         if predcition == 5:
#             return "joy"
# # 



