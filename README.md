# 🎭 Mocker API Platform

一个现代化的Mock API平台，提供完整的Web界面和强大的API服务，用于开发和测试环境中快速创建和管理API模拟接口。

## ✨ 功能特性

### 🚀 核心功能
- **📱 现代化Web界面**：基于Vue 3的响应式前端界面
- **🔧 Mock接口管理**：完整的增删改查功能，支持启用/禁用状态管理
- **🌐 多种HTTP方法**：全面支持GET、POST、PUT、DELETE、PATCH等HTTP方法
- **📝 灵活响应配置**：支持静态JSON响应和动态模板响应
- **📋 分类管理系统**：树形分类结构，支持移动和批量管理
- **📊 实时监控面板**：提供详细的请求统计和性能分析

### 🎯 智能响应生成器
- **静态响应**：直接返回预设的JSON数据，支持复杂数据结构
- **动态模板**：使用Jinja2模板引擎生成动态响应内容
- **丰富占位符**：内置时间、随机数据、请求参数等多种占位符
- **Faker数据生成**：集成Faker库，支持生成各种类型的测试数据
- **参数绑定**：支持从请求参数中提取数据用于响应生成


## 🏗️ 技术架构

### 🖥️ 前端技术栈
- **框架**：Vue 3.4+ + TypeScript 5.0+（组合式API）
- **构建工具**：Vite 5.0+（快速热重载）
- **UI框架**：TailwindCSS 3.3+ + Headless UI（无样式组件库）
- **图标库**：Heroicons（精美SVG图标）
- **图表组件**：Chart.js + Vue-ChartJS（数据可视化）
- **HTTP客户端**：Axios 1.6+（请求拦截和响应处理）
- **时间处理**：date-fns 3.0+（轻量级日期处理）
- **代码编辑器**：Monaco Editor（VS Code同款编辑器）

### ⚡ 后端技术栈
- **框架**：FastAPI 0.104+（高性能异步Web框架）
- **数据库**：MySQL 8.0 + SQLAlchemy 2.0 ORM
- **数据迁移**：Alembic 1.12+（版本化数据库迁移）
- **模板引擎**：Jinja2 3.1+（动态响应模板）
- **数据生成**：Faker 20.0+（测试数据生成）
- **包管理**：uv（超快Python包管理器）
- **API文档**：自动生成OpenAPI/Swagger文档

### 🚀 部署架构
- **容器化**：Docker + Docker Compose（多环境支持）
- **反向代理**：Nginx（静态文件服务 + API代理）
- **数据持久化**：MySQL数据卷 + Redis缓存
- **环境管理**：开发/生产双环境配置
- **自动化工具**：Makefile + Shell脚本（一键部署）

## 🚀 快速开始

### 📋 环境要求
- **Docker & Docker Compose**: 20.10+ & 2.0+（推荐方式）
- **Node.js**: 18+ (前端开发)
- **Python**: 3.10+ (后端开发)
- **MySQL**: 8.0+ (本地开发可选)

### 🐳 方式一：Docker部署（推荐）

**一键启动完整服务**：
```bash
# 克隆项目
git clone <repository-url>
cd Mocker

# 开发环境（支持热重载）
make dev

# 或生产环境（优化构建）
make prod
```

**验证部署**：
- 🌐 前端界面：http://localhost:3000 (开发) 或 http://localhost (生产)
- 🔌 后端API：http://localhost:8000
- 📚 API文档：http://localhost:8000/api/v1/docs
- 💚 健康检查：http://localhost:8000/health

### 💻 方式二：本地开发

**后端启动**：
```bash
cd backend
# 使用uv（推荐）
uv sync
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或使用pip
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**前端启动**：
```bash
cd frontend
npm install
npm run dev
```

**数据库配置**：
```bash
# 复制环境配置
cp .env.example .env

# 修改数据库连接（.env文件中）
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/mocker

# 执行数据库迁移
cd backend
uv run alembic upgrade head
```

## 📖 使用指南

### 🖱️ Web界面操作

**访问管理界面**：
启动服务后，访问 http://localhost:3000 (开发环境) 进入管理界面。

**主要功能模块**：
1. **📊 仪表盘**：查看实时统计数据和系统概览
2. **📝 Mock管理**：创建、编辑、删除Mock接口
3. **📂 分类管理**：组织和管理接口分类
4. **📋 日志查看**：查看详细的请求日志和统计信息

### 🔧 创建Mock接口

**方式1：通过Web界面**
1. 进入"Mock管理"页面
2. 点击"新建接口"按钮
3. 填写接口信息：名称、HTTP方法、路径、响应内容
4. 选择所属分类
5. 保存并启用接口

**方式2：通过API创建**
```bash
curl -X POST "http://localhost:8000/api/v1/mocks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "用户信息接口",
    "description": "获取用户基本信息",
    "method": "GET",
    "path": "/api/users/123",
    "status_code": 200,
    "response_body": {
      "id": 123,
      "name": "张三",
      "email": "zhangsan@example.com",
      "created_at": "{{now}}"
    },
    "category_id": 1
  }'
```

### 🌐 使用Mock接口

创建成功后，可以直接访问Mock接口：

```bash
curl http://localhost:8000/mock/api/users/123
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

### 📂 分类管理

**创建分类**：
```bash
curl -X POST "http://localhost:8000/api/v1/categories" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "用户管理",
    "description": "用户相关API接口",
    "parent_id": null
  }'
```

**树形结构**：
- 支持多级分类嵌套
- 移动分类位置
- 批量移动接口到不同分类

### ⚡ 动态模板示例

创建使用模板的动态响应：

```bash
curl -X POST "http://localhost:8000/api/v1/mocks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "动态用户接口",
    "method": "GET",
    "path": "/api/users/random",
    "response_template": "{\"id\": {{fake.random_int(1, 1000)}}, \"name\": \"{{fake.name}}\", \"email\": \"{{fake.email}}\", \"phone\": \"{{fake.phone_number}}\", \"address\": \"{{fake.address}}\", \"company\": \"{{fake.company}}\", \"timestamp\": \"{{now}}\"}"
  }'
```

**支持的模板变量**：
- `{{now}}` - 当前时间（ISO格式）
- `{{timestamp}}` - 当前时间戳
- `{{fake.name}}` - 随机姓名
- `{{fake.email}}` - 随机邮箱
- `{{fake.phone_number}}` - 随机电话
- `{{fake.address}}` - 随机地址
- `{{fake.company}}` - 随机公司名
- `{{fake.uuid}}` - 随机UUID
- `{{request.query_params.参数名}}` - 获取URL查询参数
- `{{request.path_params.参数名}}` - 获取路径参数

## 📊 项目结构

```
Mocker/
├── 📁 frontend/                 # 前端应用
│   ├── 📁 src/
│   │   ├── 📁 components/       # Vue组件
│   │   │   ├── 📁 Layout/       # 布局组件
│   │   │   ├── 📁 CategoryModal/ # 分类管理模态框
│   │   │   ├── 📁 CategoryTree/  # 分类树组件
│   │   │   ├── 📁 MockEditor/    # Mock接口编辑器
│   │   │   ├── 📁 LogViewer/     # 日志查看组件
│   │   │   └── 📁 Toast/         # 通知提示组件
│   │   ├── 📁 views/            # 页面组件
│   │   ├── 📁 composables/      # 组合式API逻辑
│   │   ├── 📁 api/              # API接口封装
│   │   ├── 📁 types/            # TypeScript类型定义
│   │   └── 📁 utils/            # 工具函数
│   ├── 📄 package.json          # 前端依赖配置
│   ├── 📄 vite.config.ts        # Vite构建配置
│   ├── 📄 tailwind.config.js    # TailwindCSS配置
│   └── 🐳 Dockerfile            # 前端Docker配置
├── 📁 backend/                  # 后端应用
│   ├── 📁 app/
│   │   ├── 📁 api/              # API路由层
│   │   │   └── 📁 v1/           # API版本控制
│   │   │       ├── 📄 mocks.py     # Mock接口管理
│   │   │       ├── 📄 categories.py # 分类管理
│   │   │       ├── 📄 dashboard.py  # 仪表盘统计
│   │   │       ├── 📄 logs.py       # 日志管理
│   │   │       └── 📄 proxy.py      # Mock代理服务
│   │   ├── 📁 core/             # 核心配置
│   │   ├── 📁 models/           # 数据模型（SQLAlchemy）
│   │   ├── 📁 schemas/          # Pydantic数据验证
│   │   ├── 📁 services/         # 业务逻辑层
│   │   └── 📁 utils/            # 工具模块
│   ├── 📁 alembic/              # 数据库迁移
│   ├── 📄 requirements.txt      # Python依赖
│   ├── 📄 pyproject.toml        # uv项目配置
│   └── 🐳 Dockerfile            # 后端Docker配置
├── 🐳 docker-compose.yml        # 生产环境编排
├── 🐳 docker-compose.dev.yml    # 开发环境编排
├── 📄 Makefile                  # 自动化构建脚本
├── 📁 scripts/                  # 部署脚本
│   ├── 📄 quick-deploy.sh       # 快速部署脚本
│   └── 📄 check-deployment.sh   # 部署验证脚本
├── 📄 .env.example             # 环境变量模板
├── 📄 README.md                # 项目说明文档
├── 📄 ARCHITECTURE.md          # 架构设计文档
└── 📄 DOCKER_DEPLOYMENT.md     # Docker部署指南
```

## 🔧 配置说明

### 🔐 环境变量

主要配置项说明（`.env`文件）：

| 变量名 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `DATABASE_URL` | 数据库连接URL | - | mysql+pymysql://root:password@mysql:3306/mocker |
| `DEBUG` | 调试模式 | false | true/false |
| `SECRET_KEY` | 应用密钥 | - | your-secret-key-here |
| `API_V1_STR` | API版本前缀 | /api/v1 | /api/v1 |
| `MOCK_PREFIX` | Mock服务前缀 | /mock | /mock |
| `BACKEND_CORS_ORIGINS` | 跨域允许源 | [] | ["http://localhost:3000"] |

## 📚 API文档

启动服务后，访问以下地址查看完整API文档：

- **📖 Swagger UI**：http://localhost:8000/api/v1/docs （交互式API文档）
- **📋 ReDoc**：http://localhost:8000/api/v1/redoc （美观的文档界面）
- **🔗 OpenAPI JSON**：http://localhost:8000/api/v1/openapi.json （API规范文件）

### 🔌 主要API端点

| 分类 | 端点 | 方法 | 说明 |
|------|------|------|------|
| **Mock管理** | `/api/v1/mocks` | GET | 获取Mock接口列表（支持分页、筛选） |
| | `/api/v1/mocks` | POST | 创建新的Mock接口 |
| | `/api/v1/mocks/{id}` | GET | 获取单个Mock接口详情 |
| | `/api/v1/mocks/{id}` | PUT | 更新Mock接口信息 |
| | `/api/v1/mocks/{id}` | DELETE | 删除Mock接口 |
| | `/api/v1/mocks/{id}/toggle` | POST | 切换Mock接口启用/禁用状态 |
| **分类管理** | `/api/v1/categories` | GET | 获取分类树结构 |
| | `/api/v1/categories` | POST | 创建新分类 |
| | `/api/v1/categories/{id}` | PUT | 更新分类信息 |
| | `/api/v1/categories/{id}` | DELETE | 删除分类（级联删除子分类） |
| **统计面板** | `/api/v1/dashboard/overview` | GET | 获取系统概览统计数据 |
| | `/api/v1/dashboard/trends` | GET | 获取请求趋势数据 |
| **日志管理** | `/api/v1/logs` | GET | 获取请求日志（支持分页、筛选） |
| | `/api/v1/logs/stats/overview` | GET | 获取日志统计信息 |
| **Mock服务** | `/mock/*` | ANY | Mock API代理服务（实际Mock响应） |

### 🛠️ 常用操作命令

使用Makefile简化操作（推荐）：

```bash
# 🚀 部署相关
make dev              # 启动开发环境
make prod             # 启动生产环境
make down             # 停止所有服务
make restart          # 重启服务

# 📊 监控相关  
make logs             # 查看所有服务日志
make logs-backend     # 查看后端日志
make logs-frontend    # 查看前端日志
make ps               # 查看容器状态
make health           # 健康检查

# 🗄️ 数据库相关
make db-migrate       # 执行数据库迁移
make db-reset         # 重置数据库
make backup           # 备份数据库
make restore          # 恢复数据库

# 🧹 清理相关
make clean            # 清理容器和镜像
make clean-logs       # 清理日志文件
```

## 🧪 开发指南

### 🏗️ 添加新功能

1. **📦 后端功能开发**：
   ```bash
   cd backend
   # 创建数据模型
   # app/models/new_model.py
   
   # 创建Pydantic Schema
   # app/schemas/new_schema.py
   
   # 实现业务逻辑
   # app/services/new_service.py
   
   # 添加API路由
   # app/api/v1/new_routes.py
   
   # 生成数据库迁移
   uv run alembic revision --autogenerate -m "Add new feature"
   uv run alembic upgrade head
   ```

2. **🎨 前端功能开发**：
   ```bash
   cd frontend
   # 创建组件
   # src/components/NewFeature/NewComponent.vue
   
   # 添加API接口
   # src/api/newApi.ts
   
   # 创建组合式API
   # src/composables/useNewFeature.ts
   
   # 添加路由
   # src/router/index.ts
   
   # 创建页面
   # src/views/NewFeaturePage.vue
   ```

### 📝 代码规范

**Python后端**：
- 使用Python类型提示
- 遵循PEP 8代码风格
- 编写详细的文档字符串
- 使用异步/等待模式处理IO操作
- 添加适当的错误处理和日志记录

**TypeScript前端**：
- 使用严格的TypeScript配置
- 遵循Vue 3组合式API模式
- 使用TailwindCSS进行样式设计
- 组件化开发，保持单一职责原则
- 合理使用组合式函数复用逻辑

### 🧪 测试指南

```bash
# 后端测试（规划中）
cd backend
pytest tests/

# 前端测试（规划中）  
cd frontend
npm run test

# 端到端测试（规划中）
npm run test:e2e
```

### 🔧 调试技巧

1. **后端调试**：
   - 使用FastAPI自动生成的交互式文档进行API测试
   - 查看详细的日志输出：`make logs-backend`
   - 使用Python调试器进行断点调试

2. **前端调试**：
   - 利用Vue Devtools浏览器扩展
   - 使用Vite的热重载功能快速迭代
   - 查看浏览器开发者工具的控制台和网络面板

## 🤝 贡献指南

我们欢迎社区贡献！请遵循以下步骤：

### 📋 贡献流程

1. **🍴 Fork项目**
   ```bash
   # 在GitHub上Fork项目到你的账户
   git clone https://github.com/your-username/Mocker.git
   cd Mocker
   ```

2. **🌿 创建功能分支**
   ```bash
   git checkout -b feature/amazing-new-feature
   ```

3. **💻 进行开发**
   - 遵循现有的代码风格和项目结构
   - 添加必要的测试用例
   - 更新相关文档

4. **✅ 提交更改**
   ```bash
   git add .
   git commit -m "feat: add amazing new feature
   
   - 添加了新功能X
   - 修复了问题Y  
   - 更新了文档Z"
   ```

5. **🚀 推送并创建PR**
   ```bash
   git push origin feature/amazing-new-feature
   # 然后在GitHub上创建Pull Request
   ```

### 📋 贡献指南

- **🐛 Bug报告**：详细描述问题重现步骤和环境信息
- **💡 功能建议**：清楚描述新功能的用途和实现思路
- **📖 文档改进**：修正错误、补充示例、改善可读性
- **🧪 测试用例**：为现有功能添加更多测试覆盖
- **🎨 UI/UX改进**：提升用户界面和交互体验

### ✅ 提交规范

使用[约定式提交](https://www.conventionalcommits.org/zh-hans/)格式：

- `feat:` 新功能
- `fix:` 修复bug
- `docs:` 仅文档更改
- `style:` 不影响代码含义的更改（空格、格式化等）
- `refactor:` 既不修复bug也不添加功能的代码更改
- `perf:` 改善性能的代码更改
- `test:` 添加缺失的测试或修正现有的测试
- `chore:` 对构建过程或辅助工具和库的更改

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🚀 项目状态

- **✅ 后端服务**：完整的FastAPI服务，支持Mock API管理
- **✅ 前端界面**：现代化Vue 3界面，支持完整功能操作
- **✅ Docker部署**：完整的容器化部署方案
- **✅ 分类管理**：树形分类结构，支持拖拽操作
- **✅ 日志系统**：详细的请求日志和统计分析
- **✅ 响应模板**：动态模板系统，支持Faker数据生成
- **🔄 持续改进**：功能持续优化和性能提升

## 🌟 特色亮点

1. **🎨 现代化界面**：基于Vue 3 + TailwindCSS的美观响应式界面
2. **⚡ 高性能**：FastAPI异步架构，支持高并发请求处理
3. **🐳 一键部署**：完整Docker化，支持开发/生产双环境
4. **🔧 智能模板**：内置Faker库，支持丰富的动态数据生成
5. **📊 实时监控**：完整的统计面板和请求日志分析
6. **🌳 分类管理**：直观的树形分类结构，便于接口组织
7. **💻 开发友好**：热重载开发环境，完整的API文档

## 🙏 致谢

感谢以下优秀的开源项目：

### 🖥️ 前端技术栈
- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [Vite](https://vitejs.dev/) - 下一代前端构建工具
- [TailwindCSS](https://tailwindcss.com/) - 实用优先的CSS框架
- [Headless UI](https://headlessui.com/) - 无样式可访问组件
- [Heroicons](https://heroicons.com/) - 精美的SVG图标库
- [Chart.js](https://www.chartjs.org/) - 简洁的HTML5图表库

### ⚡ 后端技术栈
- [FastAPI](https://fastapi.tiangolo.com/) - 现代高性能Web框架
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL工具包和ORM
- [Alembic](https://alembic.sqlalchemy.org/) - 轻量级数据库迁移工具
- [Pydantic](https://pydantic-docs.helpmanual.io/) - 数据验证和设置管理
- [Jinja2](https://jinja.palletsprojects.com/) - 现代且设计师友好的模板引擎
- [Faker](https://faker.readthedocs.io/) - 生成虚假数据的Python库

### 🛠️ 开发工具
- [Docker](https://www.docker.com/) - 容器化平台
- [TypeScript](https://www.typescriptlang.org/) - JavaScript的类型化超集
- [uv](https://github.com/astral-sh/uv) - 极速Python包管理器

---

## 📞 联系方式

- 🐛 **问题反馈**：[GitHub Issues](https://github.com/your-username/Mocker/issues)
- 💡 **功能建议**：[GitHub Discussions](https://github.com/your-username/Mocker/discussions)
- 📧 **邮件联系**：your-email@example.com
- 📖 **更多文档**：查看项目内的 `ARCHITECTURE.md` 和 `DOCKER_DEPLOYMENT.md`

---

**⭐ 如果这个项目对你有帮助，请给我们一个Star支持！**