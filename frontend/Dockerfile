# Этап 1: Сборка React-приложения
FROM node:18-alpine as builder

WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package.json ./
COPY package-lock.json ./
RUN npm install

# Копируем остальные файлы приложения
COPY . .

# Собираем production-билд
RUN npm run build

# Этап 2: Настройка Nginx для раздачи статики
FROM nginx:1.25-alpine

# Копируем собранные файлы из этапа сборки
COPY --from=builder /app/build /usr/share/nginx/html

# Копируем нашу конфигурацию Nginx
# Мы удаляем стандартную конфигурацию, чтобы избежать конфликтов
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

# Указываем Nginx запуститься на переднем плане
CMD ["nginx", "-g", "daemon off;"]