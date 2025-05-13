https://colab.research.google.com/drive/1FaFP-yG27fI4499IaKe2hooaarfoXU0I#scrollTo=gJOFq3gHnnwA

RMSE | MAPE | RAE | MAE

PAG_6bs512 
```python
model_name = 'PAG' 
mode = 'completed'
seq_l = 12  # lookback  60min
pre_l = 6  # predict_time
```

pre_l 30 min

Pre-training: 100% 200/200 [12:06<00:00,  3.63s/it]
Fine-tuning: 100% 1000/1000 [24:01<00:00,  1.44s/it]
occupancy: torch.Size([1710, 247, 12]) price: torch.Size([1710, 247, 12]) label: torch.Size([1710, 247])
MAPE: 0.13165747601233665   13.17
MAE:0.02269172655174996     2.27
MSE:0.0019193848987534919   0.20
RMSE:0.04381078518759384    4.38
R2:0.8287269705618396
RAE:0.16270310294658774     16.27




