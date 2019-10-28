# YSU_netLogin
燕山大学校园网认证脚本

# 说明
此脚本目的用于为校园网内远程设备认证上网

# V1.0
重写[OYCN](https://github.com/OYCN)的认证脚本

# 支持功能

## 网络认证

服务器提供商:
0.校园网 
1.中国移动 
2.中国联通 
3.中国电信

```python3 
python3 main.py 学号 密码 服务提供商编号(默认0.校园网)
```

## 用户下线

会自动获取目前已登录用户信息，将其下线

```python3
python3 main.py logout
```

# 感谢
[OYCN](https://github.com/OYCN)
