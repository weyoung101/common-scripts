### venv为每个项目建立虚拟环境

1. 安装venv

```shell
pip install virtualenv
```

2. 建立与激活虚拟环境

```shell
python -m venv venv
source venv/bin/activate
```

### 常用命令记录

#### 生成 requirements.txt

```shell
pip freeze > requirements.txt
```

#### 安装依赖

```shell
pip install -r requirements.txt
```

### 打包成可执行文件

#### 安装PyInstaller
```shell
pip install pyinstaller
```

#### 使用PyInstaller打包程序
其中，`your_program.py`是你的Python程序的文件名。`--onefile`选项表示将程序打包成一个可执行文件。这个命令会生成一个dist目录，里面包含了打包后的可执行文件。
```shell
pyinstaller --onefile your_program.py
```