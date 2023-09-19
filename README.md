### venv为每个项目建立虚拟环境

1. 安装venv

```shell
pip install virtualenv
```

2. 建立与激活虚拟环境

```
python -m venv venv
source venv/bin/activate
```

### 常用命令记录

#### 生成 requirements.txt

`pip freeze > requirements.txt`

#### 安装依赖

`pip install -r requirements.txt`

