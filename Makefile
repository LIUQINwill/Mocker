# Mocker API平台 - Docker部署管理

.PHONY: help build up down logs clean restart health-check

# 默认目标
help: ## 显示帮助信息
	@echo "Mocker API平台 Docker 部署管理"
	@echo ""
	@echo "可用命令："
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# 基本命令
up: ## 启动服务
	docker-compose up -d

down: ## 停止服务
	docker-compose down

logs: ## 查看日志
	docker-compose logs -f

restart: ## 重启服务
	docker-compose restart

# 构建命令
build: ## 构建所有镜像
	docker-compose build

build-up: ## 构建并启动服务
	docker-compose up -d --build

# 清理命令
clean: ## 清理所有容器和镜像
	docker-compose down -v --rmi all
	docker system prune -af

clean-volumes: ## 清理数据卷
	docker-compose down -v

# 健康检查
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
	docker-compose exec mysql mysqldump -u root -pqwer4321 mocker > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore: ## 恢复数据库 (使用 BACKUP_FILE=filename.sql)
	@if [ -z "$(BACKUP_FILE)" ]; then echo "请指定备份文件: make restore BACKUP_FILE=backup.sql"; exit 1; fi
	cat $(BACKUP_FILE) | docker-compose exec -T mysql mysql -u root -pqwer4321 mocker

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
	docker-compose exec mysql mysql -u root -pqwer4321 mocker

# 更新和部署
update: ## 更新并重启服务
	git pull
	docker-compose down
	docker-compose build
	docker-compose up -d
	$(MAKE) health-check

# 快速部署
deploy: build-up ## 快速构建并部署服务
	$(MAKE) health-check

stop: down ## 快速停止服务