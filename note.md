https://colab.research.google.com/drive/1FaFP-yG27fI4499IaKe2hooaarfoXU0I#scrollTo=gJOFq3gHnnwA

RMSE | MAPE | RAE | MAE

有 VAR LSTM GCN GAT GCN-LSTM STGCN

无 Lasso KNN FCNN DCRNN AST-GAT

## PAG_6bs512 
```python
model_name = 'PAG' 
mode = 'completed'
seq_l = 12  # lookback  60min
pre_l = 6  # predict_time
```

pre_l 30 min
```
Pre-training: 100% 200/200 [12:06<00:00,  3.63s/it]
Fine-tuning: 100% 1000/1000 [24:01<00:00,  1.44s/it]
occupancy: torch.Size([1710, 247, 12]) price: torch.Size([1710, 247, 12]) label: torch.Size([1710, 247])
MAPE: 0.13165747601233665   13.17
MAE:0.02269172655174996     2.27
MSE:0.0019193848987534919   0.20
RMSE:0.04381078518759384    4.38
R2:0.8287269705618396
RAE:0.16270310294658774     16.27
```


## PAG
```python
model_name = 'PAG' 
mode = 'simplified'
seq_l = 12  # lookback  60min
pre_l = 6  # predict_time
```

## LSTM
```python
model_name = 'LSTM'
seq_l = 12
pre_l = 6
bs = 512
```

```
Pre-training:   0% 0/200 [00:00<?, ?it/s]/content/ST-EVCDP/learner.py:37: FutureWarning: You are using `torch.load` with `weights_only=False` (the current default value), which uses the default pickle module implicitly. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling (See https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models for more details). In a future release, the default value for `weights_only` will be flipped to `True`. This limits the functions that could be executed during unpickling. Arbitrary objects will no longer be allowed to be loaded via this mode unless they are explicitly allowlisted by the user via `torch.serialization.add_safe_globals`. We recommend you start setting `weights_only=True` for any use case where you don't have full control of the loaded file. Please open an issue on GitHub for any issues related to this experimental feature.
  temp_model = torch.load('./checkpoints' + '/meta_' + model_name + '_' + str(pre_l) + '_bs' + str(bs) + 'model.pt').to(device)
Pre-training: 100% 200/200 [14:05<00:00,  4.23s/it]
Fine-tuning: 100% 1000/1000 [20:35<00:00,  1.24s/it]
/content/ST-EVCDP/main.py:99: FutureWarning: You are using `torch.load` with `weights_only=False` (the current default value), which uses the default pickle module implicitly. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling (See https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models for more details). In a future release, the default value for `weights_only` will be flipped to `True`. This limits the functions that could be executed during unpickling. Arbitrary objects will no longer be allowed to be loaded via this mode unless they are explicitly allowlisted by the user via `torch.serialization.add_safe_globals`. We recommend you start setting `weights_only=True` for any use case where you don't have full control of the loaded file. Please open an issue on GitHub for any issues related to this experimental feature.
  model = torch.load('./checkpoints' + '/' + model_name + '_' + str(pre_l) + '_bs' + str(bs) + '_' + mode + '.pt')
occupancy: torch.Size([1710, 247, 12]) price: torch.Size([1710, 247, 12]) label: torch.Size([1710, 247])
MAPE: 0.4682727878862736   46.8
MAE:0.06083133624522273    6.08
MSE:0.00743108298071689    0.74
RMSE:0.08620372950584498   8.62
R2:0.0948750810238791  
RAE:0.4361698586889454     43.62
```

