const form = document.getElementById('calc-form');
const resultadoEl = document.getElementById('resultado');
const historyButton = document.getElementById('load-history');
const historyList = document.getElementById('history-list');
const welcomeButton = document.getElementById('load-welcome');
const welcomeEl = document.getElementById('welcome');

async function apiGet(path) {
  const response = await fetch(path);
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || 'Erro ao chamar a API');
  }
  return response.json();
}

function showResult(text) {
  resultadoEl.textContent = text;
}

function renderHistory(items) {
  historyList.innerHTML = '';
  if (!items.length) {
    historyList.innerHTML = '<li>Nenhum cálculo registrado.</li>';
    return;
  }
  items.forEach(item => {
    const li = document.createElement('li');
    li.textContent = `${item.id}. ${item.operacao} | ${item.numero1} e ${item.numero2} = ${item.resultado}`;
    historyList.appendChild(li);
  });
}

async function loadHistory() {
  try {
    const data = await apiGet('/historico');
    renderHistory(data);
  } catch (error) {
    historyList.innerHTML = `<li>Erro: ${error.message}</li>`;
  }
}

async function loadWelcome() {
  try {
    const data = await apiGet('/');
    welcomeEl.textContent = data.mensagem || 'API conectada com sucesso.';
  } catch (error) {
    welcomeEl.textContent = `Erro: ${error.message}`;
  }
}

form.addEventListener('submit', async event => {
  event.preventDefault();
  const numero1 = document.getElementById('numero1').value;
  const numero2 = document.getElementById('numero2').value;
  const operacao = document.getElementById('operacao').value;

  if (!numero1 || !numero2) {
    showResult('Preencha ambos os números.');
    return;
  }

  try {
    const params = new URLSearchParams({
      numero1,
      numero2,
      operacao
    });
    const data = await apiGet(`/calcular?${params}`);
    showResult(`Resultado: ${data.resultado} (${data.operacao})`);
    loadHistory();
  } catch (error) {
    showResult(`Erro: ${error.message}`);
  }
});

historyButton.addEventListener('click', loadHistory);
welcomeButton.addEventListener('click', loadWelcome);

window.addEventListener('load', () => {
  loadWelcome();
  loadHistory();
});
