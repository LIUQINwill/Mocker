#!/bin/bash

# Mocker API平台部署检查脚本
# 用于验证Docker部署是否成功

set -e

echo "🎭 Mocker API平台部署检查"
echo "========================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查函数
check_service() {
    local service_name=$1
    local url=$2
    local expected_status=${3:-200}
    
    echo -n "检查 $service_name... "
    
    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "$expected_status"; then
        echo -e "${GREEN}✓ 正常${NC}"
        return 0
    else
        echo -e "${RED}✗ 失败${NC}"
        return 1
    fi
}

check_port() {
    local service_name=$1
    local port=$2
    
    echo -n "检查端口 $port ($service_name)... "
    
    if nc -z localhost $port 2>/dev/null; then
        echo -e "${GREEN}✓ 开放${NC}"
        return 0
    else
        echo -e "${RED}✗ 关闭${NC}"
        return 1
    fi
}

# 检查Docker和Docker Compose是否安装
echo "1. 检查依赖环境"
echo "---------------"

if command -v docker >/dev/null 2>&1; then
    echo -e "Docker: ${GREEN}✓ 已安装${NC} ($(docker --version | cut -d' ' -f3 | cut -d',' -f1))"
else
    echo -e "Docker: ${RED}✗ 未安装${NC}"
    exit 1
fi

if command -v docker-compose >/dev/null 2>&1; then
    echo -e "Docker Compose: ${GREEN}✓ 已安装${NC} ($(docker-compose --version | cut -d' ' -f4 | cut -d',' -f1))"
else
    echo -e "Docker Compose: ${RED}✗ 未安装${NC}"
    exit 1
fi

echo

# 检查容器状态
echo "2. 检查容器状态"
echo "---------------"

containers=("mocker_mysql" "mocker_backend" "mocker_frontend")
for container in "${containers[@]}"; do
    echo -n "检查容器 $container... "
    
    if docker ps --format "table {{.Names}}" | grep -q "^$container$"; then
        status=$(docker ps --format "table {{.Names}}\t{{.Status}}" | grep "^$container" | cut -d$'\t' -f2)
        echo -e "${GREEN}✓ 运行中${NC} ($status)"
    else
        echo -e "${RED}✗ 未运行${NC}"
    fi
done

echo

# 检查端口
echo "3. 检查端口状态"
echo "---------------"

check_port "前端服务" 80 || check_port "前端开发服务" 3000
check_port "后端API" 8000
check_port "MySQL数据库" 3306
check_port "Redis缓存" 6379 || echo -e "${YELLOW}⚠ Redis是可选服务${NC}"

echo

# 检查服务响应
echo "4. 检查服务响应"
echo "---------------"

# 等待服务启动
echo "等待服务完全启动..."
sleep 5

# 检查后端服务
check_service "后端健康检查" "http://localhost:8000/health"
check_service "后端API文档" "http://localhost:8000/api/v1/docs"

# 检查前端服务
if check_service "前端服务" "http://localhost/" 200 2>/dev/null; then
    echo -e "前端服务: ${GREEN}✓ 正常${NC}"
elif check_service "前端开发服务" "http://localhost:3000/" 200 2>/dev/null; then
    echo -e "前端开发服务: ${GREEN}✓ 正常${NC}"
else
    echo -e "前端服务: ${RED}✗ 失败${NC}"
fi

echo

# 检查数据库连接
echo "5. 检查数据库连接"
echo "----------------"

echo -n "检查MySQL连接... "
if docker exec mocker_mysql mysqladmin ping -h localhost -u root -pmocker123 >/dev/null 2>&1; then
    echo -e "${GREEN}✓ 正常${NC}"
else
    echo -e "${RED}✗ 失败${NC}"
fi

echo -n "检查数据库表... "
if docker exec mocker_mysql mysql -u root -pmocker123 -e "USE mocker; SHOW TABLES;" >/dev/null 2>&1; then
    table_count=$(docker exec mocker_mysql mysql -u root -pmocker123 -e "USE mocker; SHOW TABLES;" | wc -l)
    echo -e "${GREEN}✓ 正常${NC} (共 $((table_count-1)) 张表)"
else
    echo -e "${RED}✗ 失败${NC}"
fi

echo

# 检查日志中的错误
echo "6. 检查服务日志"
echo "---------------"

echo "检查后端服务日志中的错误..."
backend_errors=$(docker logs mocker_backend 2>&1 | grep -i "error\|exception\|failed" | wc -l)
if [ "$backend_errors" -eq 0 ]; then
    echo -e "后端日志: ${GREEN}✓ 无错误${NC}"
else
    echo -e "后端日志: ${YELLOW}⚠ 发现 $backend_errors 个错误${NC}"
fi

echo "检查前端服务日志中的错误..."
frontend_errors=$(docker logs mocker_frontend 2>&1 | grep -i "error\|exception\|failed" | wc -l)
if [ "$frontend_errors" -eq 0 ]; then
    echo -e "前端日志: ${GREEN}✓ 无错误${NC}"
else
    echo -e "前端日志: ${YELLOW}⚠ 发现 $frontend_errors 个错误${NC}"
fi

echo

# 性能检查
echo "7. 性能检查"
echo "-----------"

echo "检查容器资源使用情况..."
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" | head -n 5

echo

# 总结
echo "8. 部署总结"
echo "-----------"

echo -e "${GREEN}✅ 部署检查完成!${NC}"
echo
echo "访问地址："
echo "  - 前端界面: http://localhost (生产) 或 http://localhost:3000 (开发)"
echo "  - 后端API:  http://localhost:8000"
echo "  - API文档:  http://localhost:8000/api/v1/docs"
echo "  - 健康检查: http://localhost:8000/health"
echo
echo "常用命令："
echo "  - 查看服务状态: make ps"
echo "  - 查看日志: make logs"
echo "  - 停止服务: make prod-down"
echo "  - 重启服务: make prod-restart"
echo
echo -e "${YELLOW}注意: 如果发现问题，请查看具体服务日志进行排查${NC}"