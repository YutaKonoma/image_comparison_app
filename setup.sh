#!/bin/bash

# --- 色の設定（見栄え用） ---
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}   ImageCleaner Project Setup Start  ${NC}"
echo -e "${GREEN}=====================================${NC}"

# 1. .envファイルの作成
if [ ! -f .env ]; then
    echo -e "Creating .env file..."
    cp .env.example .env || echo "DATABASE_URL=mysql+pymysql://root:root_password@db/app_db" > .env
fi

# 2. フォルダの存在確認
mkdir -p backend/php backend/python frontend

# 3. Dockerイメージのビルドと起動
echo -e "${GREEN}Building and starting Docker containers...${NC}"
docker-compose up -d --build

# 4. Laravelのセットアップ
echo -e "${GREEN}Setting up Laravel...${NC}"

# Composerのインストール（プロジェクトが空の場合のみ）
if [ ! -f backend/php/composer.json ]; then
    echo "Initializing Laravel project..."
    docker exec img_laravel composer create-project laravel/laravel .
fi

# .envのコピー（コンテナ内）
docker exec img_laravel cp .env.example .env

# 依存関係のインストール
docker exec img_laravel composer install

# アプリケーションキーの生成
docker exec img_laravel php artisan key:generate

# DBが立ち上がるまで少し待機（MySQLは起動に時間がかかるため）
echo "Waiting for MySQL to be ready..."
sleep 15

# マイグレーション実行
echo -e "${GREEN}Running Database Migrations...${NC}"
docker exec img_laravel php artisan migrate

# 5. Vue.js (Node) のセットアップ
echo -e "${GREEN}Setting up Frontend (Vue.js)...${NC}"
if [ ! -f frontend/package.json ]; then
    echo "Initializing Vue project..."
    # コンテナ内でViteプロジェクトを作成
    docker exec img_vue npm create vite@latest . -- --template vue
fi
docker exec img_vue npm install

echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}   Setup Completed Successfully!     ${NC}"
echo -e "${GREEN}=====================================${NC}"
echo -e "Web App (Vue):   http://localhost:5173"
echo -e "Backend (Laravel): http://localhost:8080"
echo -e "API (FastAPI):     http://localhost:8000/docs"
