# Mocker API平台 - Docker部署管理

.PHONY: help build up down logs clean dev-up dev-down prod-up prod-down restart health-check

# 默认目标
help: ## 显示帮助信息
	@echo "Mocker API平台 Docker 部署管理"
	@echo ""
	@echo "可用命令："
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# 开发环境命令
dev-up: ## 启动开发环境
	docker-compose -f docker-compose.dev.yml up -d

dev-down: ## 停止开发环境
	docker-compose -f docker-compose.dev.yml down

dev-logs: ## 查看开发环境日志
	docker-compose -f docker-compose.dev.yml logs -f

dev-restart: ## 重启开发环境
	docker-compose -f docker-compose.dev.yml restart

# 生产环境命令
prod-up: ## 启动生产环境
	docker-compose -f docker-compose.yml up -d

prod-down: ## 停止生产环境
	docker-compose -f docker-compose.yml down

prod-logs: ## 查看生产环境日志
	docker-compose -f docker-compose.yml logs -f

prod-restart: ## 重启生产环境
	docker-compose -f docker-compose.yml restart

# 通用命令
build: ## 构建所有镜像
	docker-compose build

build-dev: ## 构建开发环境镜像
	docker-compose -f docker-compose.dev.yml build

build-prod: ## 构建生产环境镜像
	docker-compose -f docker-compose.yml build

logs: ## 查看日志 (默认生产环境)
	docker-compose logs -f

clean: ## 清理所有容器和镜像
	docker-compose -f docker-compose.yml down -v --rmi all
	docker-compose -f docker-compose.dev.yml down -v --rmi all
	docker system prune -af

health-check: ## 检查服务健康状态
	@echo "检查服务健康状态..."
	@curl -f http://localhost:8000/health || echo "后端服务不可用"
	@curl -f http://localhost/ || echo "前端服务不可用"

# 数据库管理
db-migrate: ## 运行数据库迁移
	docker-compose exec backend uv run alembic upgrade head

db-reset: ## 重置数据库
	docker-compose down -v
	docker-compose up -d mysql
	sleep 10
	docker-compose up -d backend
	$(MAKE) db-migrate

# 备份和恢复
backup: ## 备份数据库
	@echo "备份数据库到 backup_$(shell date +%Y%m%d_%H%M%S).sql"
	docker-compose exec mysql mysqldump -u root -pmocker123 mocker > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore: ## 恢复数据库 (使用 BACKUP_FILE=filename.sql)
	@if [ -z "$(BACKUP_FILE)" ]; then echo "请指定备份文件: make restore BACKUP_FILE=backup.sql"; exit 1; fi
	cat $(BACKUP_FILE) | docker-compose exec -T mysql mysql -u root -pmocker123 mocker

# 监控和调试
ps: ## 显示运行中的容器
	docker-compose ps

stats: ## 显示容器资源使用情况
	docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"

shell-backend: ## 进入后端容器shell
	docker-compose exec backend /bin/bash

shell-frontend: ## 进入前端容器shell
	docker-compose exec frontend /bin/sh

shell-mysql: ## 进入MySQL容器
	docker-compose exec mysql mysql -u root -pmocker123 mocker

# 更新和部署
update: ## 更新并重启服务
	git pull
	docker-compose down
	docker-compose build
	docker-compose up -d
	$(MAKE) health-check

# 快速启动命令
dev: dev-up ## 快速启动开发环境
prod: prod-up ## 快速启动生产环境
stop: prod-down ## 快速停止服务