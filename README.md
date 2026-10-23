# Pu签到助手(目前值抓到报名的包，待完善)
## 项目简介
由于CCZU每月会发起5次PU活动，故产生此项目，仅供技术交流，如果使用请遵循学校及平台规定，产生一切后果与本人无关
## 项目结构
```text
Pu-EasySign/
├── config.py
├── main.py
├── README.md
└── requirements.txt
```
## 使用教程
1. 克隆本仓库
2. 安装依赖
```shell
pip install -r requirements.txt
```
3. 填写配置信息
```python
# config.py
PU_USERNAME = "学号"
PU_PASSWORD = "密码"
SID = 222766320254976   # 学校的sid，已经填写了CCZU的sid，其他学校可调用注释的代码来获取自己学校的sid
```
4. 运行
```shell
python main.py
```