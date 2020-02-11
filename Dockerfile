FROM python:3.7.6

COPY src /src
COPY entrypoint.sh /entrypoint.sh

WORKDIR /src
RUN pip install -r requirements.txt

CMD ["/bin/bash", "/entrypoint.sh"]