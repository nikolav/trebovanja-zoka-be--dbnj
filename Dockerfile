FROM python:3.12.2

# Set work directory
WORKDIR /home/app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy files
COPY . .

# add chrome --headless for pdfs
RUN apt update
RUN apt-get update -y
RUN curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm ./google-chrome-stable_current_amd64.deb

# Expose Flask port
EXPOSE 5000

# Run app
# CMD ["python", "app.py"]
CMD ["./wserver.sh"]
