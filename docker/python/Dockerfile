# Pythonイメージ
FROM python:3.11-slim

# OSの依存パッケージ（画像処理用）
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ
WORKDIR /app

# requirements.txtをコピー
COPY requirements.txt .

# ライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# コードをコピー
COPY . .

# FastAPI用のポート 8000
EXPOSE 8000

# デフォルトの起動コマンド（Compose側で上書きするので一旦ダミー）
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]
