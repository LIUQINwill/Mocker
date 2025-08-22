# 🎭 Mocker API Platform

一个强大的Mock API平台，用于开发和测试环境中快速创建和管理API模拟接口。

## ✨ 功能特性

### 🚀 核心功能
- **Mock接口管理**：支持创建、编辑、删除、启用/禁用Mock接口
- **多种HTTP方法**：支持GET、POST、PUT、DELETE、PATCH等HTTP方法
- **灵活响应配置**：支持静态响应、动态模板响应
- **请求日志记录**：详细记录所有Mock请求和响应信息
- **实时监控**：提供请求统计和性能分析

### 🎯 响应生成器
- **静态响应**：直接返回预设的JSON数据
- **模板响应**：使用Jinja2模板引擎生成动态响应
- **占位符支持**：支持时间、随机数据、请求参数等占位符
- **Faker集成**：内置Faker库生成随机测试数据

### 📊 监控统计
- **请求统计**：总请求数、今日请求数、成功率
- **性能分析**：平均响应时间、热门API统计
- **方法分布**：HTTP方法使用统计
- **状态码分析**：响应状态码分布统计

## 🏗️ 技术架构

### 后端技术栈
- **框架**：FastAPI (高性能异步Web框架)
- **数据库**：MySQL 8.0 + SQLAlchemy ORM
- **数据迁移**：Alembic
- **模板引擎**：Jinja2
- **数据生成**：Faker
- **API文档**：自动生成OpenAPI/Swagger文档

### 前端技术栈（规划中）
- **框架**：Vue.js 3 + TypeScript
- **构建工具**：Vite
- **UI组件**：Element Plus
- **状态管理**：Pinia
- **HTTP客户端**：Axios

### 部署方案
- **容器化**：Docker + Docker Compose
- **反向代理**：Nginx（规划中）
- **数据持久化**：MySQL数据卷

## 🚀 快速开始

### 环境要求
- Python 3.10+
- MySQL 8.0+
- Docker & Docker Compose（可选）

### 方式一：Docker部署（推荐）

1. **克隆项目**
```bash
git clone <repository-url>
cd Mocker
```

2. **启动服务**
```bash
docker-compose up -d
```

3. **访问服务**
- API文档：http://localhost:8000/api/v1/docs
- 健康检查：http://localhost:8000/health
- Mock服务：http://localhost:8000/mock/*

### 方式二：本地开发

1. **安装依赖**
```bash
cd backend
pip install -r requirements.txt
```

2. **配置数据库**
```bash
# 复制环境配置文件
cp ../.env.example .env

# 修改数据库连接信息
# DATABASE_URL=mysql+pymysql://root:password@localhost:3306/mocker
```

3. **初始化数据库**
```bash
# 创建数据库迁移
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

4. **启动服务**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📖 使用指南

### 创建Mock接口

通过API创建一个简单的Mock接口：

```bash
curl -X POST "http://localhost:8000/api/v1/mocks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "用户信息接口",
    "description": "获取用户基本信息",
    "method": "GET",
    "path": "/users/123",
    "status_code": 200,
    "response_body": {
      "id": 123,
      "name": "张三",
      "email": "zhangsan@example.com",
      "created_at": "{{now}}"
    }
  }'
```

### 使用Mock接口

创建成功后，可以直接访问Mock接口：

```bash
curl http://localhost:8000/mock/users/123
```

响应：
```json
{
  "id": 123,
  "name": "张三",
  "email": "zhangsan@example.com",
  "created_at": "2024-01-15T10:30:00"
}
```

### 模板响应示例

创建使用模板的动态响应：

```bash
curl -X POST "http://localhost:8000/api/v1/mocks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "动态用户接口",
    "method": "GET",
    "path": "/users/dynamic",
    "response_template": "{\"id\": {{fake.random_int(1, 1000)}}, \"name\": \"{{fake.name}}\", \"email\": \"{{fake.email}}\", \"timestamp\": \"{{now}}\"}"
  }'
```

每次请求都会返回不同的随机数据。

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `APP_NAME` | 应用名称 | Mocker API Platform |
| `DEBUG` | 调试模式 | true |
| `DATABASE_URL` | 数据库连接URL | mysql+pymysql://root:mocker123@localhost:3306/mocker |
| `API_V1_STR` | API版本前缀 | /api/v1 |
| `MOCK_PREFIX` | Mock服务前缀 | /mock |

### 响应模板语法

支持以下占位符和函数：

- `{{now}}` - 当前时间（ISO格式）
- `{{timestamp}}` - 当前时间戳
- `{{fake.name}}` - 随机姓名
- `{{fake.email}}` - 随机邮箱
- `{{fake.phone}}` - 随机电话
- `{{fake.address}}` - 随机地址
- `{{fake.company}}` - 随机公司名
- `{{fake.uuid}}` - 随机UUID
- `{{fake.number}}` - 随机数字
- `{{request.param_name}}` - 请求参数

## 📊 API文档

启动服务后，访问以下地址查看完整API文档：

- **Swagger UI**：http://localhost:8000/api/v1/docs
- **ReDoc**：http://localhost:8000/api/v1/redoc
- **OpenAPI JSON**：http://localhost:8000/api/v1/openapi.json

### 主要API端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/mocks` | GET | 获取Mock接口列表 |
| `/api/v1/mocks` | POST | 创建Mock接口 |
| `/api/v1/mocks/{id}` | GET | 获取Mock接口详情 |
| `/api/v1/mocks/{id}` | PUT | 更新Mock接口 |
| `/api/v1/mocks/{id}` | DELETE | 删除Mock接口 |
| `/api/v1/mocks/{id}/toggle` | POST | 切换Mock接口状态 |
| `/api/v1/logs` | GET | 获取请求日志 |
| `/api/v1/logs/stats/overview` | GET | 获取统计信息 |
| `/mock/*` | ANY | Mock代理服务 |

## 🧪 开发指南

### 项目结构

```
Mocker/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模式
│   │   ├── services/       # 业务逻辑
│   │   ├── utils/          # 工具函数
│   │   └── main.py         # 应用入口
│   ├── alembic/            # 数据库迁移
│   ├── requirements.txt    # Python依赖
│   └── Dockerfile          # Docker配置
├── frontend/               # 前端应用（规划中）
├── docker-compose.yml      # Docker编排
├── .env.example           # 环境配置示例
└── README.md              # 项目文档
```

### 添加新功能

1. **数据模型**：在 `backend/app/models/` 中定义新的SQLAlchemy模型
2. **Schema**：在 `backend/app/schemas/` 中定义Pydantic模式
3. **服务层**：在 `backend/app/services/` 中实现业务逻辑
4. **API路由**：在 `backend/app/api/v1/` 中添加新的路由
5. **数据迁移**：使用Alembic生成和执行数据库迁移

### 代码规范

- 使用Python类型提示
- 遵循PEP 8代码风格
- 编写详细的文档字符串
- 添加适当的错误处理
- 编写单元测试

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建功能分支：`git checkout -b feature/new-feature`
3. 提交更改：`git commit -am 'Add new feature'`
4. 推送分支：`git push origin feature/new-feature`
5. 提交Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢以下开源项目：

- [FastAPI](https://fastapi.tiangolo.com/) - 现代高性能Web框架
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL工具包
- [Alembic](https://alembic.sqlalchemy.org/) - 数据库迁移工具
- [Pydantic](https://pydantic-docs.helpmanual.io/) - 数据验证库
- [Jinja2](https://jinja.palletsprojects.com/) - 模板引擎
- [Faker](https://faker.readthedocs.io/) - 测试数据生成器