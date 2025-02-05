# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# تغییر مالکیت فایل‌ها و تنظیم مجوز اجرا
RUN chmod +x /app/manage.py && chmod -R 777 /app

# تغییر کاربر به root برای جلوگیری از مشکلات دسترسی
USER root

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose Django port
EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
