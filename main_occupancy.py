import torch
import numpy as np
import pandas as pd
import functions as fn
from torch.utils.data import DataLoader
import models

# System configuration
use_cuda = True
device = torch.device("cuda:0" if use_cuda and torch.cuda.is_available() else "cpu")
fn.set_seed(seed=2023, flag=True)

# Hyperparams and model settings
model_name = 'LSTM'
seq_l = 12
pre_l = 3
bs = 512
mode = 'completed'

# Load data
occ, prc, adj, col, dis, cap, time, inf = fn.read_dataset()
adj_dense = torch.Tensor(adj)
adj_sparse = adj_dense.to_sparse_coo().to(device)

# Split data
_, _, test_occupancy = fn.division(occ, train_rate=0.6, valid_rate=0.2, test_rate=0.2)
_, _, test_price = fn.division(prc, train_rate=0.6, valid_rate=0.2, test_rate=0.2)

# Only use occupancy for test dataset
test_dataset = fn.CreateDataset(test_occupancy, test_price, seq_l, pre_l, device, adj_dense)
test_loader = DataLoader(test_dataset, batch_size=len(test_occupancy), shuffle=False)

# Load trained model
model = torch.load(f'./checkpoints/{model_name}_{pre_l}_bs{bs}_{mode}.pt')
model.eval()

predict_list = np.zeros([1, adj_dense.shape[1]])
label_list = np.zeros([1, adj_dense.shape[1]])

for data in test_loader:
    occupancy, price, label = data  # Keep price for CreateDataset compatibility
    with torch.no_grad():
        predict = model(occupancy, price)
        predict = predict.cpu().detach().numpy()
        label = label.cpu().detach().numpy()
        predict_list = np.concatenate((predict_list, predict), axis=0)
        label_list = np.concatenate((label_list, label), axis=0)

# Only evaluate for zone 42
zone_42_predict = predict_list[1:, 42:43]
zone_42_label = label_list[1:, 42:43]
output_zone_42 = fn.metrics(test_pre=zone_42_predict, test_real=zone_42_label)
result_df = pd.DataFrame([output_zone_42], columns=['MSE', 'RMSE', 'MAPE', 'RAE', 'MAE', 'R2'])
result_df.to_csv(f'./results/{model_name}_{pre_l}bs{bs}_zone42.csv', encoding='gbk', index=False)