const http = require('http');

const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end('<h1>🐳 Node.js в Docker контейнере!</h1>');
});

server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
