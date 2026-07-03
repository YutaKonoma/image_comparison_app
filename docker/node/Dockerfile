# frontend-vue/Dockerfile
FROM node:20-slim
FROM node:20-alpine

WORKDIR /app

# パッケージ管理
COPY package*.json ./
RUN npm install

# アプリケーションコードのコピー
COPY . .

# Viteのデフォルトポート
EXPOSE 5173

# 開発用起動コマンド
# 0.0.0.0でホストしないとDocker外からアクセスできないため
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
