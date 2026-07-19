const indexForm = document.getElementById('index-form');
const indexBtn = document.getElementById('index-btn');
const messages = document.getElementById('messages');
const pipeline = document.getElementById('pipeline');
const askSection = document.getElementById('ask-section');
const repoNameLabel = document.getElementById('repo-name-label');

const askForm = document.getElementById('ask-form');
const askBtn = document.getElementById('ask-btn');
const questionInput = document.getElementById('question-input');
const qaHistory = document.getElementById('qa-history');

function showMessage(text, type) {
  messages.innerHTML = `<div class="message ${type}">${type === 'error' ? '✕' : '✓'} ${text}</div>`;
}

function setLoading(button, isLoading, loadingText, defaultText) {
  button.disabled = isLoading;
  button.innerHTML = isLoading ? `<span class="spinner"></span>` : defaultText;
}

indexForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  messages.innerHTML = '';
  pipeline.style.display = 'none';
  setLoading(indexBtn, true, '', 'Index');

  const formData = new FormData(indexForm);

  try {
    const res = await fetch('/index', { method: 'POST', body: formData });
    const data = await res.json();

    if (!res.ok) {
      showMessage(data.error, 'error');
    } else {
      showMessage(data.success, 'success');
      pipeline.style.display = 'flex';
      repoNameLabel.textContent = data.repo_name;
      askSection.style.display = 'block';
      qaHistory.innerHTML = '';
    }
  } catch (err) {
    showMessage('Something went wrong. Check the server logs.', 'error');
  } finally {
    setLoading(indexBtn, false, '', 'Index');
  }
});

askForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const question = questionInput.value;
  setLoading(askBtn, true, '', 'Ask');

  const formData = new FormData(askForm);

  try {
    const res = await fetch('/ask', { method: 'POST', body: formData });
    const data = await res.json();

    if (!res.ok) {
      showMessage(data.error, 'error');
    } else {
      const sourcesHtml = data.sources && data.sources.length
        ? `<div class="sources">
             <span class="sources-label">sourced from</span>
             ${data.sources.map(s => `<span class="source-file">${s}</span>`).join('')}
           </div>`
        : '';

      const block = document.createElement('div');
      block.className = 'qa-block';
      block.innerHTML = `
        <div class="question">${data.question}</div>
        <div class="answer">${marked.parse(data.answer)}</div>
        ${sourcesHtml}
      `;
      qaHistory.appendChild(block);
      block.scrollIntoView({ behavior: 'smooth', block: 'start' });
      questionInput.value = '';
    }
  } catch (err) {
    showMessage('Something went wrong. Check the server logs.', 'error');
  } finally {
    setLoading(askBtn, false, '', 'Ask');
  }
});