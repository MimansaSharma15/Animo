import torch 
from torch import nn as nn 
from torch.nn import functional as f 
from data import main_data
from torch.utils.data import DataLoader
from models import Encoder, Decoder
import random
import time 
from tqdm import tqdm
from models import Seq2Seq, Encoder, Decoder
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

'''

MAIN FILE TO TRAIN THE
seq2seq MODEL
-->
IMPORTING THE PREVIOUSLY CREATED MODEL 
-->
SETTING A TRAINING LOOP

'''


device = "cpu"
bs = 3
teacher_forcing_ratio = 0.5

data = main_data()
max, vocab_enc, vocab_dec = data.len_all()

train_loader = DataLoader(data,batch_size=bs)
encoder_net = Encoder(vocab_enc, 150, 200, 1, 0.3).to("cpu")
decoder_net = Decoder(vocab_dec,150,200,vocab_dec,1,0.3,).to("cpu")

model = Seq2Seq(encoder_net, decoder_net,vocab_dec)

optimizer = torch.optim.Adam(model.parameters(),lr=0.001)
criterion = nn.CrossEntropyLoss()

writer = SummaryWriter(f"runs/tensor_board_loss")
step = 0

def save_checkpoint(state, filename="my_checkpoint.pth.tar"):
    print("Saving.. ")
    torch.save(state, filename)


num_epochs = 50
save_model = True
load_model = False

for epoch in range(num_epochs):
    print(f"[Epoch {epoch} / {num_epochs}]")

    if save_model:
        checkpoint = {
            "state_dict": model.state_dict(),
            "optimizer": optimizer.state_dict(),
        }
        save_checkpoint(checkpoint) 

    model.train()

    for batch_idx, batch in tqdm(enumerate(train_loader),total=len(train_loader),desc="Training"):
        inp_data, target = batch

        try:
            output = model(inp_data, target)
        except:
            break

        
        output = output[1:].reshape(-1, output.shape[2])
        target = target[1:].reshape(-1)
        optimizer.zero_grad()
        loss = criterion(output, target)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1)

        optimizer.step()

        # Plot to tensorboard
        writer.add_scalar("Training loss", loss.item(), global_step=step)
        step += 1    

torch.save(model.state_dict(),"model_for_faq.pt")
