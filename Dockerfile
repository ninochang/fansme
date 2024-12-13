FROM python:3.11-bullseye
WORKDIR /usr/src/app

# Install the application dependencies
COPY . . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
