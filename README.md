# 激活码系统 API

这是一个基于 FastAPI 的激活码系统 API，用于生成、绑定、验证和管理应用程序的激活码。

## 功能特性

- 生成唯一的激活码
- 绑定激活码到特定应用
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
   git clone https://github.com/your-username/vd.git
   cd vd

2. 创建并激活虚拟环境：

source venv/bin/activate # On Windows use `venv\Scripts\activate`

3. 安装依赖：
   pip install -r requirements.txt

4. 配置环境变量：

DATABASE_URL=your_database_url
API_KEY=your_api_key

5. 运行应用：

uvicorn main:app --reload

## 使用

### 生成激活码

## API 文档

API 文档可以通过访问 `http://localhost:8000/docs` 查看。

## API 端点

- `POST /generate`: 生成新的激活码
- `POST /bind`: 绑定激活码到特定应用
- `POST /validate`: 验证激活码
- `POST /bulk_generate`: 批量生成激活码
- `POST /revoke`: 撤销激活码
- `GET /list_codes`: 获取激活码列表

### 生成激活码

```python
python
import requests
url = "http://localhost:8000/generate"
headers = {
"X-API-Key": "your_api_key_here"
}
data = {
"length": 16,
"expires_in_days": 30,
"max_uses": 1
}
response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### 绑定激活码

```python
import requests
url = "http://localhost:8000/bind"
headers = {
"X-API-Key": "your_api_key_here"
}
data = {
"activation_code": "your_activation_code_here",
"app_id": "your_app_id_here"
}
response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### 验证激活码

```python
import requests
url = "http://localhost:8000/validate"
headers = {
"X-API-Key": "your_api_key_here"
}
data = {
"activation_code": "your_activation_code_here",
"app_id": "your_app_id_here"
}
response = requests.post(url, json=data, headers=headers)
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
"app_id": "your_app_id_here",
"count": 10,
"expires_in_days": 30,
"max_uses": 1
}
response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### 撤销激活码

```python
    import requests
    url = "http://localhost:8000/revoke"
    headers = {
"X-API-Key": "your_api_key_here"
}
data = {
"activation_code": "your_activation_code_here"
}
response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### 撤销激活码

```python
import requests
url = "http://localhost:8000/revoke"
headers = {
"X-API-Key": "your_api_key_here"
}
data = {
"activation_code": "your_activation_code_here"
}
response = requests.post(url, json=data, headers=headers)
print(response.json())
```
### 获取激活码列表

```python
import requests
url = "http://localhost:8000/list_codes"
headers = {
"X-API-Key": "your_api_key_here"
}
response = requests.get(url, headers=headers)
print(response.json())  
```

## 注意事项

- 确保在生产环境中使用安全的 API 密钥和数据库连接字符串。
- 根据需要调整速率限制和其他安全设置。
- 定期备份数据库以防数据丢失。

## 贡献

欢迎提交 issues 和 pull requests 来改进这个项目。

## 许可

[MIT License](LICENSE)
