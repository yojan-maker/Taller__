const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.get('/', (req, res) => {
  res.send('<h1>🎮 Bienvenido al Juego Multijugador</h1>');
});

let players = {};

io.on('connection', (socket) => {
  console.log('Jugador conectado:', socket.id);
  players[socket.id] = { x: 0, y: 0 };

  socket.on('move', (data) => {
    players[socket.id] = data;
    io.emit('state', players);
  });

  socket.on('disconnect', () => {
    delete players[socket.id];
    io.emit('state', players);
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Servidor del juego en puerto ${PORT}`);
});
