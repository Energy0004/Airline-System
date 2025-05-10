# 1️⃣ Base image
FROM python:3.11-slim

# 2️⃣ Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ Set working directory
WORKDIR /app

# 4️⃣ Copy requirements and install
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 5️⃣ Copy entire project
COPY . /app/

# 6️⃣ Expose port
EXPOSE 8000

RUN python manage.py collectstatic --noinput

# Дать права на папку проекта
RUN chmod -R 755 /app && chown -R www-data:www-data /app

# 7️⃣ Run migrations & start server
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn airline_system.wsgi:application --bind 0.0.0.0:8000"]
