import torch
import numpy as np
import pandas as pd
import functions as fn
from torch.utils.data import DataLoader
import models
import matplotlib.pyplot as plt

# System configuration
use_cuda = True
device = torch.device("cuda:0" if use_cuda and torch.cuda.is_available() else "cpu")
fn.set_seed(seed=2023, flag=True)

# Hyperparams and model settings
model_name = 'PAG100'
seq_l = 12
pre_l = 6
bs = 512
mode = 'complited'

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
# model = torch.load(f'./checkpoints/old_datasets_models/{model_name}_{pre_l}_bs{bs}_{mode}.pt')
model = torch.load(f'checkpoints\PAG100_6_bs512_completed.pt')
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
# result_df.to_csv(f'./results/{model_name}_{pre_l}bs{bs}_zone42.csv', encoding='gbk', index=False)

zone_42_capacity = inf['count'][42]
zone_42_label_raw = zone_42_label.ravel() * zone_42_capacity

df = pd.DataFrame({
    "Actual Occupancy": zone_42_label.ravel(),
    "Predicted Occupancy": zone_42_predict.ravel(),
    "zone_42_label_raw": zone_42_label_raw
})
# df.to_csv("occupancy_results.csv", index=False)

# 绘制预测值和实际值曲线图
plt.figure(figsize=(12, 6))
plt.plot(zone_42_label, label='Actual Values', color='blue', linewidth=2)
plt.plot(zone_42_predict, label='Predicted Values', color='red', linestyle='--', linewidth=2)
plt.title(f'Comparison of Actual and Predicted Values (Zone 42)\n{model_name} Model, Prediction Length={pre_l}')
plt.xlabel('Time Steps')
plt.ylabel('Occupancy Rate')
plt.legend()
plt.grid(True)

# plt.savefig(f'./results/plots_simplified/{model_name}_{pre_l}bs{bs}_zone42_plot.png', dpi=300, bbox_inches='tight')
plt.show()