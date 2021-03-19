# 摆脱烦人的傻逼北温打



一个小北温度打卡自动脚本



# 如何使用

首先在 config.py 中写入你的身份证号和密码（默认为身份证号后六位）

注意不要去掉双引号

```python
username = "100000199801020022"
password = "020022"

```

在完成后，它应该像上面这样

# 运行

```bash
pip3 install requests
# 安装依赖
python3 main.py
# 执行
```

如果想自动执行的话，就把`python3 + main.py的绝对位置`加入crontab 当中就 ok 了