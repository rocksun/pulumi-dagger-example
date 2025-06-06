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

## Install Pulumi

```py
# Linux
curl -fsSL https://get.pulumi.com | sh
```

## Install Docker

..

## Install Dagger

...

## Install AWS CLI

Install AWS CLI:

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

## Config AWS CLI ENV:

Create .env file with content:

```
AWS_ACCESS_KEY_ID="你的AWS访问密钥ID"
AWS_SECRET_ACCESS_KEY="你的AWS秘密访问密钥"
AWS_ACCESS_KEY_IDWS_DEFAULT_REGION="ap-southeast-1"
```

## Init Project

Add dependenies:

```
uv add dagger-io pulumi pulumi-aws anyio
```

## 注意

如果依然有权限问题，需要设置：

```
此账户的“屏蔽公共访问权限”设置
```