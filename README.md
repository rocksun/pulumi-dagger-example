# Pulumi and Dagger Example

Use python with Pulumi and Dagger on AWS.

## Install Python and UV

在 Amazon Linux 2023 上安装 Python 和 UV:

1. 更新系统包并安装 Python:

```bash
sudo dnf update -y
sudo dnf install python3.12 python3.12-pip -y

# 首先添加 alternatives 配置
sudo alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
sudo alternatives --install /usr/bin/python python /usr/bin/python3.12 1

# 然后设置为默认版本
sudo alternatives --set python3 /usr/bin/python3.12
sudo alternatives --set python /usr/bin/python3.12
```

2. 验证 Python 安装:

```bash
python3 --version
pip3 --version
```

3. 安装 UV (使用 pip):
```bash
# 首先安装 pipx
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# 使用 pipx 安装 uv
pipx install uv

# 验证安装
uv --version
```

注意：执行完安装命令后，可能需要重新打开终端或运行 `source ~/.bashrc` 使环境变量生效。

## Init Project