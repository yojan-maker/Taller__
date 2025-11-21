FROM node:18-alpine

WORKDIR /app

COPY server.js .

RUN npm install express socket.io

EXPOSE 3000

CMD ["node", "server.js"]
