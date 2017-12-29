FROM node:latest

RUN cd /opt && \
  git clone https://github.com/telefonicaid/iotagent-json.git && \
  cd iotagent-json && \
  npm install --production

COPY . /opt/iotagent-json/
WORKDIR /opt/iotagent-json
EXPOSE 4041

ENTRYPOINT bin/iotagent-json config.js
