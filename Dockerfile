FROM python:3.12-bookworm

# everything in one dir
RUN mkdir /app
WORKDIR /app

# sort out reqs 
COPY requirements.txt /app/
RUN pip3 install --user -r requirements.txt

# now code
COPY src /app

# and run it
CMD [ "python", "/app/main.py" ]