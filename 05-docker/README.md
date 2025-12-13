# Docker

## 📋 Описание
Управление Docker контейнерами, образами и Docker Compose прямо из VS Code.

## 🚀 Установка
1. Установить Docker Desktop
2. Extensions → **"Docker"**

## ⚙️ Возможности
- 📦 Управление контейнерами и образами
- 📊 Просмотр логов
- 🔍 Inspect контейнеров
- 🐳 Docker Compose поддержка
- 🐛 Debugging в контейнерах

## 🔧 Команды

```bash
# Build образ
docker build -t myapp .

# Запуск контейнера
docker run -p 3000:3000 myapp

# Docker Compose
docker-compose up -d
docker-compose down

# Просмотр логов
docker logs container_name

# Выполнение команд
docker exec -it container_name bash
```

## 📁 Структура Dockerfile

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

## 🔗 Ссылки
- [Docker Docs](https://docs.docker.com/)
- [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)

[⬅️ Назад](../README.md)
