import copy
import baselines
import torch
import numpy as np
import pandas as pd
import functions as fn
from torch.utils.data import DataLoader
from tqdm import tqdm
import models
import learner

# system configuration
use_cuda = True
device = torch.device("cuda:0" if use_cuda and torch.cuda.is_available() else "cpu")
fn.set_seed(seed=2023, flag=True)

# hyper params
model_name = 'PAG'
seq_l = 12  # lookback  60min
pre_l = 12  # predict_time 3 6 9 12
bs = 512  # batch size 
p_epoch = 200
n_epoch = 1000
# can directly affect the model's evaluation metrics,
law_list = np.array([-1.48, -0.74])  # price elasticities of demand for EV charging. Recommend: up to 5 elements.
is_train = False
mode = 'completed'  # 'simplified' or 'completed'
is_pre_train = True

# input data
occ, prc, adj, col, dis, cap, time, inf = fn.read_dataset()
adj_dense = torch.Tensor(adj)
adj_dense_cuda = adj_dense.to(device)  # move a tensor to a specific device
adj_sparse = adj_dense.to_sparse_coo().to(device)

# dataset division
train_occupancy, valid_occupancy, test_occupancy = fn.division(occ, train_rate=0.6, valid_rate=0.2, test_rate=0.2)
train_price, valid_price, test_price = fn.division(prc, train_rate=0.6, valid_rate=0.2, test_rate=0.2)

# data
train_dataset = fn.CreateDataset(train_occupancy, train_price, seq_l, pre_l, device, adj_dense)
train_loader = DataLoader(train_dataset, batch_size=bs, shuffle=True, drop_last=True)
valid_dataset = fn.CreateDataset(valid_occupancy, valid_price, seq_l, pre_l, device, adj_dense)
valid_loader = DataLoader(valid_dataset, batch_size=len(valid_occupancy), shuffle=False)
test_dataset = fn.CreateDataset(test_occupancy, test_price, seq_l, pre_l, device, adj_dense)
test_loader = DataLoader(test_dataset, batch_size=len(test_occupancy), shuffle=False)

# training setting
model = models.PAG(a_sparse=adj_sparse).to(device)  # init model
# model = FGN().to(device)

# model = baselines.LSTM(seq_l, 2).to(device)
# model = baselines.LstmGcn(seq_l, 2, adj_dense_cuda).to(device)
# model = baselines.VAR(node=247, seq=seq_l, feature=2).to(device)
# model = baselines.GCN(seq_l, 2, adj_dense_cuda).to(device)
# model = baselines.LstmGat(seq_l, 2, adj_dense_cuda, adj_sparse).to(device)
# model = baselines.TPA(seq_l, 2).to(device)
# model = baselines.HSTGCN(seq_l, 2, adj_dense_cuda, adj_dense_cuda).to(device)
# model = baselines.FGN(pre_length=1, seq_length=seq_l).to(device)


optimizer = torch.optim.Adam(model.parameters(), weight_decay=0.00001)
loss_function = torch.nn.MSELoss()
valid_loss = 100

if is_train is True:
    model.train()
    if is_pre_train is True:
        if mode == 'simplified':  # a simplified way of physics-informed meta-learning
            model = learner.fast_learning(law_list, model, model_name, p_epoch, bs, train_occupancy, train_price, seq_l, pre_l, device, adj_dense)

        elif mode == 'completed': # the completed process
            model = learner.physics_informed_meta_learning(law_list, model, model_name, p_epoch, bs, train_occupancy, train_price, seq_l, pre_l, device, adj_dense)
        else:
            print("Mode error, skip the pre-training process.")

    for epoch in tqdm(range(n_epoch), desc='Fine-tuning'):
        for j, data in enumerate(train_loader):
            '''
            occupancy = (batch, seq, node)
            price = (batch, seq, node)
            label = (batch, node)
            '''
            model.train()
            occupancy, price, label = data

            optimizer.zero_grad()
            predict = model(occupancy, price)
            loss = loss_function(predict, label)
            loss.backward()
            optimizer.step()

        # validation
        model.eval()
        for j, data in enumerate(valid_loader):
            '''
            occupancy = (batch, seq, node)
            price = (batch, seq, node)
            label = (batch, node)
            '''
            model.train()
            occupancy, price, label = data
            predict = model(occupancy, price)
            loss = loss_function(predict, label)
            if loss.item() < valid_loss:
                valid_loss = loss.item()
                torch.save(model, './checkpoints' + '/' + model_name + '_' + str(pre_l) + '_bs' + str(bs) + '_' + mode + '.pt')

model = torch.load('./checkpoints' + model_name + '_' + str(pre_l) + '_bs' + str(bs) + '_' + mode + '.pt')

# model = torch.load('checkpoints\PAG_6_bs512_simplified.pt')

# test
model.eval()
result_list = []
predict_list = np.zeros([1, adj_dense.shape[1]])
label_list = np.zeros([1, adj_dense.shape[1]])
for j, data in enumerate(test_loader):
    occupancy, price, label = data  # occupancy.shape = [batch, seq, node]
    print('occupancy:', occupancy.shape, 'price:', price.shape, 'label:', label.shape)
    with torch.no_grad():
        predict = model(occupancy, price)
        predict = predict.cpu().detach().numpy()
        label = label.cpu().detach().numpy()
        predict_list = np.concatenate((predict_list, predict), axis=0)
        label_list = np.concatenate((label_list, label), axis=0)

# Modified evaluation for zone 42 only
zone_42_predict = predict_list[1:, 42:43]  # Select only zone 42
zone_42_label = label_list[1:, 42:43]      # Select only zone 42
output_zone_42 = fn.metrics(test_pre=zone_42_predict, test_real=zone_42_label)
result_list.append(output_zone_42)
result_df = pd.DataFrame(columns=['MSE', 'RMSE', 'MAPE', 'RAE', 'MAE', 'R2'], data=result_list)
# result_df.to_csv('./results' + '/' + model_name + '_' + str(pre_l) + 'bs' + str(bs) + '_zone42.csv', encoding='gbk')

# output_no_noise = fn.metrics(test_pre=predict_list[1:, :], test_real=label_list[1:, :])
# result_list.append(output_no_noise)
# result_df = pd.DataFrame(columns=['MSE', 'RMSE', 'MAPE', 'RAE', 'MAE', 'R2'], data=result_list)
# result_df.to_csv('./results' + '/' + model_name + '_' + str(pre_l) + 'bs' + str(bs) + '.csv', encoding='gbk')

# 绘制预测值和实际值曲线图
plt.figure(figsize=(12, 6))
plt.plot(label_list[1:, 42:43], label='Actual Values', color='blue', linewidth=2)
plt.plot(predict_list[1:, 42:43], label='Predicted Values', color='red', linestyle='--', linewidth=2)
plt.title(f'Comparison of Actual and Predicted Values (Zone 42)\n{model_name} Model, Prediction Length={pre_l}')
plt.xlabel('Time Steps')
plt.ylabel('Occupancy Rate')
plt.legend()
plt.grid(True)

# plt.savefig(f'./results/plots_all_zones/{model_name}_{pre_l}bs{bs}_zone42_plot.png', dpi=300, bbox_inches='tight')
plt.show()