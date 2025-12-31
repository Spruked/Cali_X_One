// Cali X One Content Script
// Injects floating bubble interface on web pages

// Create floating bubble
const bubble = document.createElement('div');
bubble.id = 'cali-bubble';
bubble.innerHTML = `
  <div class="cali-bubble-content">
    <div class="cali-header">Cali X One</div>
    <div class="cali-status">Ready</div>
    <button class="cali-toggle">▶</button>
  </div>
  <div class="cali-panel" style="display: none;">
    <textarea class="cali-input" placeholder="Ask Cali..."></textarea>
    <div class="cali-output"></div>
  </div>
`;

document.body.appendChild(bubble);

// Add event listeners
const toggleBtn = bubble.querySelector('.cali-toggle');
const panel = bubble.querySelector('.cali-panel');
const input = bubble.querySelector('.cali-input');
const output = bubble.querySelector('.cali-output');

toggleBtn.addEventListener('click', () => {
  const isVisible = panel.style.display !== 'none';
  panel.style.display = isVisible ? 'none' : 'block';
  toggleBtn.textContent = isVisible ? '▶' : '◀';
});

input.addEventListener('keypress', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    const query = input.value.trim();
    if (query) {
      sendQuery(query);
      input.value = '';
    }
  }
});

function sendQuery(query) {
  output.textContent += `You: ${query}\n`;

  // Send to background script
  chrome.runtime.sendMessage({
    type: 'CALI_QUERY',
    query: query
  }, (response) => {
    if (response.success) {
      output.textContent += `Cali: ${JSON.stringify(response.data)}\n`;
    } else {
      output.textContent += `Error: ${response.error}\n`;
    }
    output.scrollTop = output.scrollHeight;
  });
}

// Make bubble draggable
let isDragging = false;
let dragOffset = { x: 0, y: 0 };

bubble.addEventListener('mousedown', (e) => {
  isDragging = true;
  dragOffset.x = e.clientX - bubble.offsetLeft;
  dragOffset.y = e.clientY - bubble.offsetTop;
});

document.addEventListener('mousemove', (e) => {
  if (isDragging) {
    bubble.style.left = (e.clientX - dragOffset.x) + 'px';
    bubble.style.top = (e.clientY - dragOffset.y) + 'px';
  }
});

document.addEventListener('mouseup', () => {
  isDragging = false;
});