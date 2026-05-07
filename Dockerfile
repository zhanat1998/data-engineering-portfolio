# Python 3.11 image колдонобуз
FROM python:3.11-slim

# Иштөө папкасы
WORKDIR /app

# Китепканаларды орнот
COPY requirements.txt .
RUN pip install -r requirements.txt

# Код жана маалыматты көчүр
COPY main.py .
COPY aug_train.csv .

# Иштет
CMD ["python", "main.py"]
