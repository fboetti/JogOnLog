FROM python:3.12

COPY ./src/requirements.txt src/requirements.txt
RUN python3 -m pip install -r src/requirements.txt

# -- Configuring timezone -- #
ENV TZ=Europe/Rome
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/timezone

EXPOSE 8000

WORKDIR /usr/src/backend

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
