# 使い方
## ログ
```
python velocity_logger.py --fname velocity_data.csv --save_dir log
```

## グラフ
**logscvとtime_shiftは同じ個数指定すること**
time_shiftはグラフ間の時間軸方向の合わせに使う、ずらさない場合は指定しなくて良い
```
python draw_vel_graph.py --save_dir fig --logcsv log/velocity_data.csv  log/velocity_data02.csv --time_shift 0 50
```