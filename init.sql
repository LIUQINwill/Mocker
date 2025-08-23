-- 初始化数据库脚本
CREATE DATABASE IF NOT EXISTS mocker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mocker;

-- 创建用户并授权（允许Docker容器网络访问）
CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY 'qwer4321';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
CREATE USER IF NOT EXISTS 'mocker'@'%' IDENTIFIED BY 'qwer4321';
GRANT ALL PRIVILEGES ON mocker.* TO 'mocker'@'%';
FLUSH PRIVILEGES;

-- 创建示例Mock接口数据
-- 这些数据将在应用启动后通过Alembic迁移创建表结构后插入
