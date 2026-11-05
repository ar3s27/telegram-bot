#!/usr/bin/env bash
# deploy.sh bunu sunucuda ~/apps/telegram-bot içinde çalıştırır.
# Token henüz yazılmadıysa imajı derler ama botu başlatmaz.
set -euo pipefail

if [ ! -f .env ]; then
  umask 077
  cat > .env <<'ENV'
# BotFather'dan aldığın token'ı = işaretinden sonra yaz (tırnak koyma), sonra:
#   cd ~/apps/telegram-bot && docker compose up -d
TELEGRAM_BOT_TOKEN=
ENV
fi

if ! grep -qE '^TELEGRAM_BOT_TOKEN=[^[:space:]]+' .env; then
  docker compose build
  touch .skip-start
  echo ">> NOT: ~/apps/telegram-bot/.env içinde TELEGRAM_BOT_TOKEN boş; bot başlatılmadı."
  echo ">>      Token'ı yazdıktan sonra: cd ~/apps/telegram-bot && docker compose up -d"
fi
