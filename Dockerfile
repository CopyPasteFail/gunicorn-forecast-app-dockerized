FROM python:3.9-alpine 

# Set the working directory to /app and change ownership to "reguser"
WORKDIR /app

COPY pip-requirements /app/pip-requirements

RUN pip install -r pip-requirements/requirements.txt

COPY wsgi /app/wsgi

WORKDIR /app/wsgi

# launch gunicorn
# CMD gunicorn --bind 0.0.0.0:5000 wf:app
CMD gunicorn --bind 0.0.0.0:5000 --log-level=DEBUG wf:app
# run with 'docker run --name weather_app -p 8080:5000 <image name>'

