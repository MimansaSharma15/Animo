import torch 
from torch import nn as nn
from torch.nn import functional as f 
from score_data import main_data
from score_model import sentiment
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
import time

'''
Main file for training
the sentiment model
-->
Trains the model
for 7 epochs
 
'''


## DECLARATIONS
data = main_data()
vocab_size = data.vocab_size
model = sentiment(embed_size=100, num_layers=1, 
                  vocab_size=vocab_size, hidden_size=150)

writer = SummaryWriter(f"runs/tensor_board_loss")

train_dl = DataLoader(data,batch_size=10,shuffle=True)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

device = "cpu"

loss_fn = nn.CrossEntropyLoss()

def accuracy(pred, y):
    predictions = f.log_softmax(pred, dim=1)
    _,predictions = torch.max(predictions, dim=1)
    correct = (predictions==y).float()

    acc = correct.sum()/len(correct)

    return acc


def epoch_time(start_time, end_time):
    elapsed_time = end_time - start_time
    elapsed_mins = int(elapsed_time / 60)
    elapsed_secs = int(elapsed_time - (elapsed_mins * 60))
    return elapsed_mins, elapsed_secs


def train(model=model, train_dl=train_dl, optimizer=optimizer, loss_fn=loss_fn):
    epoch_loss = 0
    epoch_acc = 0
    step = 0
    model.train()

    for x, y in tqdm(train_dl,desc="Training",total=len(train_dl),leave=False):
        optimizer.zero_grad()
        out = model(x)
        
        loss = loss_fn(out,y)
        acc = accuracy(out,y)

        epoch_loss += loss.item()
        epoch_acc += acc.item()

        loss.backward()

        optimizer.step()
        
        writer.add_scalar("Training loss", loss.item(), global_step=step)
        step += 1    


    return epoch_loss/len(train_dl), epoch_acc/len(train_dl)

def evaluate(model=model,loss_fn=loss_fn,train_dl=train_dl):
    epoch_loss = 0
    epoch_acc = 0
    step = 0
    model.eval()

    with torch.no_grad():
        for x,y in tqdm(train_dl,leave=False,desc="Validation",total=len(train_dl)):
            x = x.to(device)
            y = y.to(device)
            out = model(x)
            
            loss = loss_fn(out,y)
            acc = accuracy(out,y)

            epoch_loss += loss.item()

            epoch_acc += acc.item()

            writer.add_scalar("Evaluate loss", loss.item(), global_step=step)
            step += 1

        return epoch_loss/len(train_dl), epoch_acc/len(train_dl)

n_epochs = 7
for epoch in range(n_epochs):
    start_time = time.time()
 
    train_loss,train_acc = train()
    eval_loss,eval_acc = evaluate()

    end_time = time.time()

    if train_acc*100>=90:
        print("Training stopped via call backs")
        break
    if eval_acc*100>=95:
        print("Training stopped via call backs")
        break

    epoch_mins, epoch_secs = epoch_time(start_time, end_time)
    print(f'Epoch: {epoch+1:02} | Epoch Time: {epoch_mins}m {epoch_secs}s')
    print(f'\tTrain Loss: {train_loss:.3f} | Train Acc: {train_acc*100:.2f}%')
    print(f'\t Val. Loss: {eval_loss:.3f} |  Val. Acc: {eval_acc*100:.2f}%')    
 
torch.save(model.state_dict(),"model_score.pt")
