# FROM node:latest AS portal
#
# WORKDIR /app
#
# COPY ./front/portal ./
# RUN npm install
# RUN npm run generate

FROM node:latest AS blog

WORKDIR /app

COPY ./front/blog ./
RUN npm install
RUN npm run generate



# Указываем базовый образ
FROM python:3.12

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . .

#COPY --from=portal /app/.output/public /app/bundle/portal/
COPY --from=blog /app/.output/public /app/bundle/blog/
#COPY --from=blog /app/.output/public/index.html /app/templates/

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["celery", "-A", "abrikosio", "worker", "--loglevel=info"]
CMD ["celery", "-A", "abrikosio", "beat", "--loglevel=info"]
