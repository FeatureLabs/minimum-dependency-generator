FROM python:3.8

ADD minimum_dependency_generator minimum_dependency_generator
ADD requirements.txt requirements.txt

RUN pip install pip --upgrade --progress-bar off
RUN pip install -r requirements.txt --progress-bar off
ENTRYPOINT ["python", "/minimum_dependency_generator/main.py"]
