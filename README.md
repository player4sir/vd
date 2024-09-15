# 激活码系统 API

这是一个基于 FastAPI 的激活码系统 API，用于生成、验证和管理应用程序的激活码。

## 功能特性

- 生成唯一的激活码
- 验证激活码
- 批量生成激活码
- 撤销激活码
- 支持激活码过期
- 支持使用次数限制
- API 密钥认证
- 速率限制

## 技术栈

- Python 3.7+
- FastAPI
- PostgreSQL
- asyncpg

## 安装

1. 克隆仓库：

git clone https://github.com/your-username/activation-code-system.git cd activation-code-system

2. 创建并激活虚拟环境：

python -m venv venv source venv/bin/activate # On Windows use venv\Scripts\activate

3. 安装依赖：

pip install -r requirements.txt

4. 配置环境变量：

DATABASE_URL=your_database_url API_KEY=your_api_key

5. 运行应用：

uvicorn main:app --reload

## API 文档

API 文档可以通过访问 `http://localhost:8000/docs` 查看。

## 示例请求

请确保将上述内容替换为您的实际数据库 URL 和 API 密钥。

## 运行应用

运行以下命令启动应用：

uvicorn main:app --reload

应用将在 `http://localhost:8000` 上运行。

## API 端点

- `POST /generate`: 生成新的激活码
- `POST /validate`: 验证激活码
- `POST /bulk_generate`: 批量生成激活码
- `POST /revoke`: 撤销激活码

详细的 API 文档可以在运行应用后访问 `http://localhost:8000/docs` 查看。

## 使用示例

### 生成激活码

```python
import requests

url = "http://localhost:8000/generate"
headers = {
    "X-API-Key": "your_api_key_here"
}
data = {
    "app_id": "your_app_id",
    "length": 16,
    "expires_in_days": 30,
    "max_uses": 1
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### 验证激活码

```python
import requests

url = "http://localhost:8000/validate"
data = {
    "activation_code": "your_activation_code",
    "app_id": "your_app_id"
}

response = requests.post(url, json=data)
print(response.json())
```

### 批量生成激活码

```python
import requests

url = "http://localhost:8000/bulk_generate"
headers = {
    "X-API-Key": "your_api_key_here"
}
data = {
    "app_id": "your_app_id",
    "count": 10,
    "expires_in_days": 30,
    "max_uses": 100
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### 撤销激活码

```python
import requests 

url = "http://localhost:8000/revoke"
data = {
    "activation_code": "your_activation_code"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
``` 

