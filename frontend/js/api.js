const API = (window.ENV && window.ENV.API) || "http://localhost:8000";

async function apiFetch(caminho, { metodo = "GET", corpo = null } = {}) {
  const opcoes = { method: metodo, credentials: "include", headers: {} };
  if (corpo !== null) {
    opcoes.headers["Content-Type"] = "application/json";
    opcoes.body = JSON.stringify(corpo);
  }
  const resp = await fetch(API + caminho, opcoes);
  const dados = await resp.json().catch(() => ({}));
  if (!resp.ok) throw new Error(dados.erro || "Erro de conexão com o servidor");
  return dados;
}
