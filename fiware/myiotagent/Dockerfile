FROM node:latest

RUN apt update && apt install --yes build-essential flex bison wget subversion m4 python3 python3-dev python3-setuptools libgmp-dev libssl-dev curl dos2unix
RUN wget https://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz && tar xvf pbc-0.5.14.tar.gz && cd /pbc-0.5.14 && ./configure LDFLAGS="-lgmp" && make && make install && ldconfig
COPY /charm /charm
RUN apt-get install python3-pip -y
RUN pip3 install pycrypto
RUN cd /charm && dos2unix configure.sh && ./configure.sh && make && make install && ldconfig