# Pull Docker image for Python 3.11
FROM python:3.11

# Create app directory then copy all contents 
WORKDIR /app
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Run the app
CMD [ "python", "app.py" ]