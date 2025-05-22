# 图

## old data



## new data








# old
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
MAPE: 0.4682727878862736   46.8
MAE:0.06083133624522273    6.08
MSE:0.00743108298071689    0.74
RMSE:0.08620372950584498   8.62
R2:0.0948750810238791  
RAE:0.4361698586889454     43.62
```

## VAR
```python
seq_l = 12
pre_l = 6
bs = 512
```
```
MAPE: 0.40690659516789074  40.7
MAE:0.05923768872932746    5.92
MSE:0.006351147416426651   6.35
RMSE:0.07969408645832293   7.97
R2:-0.02223890559664575   
RAE:0.4247431655614768     42.47
```

## gcn
```
Pre-training:   0%|                                                                                  | 0/200 [00:00<?, ?it/s]
Traceback (most recent call last):
  File "D:\_________________________PythonProject\ST-EVCDP\main_gcn.py", line 74, in <module>
    model = learner.physics_informed_meta_learning(law_list, model, model_name, p_epoch, bs, train_occupancy, train_price, seq_l, pre_l, device, adj_dense)
  File "D:\_________________________PythonProject\ST-EVCDP\learner.py", line 52, in physics_informed_meta_learning
    predict = temp_model(occupancy, mix_prc)
  File "D:\Python\Python\Python310\lib\site-packages\torch\nn\modules\module.py", line 1511, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "D:\Python\Python\Python310\lib\site-packages\torch\nn\modules\module.py", line 1520, in _call_impl
    return forward_call(*args, **kwargs)
  File "D:\_________________________PythonProject\ST-EVCDP\baselines.py", line 66, in forward
    x = self.gcn_l1(x)
  File "D:\Python\Python\Python310\lib\site-packages\torch\nn\modules\module.py", line 1511, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "D:\Python\Python\Python310\lib\site-packages\torch\nn\modules\module.py", line 1520, in _call_impl
    return forward_call(*args, **kwargs)
  File "D:\Python\Python\Python310\lib\site-packages\torch\nn\modules\linear.py", line 116, in forward
    return F.linear(input, self.weight, self.bias)
RuntimeError: mat1 and mat2 shapes cannot be multiplied (1391104x1 and 11x11)
```