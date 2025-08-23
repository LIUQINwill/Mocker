#!/bin/bash

# Mocker API平台快速部署脚本

set -e

echo "🎭 Mocker API平台快速部署"
echo "========================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认值
ENVIRONMENT="prod"
FORCE_REBUILD=false

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --dev)
            ENVIRONMENT="dev"
            shift
            ;;
        --prod)
            ENVIRONMENT="prod"
            shift
            ;;
        -f|--force)
            FORCE_REBUILD=true
            shift
            ;;
        -h|--help)
            echo "用法: $0 [选项]"
            echo "选项:"
            echo "  -e, --env ENV     指定环境 (dev|prod, 默认: prod)"
            echo "  --dev             快捷指定开发环境"
            echo "  --prod            快捷指定生产环境"
            echo "  -f, --force       强制重新构建镜像"
            echo "  -h, --help        显示此帮助信息"
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            exit 1
            ;;
    esac
done

echo -e "部署环境: ${BLUE}$ENVIRONMENT${NC}"
echo -e "强制重建: ${BLUE}$FORCE_REBUILD${NC}"
echo

# 检查依赖
echo "1. 检查系统依赖"
echo "---------------"

if ! command -v docker >/dev/null 2>&1; then
    echo -e "${RED}错误: Docker 未安装${NC}"
    echo "请安装 Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "Docker: ${GREEN}✓${NC}"

if ! command -v docker-compose >/dev/null 2>&1; then
    echo -e "${RED}错误: Docker Compose 未安装${NC}"
    echo "请安装 Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi
echo -e "Docker Compose: ${GREEN}✓${NC}"

# 检查文件存在
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}错误: 未找到 docker-compose.yml 文件${NC}"
    echo "请确保在项目根目录下运行此脚本"
    exit 1
fi

echo

# 设置环境变量
echo "2. 准备环境配置"
echo "---------------"

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "复制环境变量配置文件..."
        cp .env.example .env
        echo -e "${GREEN}✓ 已创建 .env 文件${NC}"
    else
        echo -e "${YELLOW}⚠ 未找到环境变量配置文件${NC}"
    fi
else
    echo -e "${GREEN}✓ 环境变量文件已存在${NC}"
fi

echo

# 停止现有服务
echo "3. 停止现有服务"
echo "---------------"

if [ "$ENVIRONMENT" = "dev" ]; then
    COMPOSE_FILE="docker-compose.dev.yml"
else
    COMPOSE_FILE="docker-compose.yml"
fi

echo "停止现有容器..."
docker-compose -f $COMPOSE_FILE down >/dev/null 2>&1 || true
echo -e "${GREEN}✓ 现有服务已停止${NC}"

echo

# 构建镜像
echo "4. 构建镜像"
echo "-----------"

BUILD_ARGS=""
if [ "$FORCE_REBUILD" = true ]; then
    BUILD_ARGS="--no-cache"
    echo "强制重新构建镜像..."
else
    echo "构建镜像..."
fi

docker-compose -f $COMPOSE_FILE build $BUILD_ARGS
echo -e "${GREEN}✓ 镜像构建完成${NC}"

echo

# 启动服务
echo "5. 启动服务"
echo "-----------"

echo "启动所有服务..."
docker-compose -f $COMPOSE_FILE up -d

echo "等待服务启动..."
sleep 10

echo -e "${GREEN}✓ 服务启动完成${NC}"

echo

# 检查服务状态
echo "6. 验证部署"
echo "-----------"

echo "检查容器状态..."
docker-compose -f $COMPOSE_FILE ps

echo

# 等待服务完全就绪
echo "等待服务完全就绪..."
sleep 15

# 简单的健康检查
echo "执行健康检查..."

# 检查后端
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/health" | grep -q "200"; then
    echo -e "后端服务: ${GREEN}✓ 正常${NC}"
else
    echo -e "后端服务: ${YELLOW}⚠ 可能还在启动中${NC}"
fi

# 检查前端
if [ "$ENVIRONMENT" = "dev" ]; then
    FRONTEND_URL="http://localhost:3000"
else
    FRONTEND_URL="http://localhost"
fi

if curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL" | grep -q "200"; then
    echo -e "前端服务: ${GREEN}✓ 正常${NC}"
else
    echo -e "前端服务: ${YELLOW}⚠ 可能还在启动中${NC}"
fi

echo

# 显示访问信息
echo "7. 部署完成"
echo "-----------"

echo -e "${GREEN}🎉 部署成功!${NC}"
echo
echo "访问地址:"
if [ "$ENVIRONMENT" = "dev" ]; then
    echo -e "  ${BLUE}前端界面:${NC} http://localhost:3000"
else
    echo -e "  ${BLUE}前端界面:${NC} http://localhost"
fi
echo -e "  ${BLUE}后端API:${NC}  http://localhost:8000"
echo -e "  ${BLUE}API文档:${NC}  http://localhost:8000/api/v1/docs"
echo -e "  ${BLUE}健康检查:${NC} http://localhost:8000/health"
echo
echo "管理命令:"
echo "  查看状态: docker-compose -f $COMPOSE_FILE ps"
echo "  查看日志: docker-compose -f $COMPOSE_FILE logs -f"
echo "  停止服务: docker-compose -f $COMPOSE_FILE down"
echo
echo "如果使用 Makefile:"
if [ "$ENVIRONMENT" = "dev" ]; then
    echo "  状态: make ps"
    echo "  日志: make dev-logs"
    echo "  停止: make dev-down"
    echo "  重启: make dev-restart"
else
    echo "  状态: make ps"
    echo "  日志: make prod-logs"
    echo "  停止: make prod-down"
    echo "  重启: make prod-restart"
fi
echo
echo -e "${YELLOW}提示: 运行 './scripts/check-deployment.sh' 进行完整的部署验证${NC}"