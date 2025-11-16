# ==========================
# ai_service Dockerfile (light & fast)
# ==========================

FROM python:3.10-slim

# تعيين مجلد العمل
WORKDIR /app

# تثبيت pip و Flask فقط
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && pip install --no-cache-dir flask \
    && apt-get purge -y curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# نسخ الكود
COPY ai_service.py .

# فتح البورت
EXPOSE 9003

# تشغيل الخدمة
CMD ["python", "ai_service.py"]


