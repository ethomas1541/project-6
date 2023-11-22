FROM python:3.8
LABEL maintainer="ethomas7@uoregon.edu"
RUN apt-get update -y
COPY . /brevets_svc
WORKDIR /brevets_svc
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "-B"]
CMD ["flask_brevets.py"]
