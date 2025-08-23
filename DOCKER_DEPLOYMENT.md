# Mocker API平台 - Docker部署指南

## 概述

本文档提供了Mocker API平台的完整Docker化部署方案，支持开发和生产两种环境配置。

## 架构设计

### 技术栈
- **后端**: FastAPI + Python 3.10 + SQLAlchemy + MySQL
- **前端**: Vue 3 + TypeScript + Vite + TailwindCSS
- **数据库**: MySQL 8.0
- **缓存**: Redis 7.0 (可选)
- **容器编排**: Docker Compose

### 架构图
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx/前端     │───▶│   FastAPI/后端   │───▶│   MySQL数据库    │
│   (Port 80/3000)│    │   (Port 8000)   │    │   (Port 3306)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Redis缓存      │
                       │   (Port 6379)   │
                       └─────────────────┘
```

## 快速开始

### 1. 环境准备

确保系统已安装：
- Docker (≥ 20.10)
- Docker Compose (≥ 2.0)
- Make (可选，用于简化命令)

### 2. 克隆项目并配置

```bash
# 克隆项目
git clone <project-url>
cd mocker

# 复制环境变量文件
cp .env.example .env

# 编辑环境变量（可选）
vim .env
```

### 3. 启动服务

**开发环境（推荐用于开发调试）**
```bash
# 使用 Make (推荐)
make dev

# 或直接使用 docker-compose
docker-compose -f docker-compose.dev.yml up -d
```

**生产环境**
```bash
# 使用 Make (推荐)
make prod

# 或直接使用 docker-compose
docker-compose up -d
```

### 4. 验证部署

访问以下地址验证服务状态：
- 前端界面: http://localhost (生产) 或 http://localhost:3000 (开发)
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/api/v1/docs
- 健康检查: http://localhost:8000/health

## 部署配置详解

### 开发环境 (docker-compose.dev.yml)

**特点:**
- 支持热重载
- 挂载源码目录
- 包含开发工具
- 调试友好的配置

**服务配置:**
- MySQL: 开发用数据库，数据持久化
- Backend: 挂载源码，支持热重载
- Frontend: Vite开发服务器，支持HMR
- Redis: 轻量级配置

### 生产环境 (docker-compose.yml)

**特点:**
- 优化的镜像构建
- 安全配置
- 性能优化
- 健康检查

**服务配置:**
- MySQL: 生产级配置，优化内存使用
- Backend: 非root用户运行，健康检查
- Frontend: Nginx托管，静态文件优化
- Redis: 生产级配置和持久化

## 环境变量配置

主要配置项说明：

```bash
# 数据库配置
DATABASE_URL=mysql+pymysql://root:mocker123@mysql:3306/mocker

# 应用配置
DEBUG=false  # 生产环境设为false
SECRET_KEY=your-secret-key-here-change-in-production

# CORS配置
BACKEND_CORS_ORIGINS=["http://localhost:80"]
```

## 常用命令

### 使用 Makefile (推荐)

```bash
# 查看所有可用命令
make help

# 开发环境
make dev                # 启动开发环境
make dev-down          # 停止开发环境
make dev-logs          # 查看开发环境日志

# 生产环境
make prod              # 启动生产环境  
make prod-down         # 停止生产环境
make prod-logs         # 查看生产环境日志

# 数据库管理
make db-migrate        # 运行数据库迁移
make db-reset          # 重置数据库
make backup            # 备份数据库
make restore BACKUP_FILE=backup.sql  # 恢复数据库

# 监控和调试
make ps                # 显示容器状态
make stats             # 显示资源使用情况
make health-check      # 检查服务健康状态
make shell-backend     # 进入后端容器
make shell-mysql       # 进入数据库容器

# 清理
make clean             # 清理所有容器和镜像
```

### 直接使用 Docker Compose

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启特定服务
docker-compose restart backend

# 查看服务状态
docker-compose ps
```

## 数据管理

### 数据库迁移

```bash
# 运行迁移
make db-migrate

# 或手动执行
docker-compose exec backend uv run alembic upgrade head
```

### 数据备份与恢复

```bash
# 备份数据库
make backup

# 恢复数据库
make restore BACKUP_FILE=backup_20231201_120000.sql
```

## 性能优化

### 生产环境优化建议

1. **MySQL优化**
   ```yaml
   # docker-compose.yml 中的配置
   command: --innodb-buffer-pool-size=512M --max-connections=200
   ```

2. **Nginx缓存配置**
   ```nginx
   # nginx.conf 中已包含
   location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
       expires 1y;
       add_header Cache-Control "public, immutable";
   }
   ```

3. **容器资源限制**
   ```yaml
   deploy:
     resources:
       limits:
         memory: 512M
         cpus: '0.5'
   ```

## 安全配置

### 生产环境安全检查清单

- [ ] 更改默认密码
- [ ] 设置强密钥 SECRET_KEY
- [ ] 配置适当的CORS策略
- [ ] 使用非root用户运行容器
- [ ] 启用防火墙规则
- [ ] 定期更新镜像
- [ ] 配置日志轮转

### 网络安全

```bash
# 只暴露必要端口
ports:
  - "80:80"    # 只暴露前端端口
  # - "8000:8000"  # 生产环境不暴露后端端口
  # - "3306:3306"  # 生产环境不暴露数据库端口
```

## 监控和日志

### 健康检查

所有服务都配置了健康检查：
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### 日志管理

```bash
# 查看特定服务日志
docker-compose logs -f backend

# 查看最近100行日志
docker-compose logs --tail=100 frontend

# 实时跟踪所有服务日志
docker-compose logs -f
```

## 故障排除

### 常见问题

1. **数据库连接失败**
   ```bash
   # 检查MySQL容器状态
   docker-compose ps mysql
   
   # 查看MySQL日志
   docker-compose logs mysql
   ```

2. **前端无法访问后端API**
   - 检查nginx配置中的代理设置
   - 验证后端服务是否正常运行
   - 检查CORS配置

3. **容器启动失败**
   ```bash
   # 查看详细错误信息
   docker-compose logs [service-name]
   
   # 重新构建镜像
   docker-compose build --no-cache [service-name]
   ```

### 调试命令

```bash
# 进入容器调试
docker-compose exec backend /bin/bash
docker-compose exec frontend /bin/sh

# 查看容器网络
docker network ls
docker network inspect mocker_mocker-network

# 检查端口占用
netstat -tlnp | grep :8000
```

## 部署架构决策记录(ADR)

### ADR-001: 选择Docker容器化部署

**状态**: 已接受

**背景**: 需要标准化部署流程，支持多环境一致性部署

**决策**: 采用Docker + Docker Compose方案

**原因**:
- 环境一致性保证
- 简化部署和运维
- 支持水平扩展
- 便于CI/CD集成

**替代方案**:
- 传统虚拟机部署（复杂度高）
- Kubernetes（过度设计）

**风险与缓解**:
- 性能开销 → 使用多阶段构建优化镜像
- 学习成本 → 提供详细文档和脚本

### ADR-002: 前后端分离架构

**状态**: 已接受

**背景**: 需要支持团队并行开发，提高开发效率

**决策**: 采用Nginx + FastAPI的前后端分离架构

**原因**:
- 职责分离，便于团队协作
- 技术栈灵活选择
- 支持独立部署和扩展

**风险与缓解**:
- 跨域问题 → 配置CORS和Nginx代理
- 部署复杂度 → 使用Docker Compose编排

## 升级和维护

### 版本升级

```bash
# 停止服务
make prod-down

# 拉取最新代码
git pull

# 重新构建并启动
make build-prod
make prod-up

# 验证升级
make health-check
```

### 定期维护

```bash
# 清理无用镜像和容器
docker system prune -f

# 备份数据
make backup

# 更新基础镜像
docker-compose pull
```

---

## 联系方式

如有问题或建议，请联系开发团队或提交Issue。