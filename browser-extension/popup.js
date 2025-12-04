// Cali X One Browser Extension Popup
let websocket = null;
const statusDiv = document.getElementById('status');
const cliOutput = document.getElementById('cli-output');
const cliInput = document.getElementById('cli-input');
const connectBtn = document.getElementById('connect-btn');
const sendBtn = document.getElementById('send-btn');
const systemInfoBtn = document.getElementById('system-info-btn');

function updateStatus(connected) {
  statusDiv.className = connected ? 'status connected' : 'status disconnected';
  statusDiv.textContent = connected ? 'Connected to Cali X One' : 'Disconnected';
  connectBtn.textContent = connected ? 'Disconnect' : 'Connect';
}

function addToCLI(text) {
  const timestamp = new Date().toLocaleTimeString();
  cliOutput.textContent += `[${timestamp}] ${text}\n`;
  cliOutput.scrollTop = cliOutput.scrollHeight;
}

function connect() {
  if (websocket && websocket.readyState === WebSocket.OPEN) {
    websocket.close();
    return;
  }

  try {
    websocket = new WebSocket('ws://localhost:9997');

    websocket.onopen = () => {
      updateStatus(true);
      addToCLI('Connected to Bubble Worker');
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.stdout !== undefined) {
        addToCLI(`$ ${data.command}`);
        addToCLI(data.stdout);
        if (data.stderr) addToCLI(`Error: ${data.stderr}`);
      } else if (data.type === 'pong') {
        addToCLI('Pong from server');
      } else if (data.worker_id) {
        addToCLI(`System Info: Worker ${data.worker_id}, ${data.active_sessions} sessions`);
      } else {
        addToCLI(JSON.stringify(data, null, 2));
      }
    };

    websocket.onclose = () => {
      updateStatus(false);
      addToCLI('Disconnected from Bubble Worker');
    };

    websocket.onerror = (error) => {
      addToCLI('WebSocket error: ' + error);
    };

  } catch (error) {
    addToCLI('Connection failed: ' + error.message);
  }
}

function sendCommand() {
  if (!websocket || websocket.readyState !== WebSocket.OPEN) {
    addToCLI('Not connected to Bubble Worker');
    return;
  }

  const command = cliInput.value.trim();
  if (!command) return;

  const message = {
    type: 'cli_command',
    command: command
  };

  websocket.send(JSON.stringify(message));
  cliInput.value = '';
}

function getSystemInfo() {
  if (!websocket || websocket.readyState !== WebSocket.OPEN) {
    addToCLI('Not connected to Bubble Worker');
    return;
  }

  const message = {
    type: 'system_info'
  };

  websocket.send(JSON.stringify(message));
}

// Event listeners
connectBtn.addEventListener('click', connect);
sendBtn.addEventListener('click', sendCommand);
systemInfoBtn.addEventListener('click', getSystemInfo);

cliInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    sendCommand();
  }
});

// Auto-connect on popup open
connect();