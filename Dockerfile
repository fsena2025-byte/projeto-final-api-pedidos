FROM python:3.12-slim
WORKDIR /app
COPY app ./app
ENV PORT=8000 DATABASE_PATH=/data/orders.db LOG_LEVEL=INFO
EXPOSE 8000
CMD ["python", "-m", "app.main"]
