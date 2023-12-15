const socket = new WebSocket('ws://localhost:8765');

socket.addEventListener('open', function (event) {
    console.log('Connected to server');

    const name = prompt("What's your name?");
    socket.send(name);
    console.log(`>>> ${name}`);
});

socket.addEventListener('message', function (event) {
    console.log(`<<< ${event.data}`);
});

