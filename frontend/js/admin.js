let CATEGORIAS = [], MARCAS = [], TODOS = [], RECEITAS_ADMIN = [];
const STATUSES = ["pendente", "pago", "enviado", "entregue", "cancelado"];
const STATUS_LBL = {pendente: "Pendente", pago: "Pago",
  enviado: "Enviado", entregue: "Entregue", cancelado: "Cancelado"};
const dataHora = iso => {
  try { return new Date(iso).toLocaleString("pt-BR", {dateStyle: "short", timeStyle: "short"}); }
  catch (e) { return iso; }
};

async function initAdmin() {
  try {
    const me = await apiFetch("/api/me");
    if (!me.usuario.admin) {
      store.set("iz_flash", "Acesso restrito a administradores");
      location.href = "catalogo.html";
      return;
    }
    $("#adminInfo").textContent = "Logado como " + me.usuario.nome + " (" + me.usuario.email + ")";
  } catch (e) {
    store.set("iz_flash", "Entre como administrador para acessar o painel");
    location.href = "entrar.html";
    return;
  }
  ligarAbas();
  ligarProdutos();
  ligarCategorias();
  ligarMarcas();
  ligarReceitas();
  await Promise.all([carregarCategorias(), carregarMarcas()]);
  await Promise.all([carregarProdutosAdmin(), carregarReceitasAdmin(), carregarPedidosAdmin()]);
}

function ligarAbas() {
  $$("#adminTabs button").forEach(b => b.onclick = () => {
    $$("#adminTabs button").forEach(x => x.classList.toggle("on", x === b));
    ["produtos", "categorias", "marcas", "receitas", "pedidos"].forEach(t =>
      $("#tab-" + t).hidden = t !== b.dataset.tab);
  });
}

async function carregarCategorias() {
  const d = await apiFetch("/api/categorias");
  CATEGORIAS = d.categorias || [];
  $("#listaCategorias").innerHTML = CATEGORIAS.map(c => `
    <div class="linha-admin">
      <span><b>${c.nome}</b> <small>(${c.tipo === "restricao" ? "restrição" : "produto"})</small></span>
      <span class="acoes">
        <button class="btn sm ghost" data-editar-cat="${c.id}">Renomear</button>
        <button class="btn sm ghost" data-excluir-cat="${c.id}">Excluir</button>
      </span>
    </div>`).join("");
  $("#pr-cats").innerHTML = CATEGORIAS.map(c => `
    <label><input type="checkbox" value="${c.id}"> ${c.nome}</label>`).join("");
}

async function carregarMarcas() {
  const d = await apiFetch("/api/marcas");
  MARCAS = d.marcas || [];
  $("#listaMarcas").innerHTML = MARCAS.map(m => `
    <div class="linha-admin">
      <b>${m.nome}</b>
      <span class="acoes">
        <button class="btn sm ghost" data-editar-marca="${m.id}">Renomear</button>
        <button class="btn sm ghost" data-excluir-marca="${m.id}">Excluir</button>
      </span>
    </div>`).join("");
  $("#pr-marca").innerHTML = MARCAS.map(m =>
    `<option value="${m.id}">${m.nome}</option>`).join("");
}

async function carregarProdutosAdmin() {
  const d = await apiFetch("/api/produtos/todos");
  TODOS = d.produtos || [];
  $("#listaProdutos").innerHTML = TODOS.length ? TODOS.map(p => `
    <div class="linha-admin">
      <span style="flex:1;min-width:220px">
        <b>#${p.id} ${p.nome}</b><br>
        <small>${brl(p.preco)} · estoque ${p.estoque} · ${p.marca}</small>
        ${p.destaque ? '<span class="tag">destaque</span>' : ""}
        ${p.ativo ? "" : '<span class="tag inativo">inativo</span>'}
        ${p.ativo && p.estoque === 0 ? '<span class="tag zero">sem estoque</span>' : ""}
      </span>
      <span class="acoes">
        <button class="btn sm ghost" data-editar-prod="${p.id}">Editar</button>
        ${p.ativo
          ? `<button class="btn sm ghost" data-excluir-prod="${p.id}">Remover</button>`
          : `<button class="btn sm" data-reativar-prod="${p.id}">Reativar</button>`}
      </span>
    </div>`).join("") : `<div class="empty">Nenhum produto cadastrado.</div>`;
}

function ligarProdutos() {
  const form = $("#formProduto");
  const fechar = () => { form.hidden = true; form.reset(); $("#pr-id").value = ""; };
  $("#novoProduto").onclick = () => { fechar(); form.hidden = false; $("#pr-nome").focus(); };
  $("#cancelarProduto").onclick = fechar;

  $("#listaProdutos").onclick = async e => {
    const ed = e.target.closest("[data-editar-prod]");
    const ex = e.target.closest("[data-excluir-prod]");
    const re = e.target.closest("[data-reativar-prod]");
    if (re) {
      try {
        await apiFetch("/api/produtos/" + re.dataset.reativarProd + "/reativar", {metodo: "PUT"});
        toast("Produto reativado");
        await carregarProdutosAdmin();
        carregarProdutos().then(renderCart);
      } catch (erro) { toast(erro.message); }
      return;
    }
    if (ed) {
      const p = TODOS.find(x => x.id === +ed.dataset.editarProd);
      if (!p) return;
      form.hidden = false;
      $("#pr-id").value = p.id;
      $("#pr-nome").value = p.nome;
      $("#pr-desc").value = p.descricao || "";
      $("#pr-preco").value = p.preco;
      $("#pr-estoque").value = p.estoque;
      $("#pr-destaque").checked = !!p.destaque;
      $("#pr-img").value = "";
      $("#pr-marca").value = String(MARCAS.find(m => m.nome === p.marca)?.id || MARCAS[0]?.id || "");
      $$("#pr-cats input").forEach(chk =>
        chk.checked = (p.categoria_ids || []).includes(+chk.value));
      form.scrollIntoView({behavior: "smooth", block: "start"});
    }
    if (ex) {
      const p = TODOS.find(x => x.id === +ex.dataset.excluirProd);
      if (!p || !confirm("Remover \"" + p.nome + "\" do catálogo?")) return;
      try { await apiFetch("/api/produtos/" + p.id, {metodo: "DELETE"});
        toast("Produto removido"); await carregarProdutosAdmin(); carregarProdutos().then(renderCart);
      } catch (erro) { toast(erro.message); }
    }
  };

  form.onsubmit = async e => {
    e.preventDefault();
    const id = $("#pr-id").value;
    const cats = $$("#pr-cats input:checked").map(c => c.value).join(",");
    const fd = new FormData();
    fd.append("nome", $("#pr-nome").value.trim());
    fd.append("descricao", $("#pr-desc").value.trim());
    fd.append("preco", $("#pr-preco").value);
    fd.append("estoque", $("#pr-estoque").value);
    fd.append("marca_id", $("#pr-marca").value);
    fd.append("categorias", cats);
    fd.append("destaque", $("#pr-destaque").checked ? "true" : "false");
    const arquivo = $("#pr-img").files[0];
    if (arquivo) fd.append("imagem", arquivo);
    try {
      await apiFetch("/api/produtos" + (id ? "/" + id : ""),
        {metodo: id ? "PUT" : "POST", formData: fd});
      toast(id ? "Produto atualizado" : "Produto criado");
      fechar();
      await carregarProdutosAdmin();
      carregarProdutos().then(renderCart);
    } catch (erro) { toast(erro.message); }
  };
}

function ligarCategorias() {
  $("#formCategoria").onsubmit = async e => {
    e.preventDefault();
    try {
      await apiFetch("/api/categorias", {metodo: "POST", corpo: {
        nome: $("#cat-nome").value.trim(), tipo: $("#cat-tipo").value}});
      $("#cat-nome").value = "";
      toast("Categoria criada");
      await carregarCategorias();
      await carregarProdutosAdmin();
    } catch (erro) { toast(erro.message); }
  };
  $("#listaCategorias").onclick = async e => {
    const ed = e.target.closest("[data-editar-cat]");
    const ex = e.target.closest("[data-excluir-cat]");
    try {
      if (ed) {
        const c = CATEGORIAS.find(x => x.id === +ed.dataset.editarCat);
        const nome = prompt("Novo nome da categoria:", c.nome);
        if (!nome || nome.trim() === c.nome) return;
        await apiFetch("/api/categorias/" + c.id, {metodo: "PUT", corpo: {nome: nome.trim()}});
        toast("Categoria atualizada");
        await carregarCategorias();
        await carregarProdutosAdmin();
      }
      if (ex) {
        const c = CATEGORIAS.find(x => x.id === +ex.dataset.excluirCat);
        if (!confirm("Excluir a categoria \"" + c.nome + "\"? Os vínculos com produtos serão removidos.")) return;
        await apiFetch("/api/categorias/" + c.id, {metodo: "DELETE"});
        toast("Categoria excluída");
        await carregarCategorias();
        await carregarProdutosAdmin();
      }
    } catch (erro) { toast(erro.message); }
  };
}

function ligarMarcas() {
  $("#formMarca").onsubmit = async e => {
    e.preventDefault();
    try {
      await apiFetch("/api/marcas", {metodo: "POST", corpo: {nome: $("#marca-nome").value.trim()}});
      $("#marca-nome").value = "";
      toast("Marca criada");
      await carregarMarcas();
      await carregarProdutosAdmin();
    } catch (erro) { toast(erro.message); }
  };
  $("#listaMarcas").onclick = async e => {
    const ed = e.target.closest("[data-editar-marca]");
    const ex = e.target.closest("[data-excluir-marca]");
    try {
      if (ed) {
        const m = MARCAS.find(x => x.id === +ed.dataset.editarMarca);
        const nome = prompt("Novo nome da marca:", m.nome);
        if (!nome || nome.trim() === m.nome) return;
        await apiFetch("/api/marcas/" + m.id, {metodo: "PUT", corpo: {nome: nome.trim()}});
        toast("Marca atualizada");
        await carregarMarcas();
        await carregarProdutosAdmin();
      }
      if (ex) {
        const m = MARCAS.find(x => x.id === +ex.dataset.excluirMarca);
        if (!confirm("Excluir a marca \"" + m.nome + "\"?")) return;
        await apiFetch("/api/marcas/" + m.id, {metodo: "DELETE"});
        toast("Marca excluída");
        await carregarMarcas();
        await carregarProdutosAdmin();
      }
    } catch (erro) { toast(erro.message); }
  };
}

async function carregarReceitasAdmin() {
  const d = await apiFetch("/api/receitas");
  RECEITAS_ADMIN = d.receitas || [];
  $("#listaReceitas").innerHTML = RECEITAS_ADMIN.length ? RECEITAS_ADMIN.map(r => `
    <div class="linha-admin">
      <span style="flex:1;min-width:230px">
        <b>#${r.id} ${r.titulo}</b><br>
        <small>${r.categoria} · ${dataHora(r.criado_em)}</small>
      </span>
      <span class="acoes">
        <button class="btn sm ghost" data-editar-rec="${r.id}">Editar</button>
        <button class="btn sm ghost" data-excluir-rec="${r.id}">Excluir</button>
      </span>
    </div>`).join("") : `<div class="empty">Nenhuma receita cadastrada.</div>`;
}

function linhaIngrediente(produtoId = "", quantidade = "") {
  const opcoes = TODOS.map(p =>
    `<option value="${p.id}" ${p.id === +produtoId ? "selected" : ""}>${p.nome}</option>`).join("");
  return `<div class="dupla" data-ing style="margin-bottom:8px">
    <div class="field"><select data-ing-prod><option value="">Produto...</option>${opcoes}</select></div>
    <div class="field"><input data-ing-qtd placeholder="Quantidade (ex.: 1 xícara)" value="${quantidade}"></div>
    <button type="button" class="btn sm ghost" data-rem-ing>Remover</button>
  </div>`;
}

function ligarReceitas() {
  const form = $("#formReceita");
  const fechar = () => { form.hidden = true; form.reset(); $("#rc-id").value = ""; $("#rc-ings").innerHTML = ""; };
  const abrir = async (receita) => {
    form.hidden = false;
    $("#rc-id").value = receita ? receita.id : "";
    $("#rc-titulo").value = receita ? receita.titulo : "";
    $("#rc-cat").value = receita ? receita.categoria : "";
    $("#rc-texto").value = receita ? receita.texto : "";
    $("#rc-imagem").value = receita ? receita.imagem : "";
    $("#rc-ings").innerHTML = "";
    let ings = receita && receita.ingredientes ? receita.ingredientes : [];
    if (!receita) ings = [{produto_id: "", quantidade: ""}];
    ings.forEach(i => $("#rc-ings").insertAdjacentHTML("beforeend",
      linhaIngrediente(i.produto_id, i.quantidade)));
    form.scrollIntoView({behavior: "smooth", block: "start"});
  };

  $("#novaReceita").onclick = () => abrir(null);
  $("#rc-cancelar").onclick = fechar;
  $("#rc-add-ing").onclick = () =>
    $("#rc-ings").insertAdjacentHTML("beforeend", linhaIngrediente());
  $("#rc-ings").onclick = e => {
    const rem = e.target.closest("[data-rem-ing]");
    if (rem) rem.closest("[data-ing]").remove();
  };

  $("#listaReceitas").onclick = async e => {
    const ed = e.target.closest("[data-editar-rec]");
    const ex = e.target.closest("[data-excluir-rec]");
    try {
      if (ed) {
        const d = await apiFetch("/api/receitas/" + ed.dataset.editarRec);
        abrir(d.receita);
      }
      if (ex) {
        const r = RECEITAS_ADMIN.find(x => x.id === +ex.dataset.excluirRec);
        if (!confirm("Excluir a receita \"" + r.titulo + "\"?")) return;
        await apiFetch("/api/receitas/" + r.id, {metodo: "DELETE"});
        toast("Receita excluída");
        await carregarReceitasAdmin();
        carregarReceitas();
      }
    } catch (erro) { toast(erro.message); }
  };

  form.onsubmit = async e => {
    e.preventDefault();
    const id = $("#rc-id").value;
    const ingredientes = $$("#rc-ings [data-ing]")
      .map(l => ({
        produto_id: l.querySelector("[data-ing-prod]").value,
        quantidade: l.querySelector("[data-ing-qtd]").value.trim()
      }))
      .filter(i => i.produto_id && i.quantidade);
    try {
      await apiFetch("/api/receitas" + (id ? "/" + id : ""), {metodo: id ? "PUT" : "POST", corpo: {
        titulo: $("#rc-titulo").value.trim(),
        categoria: $("#rc-cat").value.trim(),
        texto: $("#rc-texto").value.trim(),
        imagem: $("#rc-imagem").value.trim(),
        ingredientes
      }});
      toast(id ? "Receita atualizada" : "Receita criada");
      fechar();
      await carregarReceitasAdmin();
      carregarReceitas();
    } catch (erro) { toast(erro.message); }
  };
}

async function carregarPedidosAdmin() {
  const d = await apiFetch("/api/pedidos");
  const pedidos = d.pedidos || [];
  $("#listaPedidos").innerHTML = pedidos.length ? pedidos.map(p => `
    <div class="linha-admin pedido-linha" id="admin-pedido-${p.id}">
      <span style="flex:1;min-width:230px">
        <b>#${p.id} · ${p.usuario_nome || "usuário " + p.usuario_id}</b><br>
        <small>${dataHora(p.criado_em)} · ${p.forma_pagamento.toUpperCase()} · ${p.cep_entrega}</small><br>
        <b>${brl(p.total)}</b>
      </span>
      <span class="acoes">
        <span class="tag st-${p.status}">${STATUS_LBL[p.status] || p.status}</span>
        <select data-status="${p.id}">${STATUSES.map(s =>
          `<option value="${s}" ${s === p.status ? "selected" : ""}>${STATUS_LBL[s]}</option>`).join("")}</select>
        <button class="btn sm ghost" data-itens-pedido="${p.id}">Itens</button>
      </span>
      <div class="itens" id="admin-itens-${p.id}" hidden></div>
    </div>`).join("") : `<div class="empty">Nenhum pedido.</div>`;

  $("#listaPedidos").onchange = async e => {
    const sel = e.target.closest("[data-status]");
    if (!sel) return;
    try {
      await apiFetch("/api/pedidos/" + sel.dataset.status + "/status",
        {metodo: "PUT", corpo: {status: sel.value}});
      toast("Status atualizado");
      await carregarPedidosAdmin();
      carregarProdutos().then(renderCart);
    } catch (erro) { toast(erro.message); await carregarPedidosAdmin(); }
  };
  $("#listaPedidos").onclick = async e => {
    const bt = e.target.closest("[data-itens-pedido]");
    if (!bt) return;
    const alvo = $("#admin-itens-" + bt.dataset.itensPedido);
    if (!alvo.hidden) { alvo.hidden = true; return; }
    try {
      const det = await apiFetch("/api/pedidos/" + bt.dataset.itensPedido);
      alvo.innerHTML = (det.pedido.itens || []).map(i =>
        `<div class="row"><span>${i.quantidade}× ${i.nome}</span><span>${brl(i.preco_unitario * i.quantidade)}</span></div>`).join("");
      alvo.hidden = false;
    } catch (erro) { toast(erro.message); }
  };
  $("#recarregarPedidos").onclick = () => carregarPedidosAdmin();
}

initAdmin();
