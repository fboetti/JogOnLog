FROM postgres:15.6-alpine

# Installing packages to compile the pg_partman 5.0.0 extension
# The postgresql15-dev package is required to solve the "import posgres.h" error
RUN apk upgrade \
 && apk add \
    gcc \
    git \
    make \
    postgresql15-dev

# Cloning the v5.0.0 version of the pg_partman extension, installing it and removing the source code
RUN git clone -b v5.0.0 https://github.com/pgpartman/pg_partman.git \
 && cd pg_partman \
 && make NO_BGW=1 install \
 && cd .. \
 && rm -rf pg_partman
