import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.data import Dataset

#remove this on gpu
# os.environ['KMP_DUPLICATE_LIB_OK']='True'
# set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# data_dir = '/Users/gogo/Downloads/DSC180b/hchs/actigraphy/'
# on cluster
data_dir = '/home/yuh365/teams/DSC180B_WI22_A00/b11group2/actigraphy'

# hyperparameters
input_size = 4
# train the model with 12 hour sequence, could also use 3 hour/4 hour/1day/1.5 hour
sequence_length = 720 * 60 // 30
num_classes = 4
num_layers = 2
hidden_size = 256
learning_rate = 0.0003
batch_size = 1
num_epoch = 10
log_dir = '../../logs'
log_file_dir = os.path.join('../../logs', datetime.now().strftime('%Y-%m-%d-%H%M%S') + '.txt')


# digest data
class HCHS(Dataset):
    activity_idx = 4
    wl_idx = 6
    rl_idx = 7
    bl_idx = 8
    gl_idx = 9
    y_idx = 11
    y_encode = {'EXCLUD': 3, 'ACTIVE': 2, 'REST-S': 1, 'REST': 0}

    def __init__(self, filenames):
        self.batch_size = batch_size
        self.filenames = filenames

    def __getitem__(self, idx):
        # file_idx = idx * sequence_length // 17280
        file = self.filenames[idx]
        file = os.path.join(data_dir, file)
        temp = pd.read_csv(open(file, 'r')).dropna()
        X = temp.iloc[:, 6:10].values.astype(np.float32)
        y = temp.iloc[:, 11].apply(lambda x: HCHS.y_encode[x]).values.astype(np.float32)
        # X = temp.iloc[idx * sequence_length : (idx + 1) * sequence_length, 6:10].values
        # y = temp.iloc[idx * sequence_length:(idx + 1) * sequence_length, 11].apply(lambda x: HCHS.y_encode[x]).values
        return (X, y)

    def __len__(self):
        return len(self.filenames)


def prepare_dataset():
    files = os.listdir(data_dir)
    # test
#     train_set = HCHS(files[0:5])
#     val_set = HCHS(files[1280:1285])
#     test_set = HCHS(files[1600:1602])
    # train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    # val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=True)
    # test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=True)

    # gpu
    train_set = HCHS(files[0:1280])
    val_set = HCHS(files[1280:1600])
    test_set = HCHS(files[1600:])
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=True, num_workers=1,
                            pin_memory=True)
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=True)
    return train_loader, val_loader, test_loader


# RNN model
class RNN(nn.Module):
    def __init__(self):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.rnn = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        out, _ = self.rnn(x)
        out = self.fc(out)
        return self.softmax(out)


# metric
def is_quality_sleep(lst):
    sleep = torch.sum(lst == 1)
    in_bed = torch.sum(lst == 0)
    sleep_efficiency = sleep / (sleep + in_bed)
    return sleep_efficiency > 0.9


# train
def train(train_loader, val_loader):
    model = RNN().to(device).float()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    avg_train_loss = []
    avg_val_loss = []
    train_loss_lst = []
    val_loss_lst = []
    best_val_score = float('inf')
    for e in range(num_epoch):
        print(f'start epoch {e}')
        for i, (X, y) in enumerate(train_loader):
            print(i)
            if X.numel() == 0:
                continue
            X = X.to(device)
            y = y.long().to(device)

            output = model(X.float())
            # print('fc_out')
            # print(output.shape)
            # print('reshape out and y')
            # print(output.reshape(-1, output.shape[2]).shape)
            # print(y.reshape(-1).shape)
            loss = criterion(output.reshape(-1, output.shape[2]), y.reshape(-1))

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            avg_train_loss.append(loss.detach().item())


        # train_acc = evaluate(train_loader, model, device)
        # avg_train_acc.append(train_acc)
        # print('train loss:{0}, train accuracy{1}'.format(tl_item, train_acc))
        # print(avg_train_loss)
        train_loss = np.mean(avg_train_loss)
        train_loss_lst.append(train_loss)
        print('train loss:{0}'.format(train_loss))

        total = 0
        correct = 0
        with torch.no_grad():
            b = 0
            for X, y in val_loader:
                b += 1
                X, y = X.to(device), y.long().to(device)
                output = model(X.float())

                # predictions = torch.argmax(output.data, 1)
                # total += y.shape[0]
                # correct += torch.sum(predictions == y)

                loss = criterion(output.reshape(-1, output.shape[2]), y.reshape(-1))
                avg_val_loss.append(loss.detach().item())

        # val_acc = float(correct) / float(total)
        # avg_val_acc.append(val_acc)
        # print('validation loss:{0}, validation accuracy{1}'.format(vl_item, val_acc))
        val_loss = np.mean(avg_val_loss)
        val_loss_lst.append(val_loss)
        print('validation loss:{0}'.format(val_loss))

        with open(log_file_dir, 'a') as f:
            f.write('epoch:%d\n' % (e + 1))
            # f.write('train loss:{0}, train accuracy{1}\n'.format(tl_item, train_acc))
            # f.write('validation loss:{0}, validation accuracy{1}\n'.format(vl_item, val_acc))
            f.write('train loss:{0}, '.format(train_loss))
            f.write('validation loss:{0}\n'.format(val_loss))
        # end epochs for early stop
        if val_loss < best_val_score:
            best_val_score = val_loss
            torch.save(model.state_dict(), os.path.join(log_dir, 'best_rnn_model.pt'))

    ix = np.arange(len(train_loss_lst))
    # change this for keeping scale
    plt.ylim(0, 2)

    plt.plot(ix, train_loss_lst, label="training loss")
    plt.plot(ix, val_loss_lst, label="validation loss")
    plt.title('loss graph')
    plt.legend()
    plt.savefig(os.path.join(log_dir,"rnn_loss.png"))
    plt.clf()

    # ix = np.arange(len(avg_train_acc))
    # # change this for keeping scale
    # plt.ylim(0.5, 1)
    # plt.plot(ix, avg_train_acc, label="training accuracy")
    # plt.plot(ix, avg_val_acc, label="validation accuracy")
    # plt.title('accuracy graph')
    # plt.legend()
    # plt.savefig("acc.png")
    # plt.show()
    # plt.clf()

    model.load_state_dict(torch.load(os.path.join(log_dir, 'best_rnn_model.pt')))

    return model


def test(model, test_loader):
    acc_lst = []
    cla_acc_lst = []
    with torch.no_grad():
        for X,y in test_loader:
            X,y = X.to(device), y.long().to(device)
            pred = model(X.float()).argmax(2)
            acc = np.mean((pred ==y).squeeze().detach().cpu().numpy())
            # print(np.mean(is_quality_sleep(y).detach().cpu().numpy()))
            cla_acc = is_quality_sleep(pred) == is_quality_sleep(y)
            acc_lst.append(acc)
            cla_acc_lst.append(cla_acc.cpu())
    avg_acc = np.mean(acc_lst)
    avg_cla_acc = np.mean(cla_acc_lst)
    print('test prediction acc:{0}'.format(avg_acc))
    print('test classification acc:{0}'.format(avg_cla_acc))
    with open(log_file_dir, 'a') as f:
        f.write('test prediction acc:{0}'.format(avg_acc))
        f.write('test classification acc:{0}'.format(avg_cla_acc))


def run(): 
    train_loader, val_loader, test_loader = prepare_dataset()
    model = train(train_loader, val_loader)
    test(model, test_loader)


if __name__ == '__main__':
    # run
    if len(sys.argv) > 1:
        train_loader, val_loader, test_loader = prepare_dataset()
        model = RNN().to(device)
        model.load_state_dict(torch.load(os.path.join(log_dir, 'best_rnn_model.pt')))
        test(model, test_loader)
    else:
        run()
