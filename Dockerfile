FROM python:3.8
RUN mkdir /src/
WORKDIR /src
ADD ./requirements.txt ./
RUN pip install -r requirements.txt

ADD . .

