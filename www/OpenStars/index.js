const input = document.getElementById("commandInput");
const button = document.getElementById("sendCommandButton");
const output = document.getElementById("commandOutput");
const plRefresh = document.getElementById("plRefresh")
const serverAddressInput = document.getElementById("serverAddressInput")
const connectButton = document.getElementById("loginButton")
let ws;

connectButton.addEventListener('click', () => {
    connect();
})

button.addEventListener('click', () => {
    const command = input.value
    log(`> ${command}`)
    ws.send(command);
})

input.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        if (this.value.trim() !== '') {
            button.click()
            this.value = ''
        }
    }
})

function log(text) {
    output.textContent += `\n${text}`
    output.scrollTop = output.scrollHeight;
}

function getPlayersList() {
    tempSocket = new WebSocket(ws.url);
    tempSocket.onopen = () => {
        tempSocket.send("clients")
    }
    tempSocket.onmessage = (event) => {
        tempSocket.close()
        loadPlayerList(JSON.parse(event.data))
    };
}

function loadPlayerList(list) {
    for (const clientId in list.Clients) {
        const clientsContainer = document.getElementById("playersListHelper")
        if (list.Clients.hasOwnProperty(clientId)) {
            const clientInfo = list.Clients[clientId];
            const socketInfo = clientInfo.SocketInfo;
            
            const clientDiv = document.createElement('div');
            clientDiv.className = 'client';
            
            clientsContainer.innerHTML = '';
            clientDiv.innerHTML = `
                <strong>Client ID:</strong> ${clientId}<br>
                <strong>Remote Address:</strong> ${socketInfo.remote_address.join(':')}
            `;
            
            clientsContainer.appendChild(clientDiv);
        }
    }
}

function connect() {
    if (ws) {
        ws.close();
    }
    
    ws = new WebSocket(`ws://${serverAddressInput.value}`);
    ws.onopen = () => {
        log("Connected");
        ws.send("about");
        log("Console ready. Type commands.")
    };
    
    ws.onmessage = (event) => {
        log(event.data);
    };
    
    ws.onclose = (event) => {
        log(`Connection lost: ${event.data}`)
    }
}