// Configuração da URL do Back-End em Python
const API_BASE_URL = 'http://localhost:5000/api';

// Estado global da aplicação no Front-End
let produtosGlobal = [];
let carrinho = [];
let usuarioLogado = null;

// Executa ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
    carregarProdutos();
    carregarReceitas();
});

// Navegação em abas SPA (Single Page Application)
function navegar(secaoId) {
    document.querySelectorAll('.secao').forEach(sec => sec.style.display = 'none');
    document.getElementById(`sec-${secaoId}`).style.display = 'block';
}

// Consumo de API: Buscar Produtos da tabela Produto do BD
async function carregarProdutos() {
    try {
        const response = await fetch(`${API_BASE_URL}/produtos`);
        if (!response.ok) throw new Error("Erro ao buscar produtos");
        produtosGlobal = await response.json();
        renderizarProdutos(produtosGlobal);
    } catch (error) {
        console.warn("Utilizando dados simulados devido a falha de conexão com o Back-End:", error);
        // Fallback de teste estruturado conforme o BD
        produtosGlobal = [
            { idProduto: 1, nome: "Farinha de Arroz 1kg", preco: 7.36, estoqueQtd: 30, imagemUrl: "https://via.placeholder.com/150", categoria: "sem-gluten" },
            { idProduto: 2, nome: "Biscoito de Polvilho 100g", preco: 4.50, estoqueQtd: 15, imagemUrl: "https://via.placeholder.com/150", categoria: "sem-gluten" },
            { idProduto: 3, nome: "Leite de Amêndoas 1L", preco: 14.90, estoqueQtd: 20, imagemUrl: "https://via.placeholder.com/150", categoria: "sem-lactose" }
        ];
        renderizarProdutos(produtosGlobal);
    }
}

// Renderização dos Produtos no DOM
function renderizarProdutos(produtos) {
    const grid = document.getElementById('grid-produtos');
    grid.innerHTML = '';

    produtos.forEach(prod => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <img src="${prod.imagemUrl}" alt="${prod.nome}">
            <h3>${prod.nome}</h3>
            <p class="preco">R$ ${parseFloat(prod.preco).toFixed(2)}</p>
            <button onclick="adicionarAoCarrinho(${prod.idProduto})">Adicionar ao Carrinho</button>
        `;
        grid.appendChild(card);
    });
}

// Filtro e Busca dinâmica no Catálogo
function filtrarProdutos() {
    const textoBusca = document.getElementById('busca-produto').value.toLowerCase();
    const categoria = document.getElementById('filtro-categoria').value;

    const filtrados = produtosGlobal.filter(p => {
        const bateNome = p.nome.toLowerCase().includes(textoBusca);
        const bateCategoria = categoria === 'todos' || p.categoria === categoria;
        return bateNome && bateCategoria;
    });

    renderizarProdutos(filtrados);
}

// Gerenciamento do Carrinho
function adicionarAoCarrinho(idProduto) {
    const produto = produtosGlobal.find(p => p.idProduto === idProduto);
    if (!produto) return;

    if (produto.estoqueQtd <= 0) {
        alert("Produto fora de estoque!");
        return;
    }

    const itemExistente = carrinho.find(item => item.idProduto === idProduto);
    if (itemExistente) {
        itemExistente.quantidade++;
    } else {
        carrinho.push({ ...produto, quantidade: 1 });
    }

    atualizarCarrinhoUI();
}

function atualizarCarrinhoUI() {
    // Atualizar badge do header
    const totalItens = carrinho.reduce((acc, item) => acc + item.quantidade, 0);
    document.getElementById('carrinho-qtd').innerText = totalItens;

    // Atualizar Modal do Carrinho
    const containerItens = document.getElementById('itens-carrinho');
    containerItens.innerHTML = '';
    let subtotal = 0;

    carrinho.forEach(item => {
        const totalItem = item.preco * item.quantidade;
        subtotal += totalItem;

        const div = document.createElement('div');
        div.style.display = 'flex';
        div.style.justifySpaceBetween = 'space-between';
        div.style.marginBottom = '10px';
        div.innerHTML = `
            <span>${item.nome} (${item.quantidade}x)</span>
            <span>R$ ${totalItem.toFixed(2)}</span>
            <button onclick="removerDoCarrinho(${item.idProduto})">❌</button>
        `;
        containerItens.appendChild(div);
    });

    document.getElementById('cart-subtotal').innerText = subtotal.toFixed(2);
    document.getElementById('cart-total').innerText = subtotal.toFixed(2);
}

function removerDoCarrinho(idProduto) {
    carrinho = carrinho.filter(item => item.idProduto !== idProduto);
    atualizarCarrinhoUI();
}

// Aplicar Cupom consumindo o BD via API
async function aplicarCupom() {
    const codigo = document.getElementById('input-cupom').value;
    if (!codigo) return;

    try {
        const response = await fetch(`${API_BASE_URL}/cupons/validar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ codigo })
        });
        const res = await response.json();
        
        if (res.valido) {
            document.getElementById('cart-desconto').innerText = res.valorDesconto.toFixed(2);
            const subtotal = parseFloat(document.getElementById('cart-subtotal').innerText);
            document.getElementById('cart-total').innerText = (subtotal - res.valorDesconto).toFixed(2);
            alert("Cupom aplicado!");
        } else {
            alert("Cupom inválido ou expirado.");
        }
    } catch (e) {
        alert("Erro ao validar cupom.");
    }
}

// Integração de Login/Cadastro
async function realizarLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const senha = document.getElementById('login-senha').value;

    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, senha })
        });

        if (response.ok) {
            usuarioLogado = await response.json();
            alert(`Bem-vindo, ${usuarioLogado.nome}!`);
            fecharModal('modal-login');
            document.getElementById('btn-login-modal').innerText = usuarioLogado.nome;
        } else {
            alert("Credenciais inválidas.");
        }
    } catch (error) {
        console.error("Erro na autenticação:", error);
    }
}

// Chatbot "Chuchu"
function toggleChatbot() {
    const box = document.getElementById('chatbot-box');
    box.classList.toggle('hidden');
}

async function enviarMensagemChat() {
    const input = document.getElementById('chat-input');
    const msgTexto = input.value.trim();
    if (!msgTexto) return;

    const boxMensagens = document.getElementById('chatbot-mensagens');

    // Adiciona mensagem do usuário
    const userDiv = document.createElement('div');
    userDiv.className = 'msg user';
    userDiv.innerText = msgTexto;
    boxMensagens.appendChild(userDiv);

    input.value = '';

    try {
        const response = await fetch(`${API_BASE_URL}/chatbot`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ texto: msgTexto, idUsuario: usuarioLogado ? usuarioLogado.idUsuario : null })
        });
        const data = await response.json();

        const botDiv = document.createElement('div');
        botDiv.className = 'msg bot';
        botDiv.innerText = data.resposta || "Desculpe, não entendi sua dúvida.";
        boxMensagens.appendChild(botDiv);
    } catch (e) {
        const botDiv = document.createElement('div');
        botDiv.className = 'msg bot';
        botDiv.innerText = "No momento estou offline, tente novamente mais tarde.";
        boxMensagens.appendChild(botDiv);
    }

    boxMensagens.scrollTop = boxMensagens.scrollHeight;
}

// Utilitários de Modal
function abrirModal(id) { document.getElementById(id).style.display = 'block'; }
function fecharModal(id) { document.getElementById(id).style.display = 'none'; }
function alternarFormCadastro() { document.getElementById('form-cadastro').classList.toggle('hidden'); }