#BASE IMAGE
FROM python:3.9-slim

#WORKDIR 
WORKDIR /app

#COPY 
COPY . /app

#EXPOSE 
EXPOSE 5000

#RUN
RUN pip install --no-cache-dir -r requirements.txt

#CMD 
CMD ["python", "app.py"]
