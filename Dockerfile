# השתמש בגרסת Python 3.12 Slim
FROM python:3.12-slim

# הגדרת ספריית העבודה
WORKDIR /app

# העתקת קובץ התלויות
COPY requirements.txt .

# התקנת התלויות
RUN pip install --no-cache-dir -r requirements.txt

# העתקת קובצי הקוד
COPY . .

# הגדרת נקודת הכניסה להרצת הקובץ הראשי
ENTRYPOINT ["python3", "app.py"]
