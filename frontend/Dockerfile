FROM node

WORKDIR /src/

COPY package*.json .
RUN npm install

COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

COPY . .

ENTRYPOINT ["/entrypoint.sh"]