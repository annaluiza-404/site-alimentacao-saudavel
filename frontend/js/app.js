const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const brl=v=>v.toLocaleString("pt-BR",{style:"currency",currency:"BRL"});
const store={get(k){try
    {return JSON.parse(localStorage.getItem(k))}
    catch(e){return null}},set(k,v)
    {try{localStorage.setItem(k,JSON.stringify(v))}
    catch(e){}}};

function toast(m){const t=$("#toast");
    t.textContent=m;
    t.classList.add("show");
    clearTimeout(toast.h);
    toast.h=setTimeout(()=>t.classList.remove("show"),2400)}

window.imgFail=img=>{const s=document.createElement("span");s.textContent=img.dataset.fb;s.style.cssText="display:grid;place-items:center;width:100%;height:100%;min-height:120px;font-size:3rem";img.replaceWith(s)};
const pic=(src,fb,alt)=>`<img src="${src}" alt="${alt}" data-fb="${fb}" loading="lazy" onerror="imgFail(this)">`;
let cart=store.get("iz_cart")||[],user=store.get("iz_user");

const CODIGO_TAG=Object.fromEntries(Object.entries(TAGS).map(([k,v])=>[v,k]));
const EMOJI_CAT={"Pães e massas":"🍞","Doces e biscoitos":"🍪","Snacks":"🥨","Bebidas":"🥛","Mercearia":"🌾"};
const urlImagem=img=>!img?"":(/^https?:/.test(img)?img:(img.startsWith("uploads/")?API+"/"+img:img));
const rotulo=p=>p.c>=0?CATS[p.c]:(p.marca||"");
let PRODUTOS=[];

function mapProduto(p){
 const cats=p.categorias||[];
 const catProd=cats.find(c=>CATS.includes(c))||"";
 return {id:p.id,n:p.nome,p:p.preco,estoque:p.estoque,img:urlImagem(p.imagem),
  e:EMOJI_CAT[catProd]||"🌿",t:cats.map(c=>CODIGO_TAG[c]).filter(Boolean),
  c:CATS.indexOf(catProd),marca:p.marca,destaque:p.destaque};
}
async function carregarProdutos(){const d=await apiFetch("/api/produtos");PRODUTOS=(d.produtos||[]).map(mapProduto);return PRODUTOS}
const acharProduto=id=>PRODUTOS.find(x=>x.id===id);

const card=p=>`<div class="card"><div class="img">${pic(p.img,p.e,p.n)}</div><div class="body"><small>${rotulo(p)}</small><h3>${p.n}</h3>
<div class="tags">${p.t.slice(0,3).map(k=>`<span class="tag">${TAGS[k]}</span>`).join("")}</div>
<div class="row price"><span>${brl(p.p)}</span><button class="btn sm" data-add="${p.id}">Adicionar</button></div></div></div>`;
const postCard=b=>`<a class="card post" href="post.html?id=${b.id}"><div class="img">${pic(b.img,b.e,b.t)}</div><div class="body"><span class="tag" style="align-self:flex-start">${b.cat}</span><h3>${b.t}</h3><small>${b.d}</small></div></a>`;

function renderCart(){
    $("#count").textContent=cart.reduce((s,i)=>s+i.q,0);
    $("#cartList").innerHTML=cart.length?cart.map(i=>{const p=acharProduto(i.id);
        return p?`<div class="item"><div class="e">${pic(p.img,p.e,p.n)}</div><div class="i"><b>${p.n}</b><br><small>${brl(p.p)}</small></div><div class="qty"><button data-dec="${p.id}">−</button>${i.q}<button data-add="${p.id}" data-quiet="1">+</button></div></div>`
                :`<div class="item"><div class="i"><b>Produto #${i.id}</b><br><small>indisponível</small></div></div>`}).join(""):`<p class="empty">Seu carrinho está vazio 🌱</p>`;
    $("#total").textContent=brl(cart.reduce((s,i)=>{const p=acharProduto(i.id);return s+(p?i.q*p.p:0)},0));
}
const saveCart=()=>store.set("iz_cart",cart);

function add(id,quiet){
    const prod=acharProduto(id);
    if(!prod)return toast("Produto indisponível");
    const i=cart.find(x=>x.id===id);
    if((i?i.q:0)>=prod.estoque)return toast("Estoque máximo atingido para este produto");
    i?i.q++:cart.push({id,q:1});saveCart();
    renderCart();
    if(!quiet)toast("Adicionado ao carrinho ✔")
}

function dec(id){
    const i=cart.find(x=>x.id===id);
    if(!i)return;if(--i.q<=0)cart=cart.filter(x=>x!==i);
    saveCart();
    renderCart()
}

const openCart=o=>{$("#drawer").classList.toggle("open",o);
    $("#scrim").classList.toggle("open",o)};
$("#cartBtn").onclick=()=>openCart(true);
$("#closeCart").onclick=$("#scrim").onclick=()=>openCart(false);

const subtotalCarrinho=()=>cart.reduce((s,i)=>{const p=acharProduto(i.id);return s+(p?i.q*p.p:0)},0);
let freteAtual=0,cupomAtual=null;

function construirCheckout(){
 const drawer=$("#drawer");if(!drawer||$("#checkoutBox"))return;
 const box=document.createElement("div");box.id="checkoutBox";box.hidden=true;
 box.innerHTML=`<form id="fCheckout" novalidate>
  <div class="field"><label for="ck-cep">CEP de entrega</label>
    <input id="ck-cep" inputmode="numeric" placeholder="00000-000" autocomplete="postal-code">
    <div class="err" id="ck-cep-err"></div></div>
  <div class="field"><label for="ck-log">Endereço</label><input id="ck-log" autocomplete="address-line1"></div>
  <div class="row" style="gap:8px">
    <div class="field" style="flex:1"><label for="ck-num">Número</label><input id="ck-num"></div>
    <div class="field" style="flex:2"><label for="ck-comp">Complemento</label><input id="ck-comp"></div>
  </div>
  <div class="field"><label for="ck-bairro">Bairro</label><input id="ck-bairro"></div>
  <div class="row" style="gap:8px">
    <div class="field" style="flex:2"><label for="ck-cidade">Cidade</label><input id="ck-cidade"></div>
    <div class="field" style="flex:1"><label for="ck-uf">UF</label><input id="ck-uf" maxlength="2" placeholder="SP"></div>
  </div>
  <div class="field"><label for="ck-cupom">Cupom de desconto</label>
    <div class="row" style="gap:8px"><input id="ck-cupom" placeholder="Opcional">
      <button type="button" class="btn sm ghost" id="ck-aplicar">Aplicar</button>
      <button type="button" class="btn sm ghost" id="ck-remover" hidden>Remover</button></div>
    <div class="err" id="ck-cupom-msg"></div></div>
  <div class="field"><label for="ck-pg">Forma de pagamento</label>
    <select id="ck-pg"><option value="pix">Pix</option><option value="cartao">Cartão</option><option value="boleto">Boleto</option></select></div>
  <div id="ck-resumo" style="display:flex;flex-direction:column;gap:4px;background:var(--soft);border-radius:12px;padding:12px;font-size:.9rem"></div>
  <div class="row" style="gap:8px;margin-top:12px">
    <button type="button" class="btn ghost" id="ck-voltar">Voltar</button>
    <button class="btn" style="flex:1;justify-content:center">Confirmar pedido</button></div>
 </form>`;
 drawer.appendChild(box);

 const resumo=()=>{
  const sub=subtotalCarrinho(),desc=cupomAtual?cupomAtual.desconto:0;
  const total=Math.max(sub+freteAtual-desc,0);
  $("#ck-resumo").innerHTML=`<div class="row"><span>Subtotal</span><b>${brl(sub)}</b></div>
   <div class="row"><span>Frete</span><b>${freteAtual?brl(freteAtual):"informe o CEP"}</b></div>
   ${desc?`<div class="row"><span>Desconto (${cupomAtual.codigo})</span><b>− ${brl(desc)}</b></div>`:""}
   <div class="row"><span>Total</span><b>${brl(total)}</b></div>`;
 };

 $("#ck-cep").oninput=async e=>{
  const d=e.target.value.replace(/\D/g,"");
  $("#ck-cep-err").textContent="";freteAtual=0;cupomAtual=null;$("#ck-remover").hidden=true;resumo();
  if(d.length!==8)return;
  try{const r=await apiFetch("/api/frete",{metodo:"POST",corpo:{cep:d}});freteAtual=r.frete.valor;resumo()}
  catch(ex){$("#ck-cep-err").textContent=ex.message}
 };

 $("#ck-aplicar").onclick=async()=>{
  const codigo=$("#ck-cupom").value.trim();const msg=$("#ck-cupom-msg");msg.textContent="";
  if(!codigo)return;
  try{const r=await apiFetch("/api/cupom/validar",{metodo:"POST",
    corpo:{codigo,subtotal:subtotalCarrinho(),frete:freteAtual}});
   cupomAtual={codigo:r.cupom.codigo,desconto:r.cupom.desconto};
   $("#ck-remover").hidden=false;msg.textContent="Cupom aplicado ✔";resumo();
  }catch(ex){cupomAtual=null;msg.textContent=ex.message;resumo()}
 };
 $("#ck-remover").onclick=()=>{cupomAtual=null;$("#ck-cupom").value="";$("#ck-cupom-msg").textContent="";$("#ck-remover").hidden=true;resumo()};
 $("#ck-voltar").onclick=()=>{box.hidden=true;$("#checkout").hidden=false};

 $("#fCheckout").onsubmit=async e=>{
  e.preventDefault();
  if(!freteAtual)return toast("Informe um CEP válido para calcular o frete");
  const endereco={cep:$("#ck-cep").value,logradouro:$("#ck-log").value.trim(),
    numero:$("#ck-num").value.trim(),complemento:$("#ck-comp").value.trim(),
    bairro:$("#ck-bairro").value.trim(),cidade:$("#ck-cidade").value.trim(),
    estado:$("#ck-uf").value.trim().toUpperCase()};
  if(!endereco.logradouro||!endereco.numero||!endereco.bairro||!endereco.cidade||!endereco.estado)
    return toast("Preencha o endereço completo");
  try{
   await apiFetch("/api/pedidos",{metodo:"POST",corpo:{
     itens:cart.map(i=>({id:i.id,q:i.q})),endereco,
     cupom:cupomAtual?cupomAtual.codigo:null,forma_pagamento:$("#ck-pg").value}});
   cart=[];saveCart();renderCart();openCart(false);
   store.set("iz_flash","Pedido realizado! Acompanhe em Meus pedidos 💚");
   location.href="pedidos.html";
  }catch(ex){
   if(ex.status===400&&/CPF/.test(ex.message)){store.set("iz_flash",ex.message);location.href="entrar.html";return}
   toast(ex.message);
  }
 };
}

function abrirCheckout(){
 if(!$("#checkout"))return;
 if(!cart.length)return toast("Seu carrinho está vazio");
 if(!user){store.set("iz_flash","Entre para finalizar a compra");location.href="entrar.html";return}
 if(!user.cpf){store.set("iz_flash","Complete seu cadastro com CPF para finalizar a compra");location.href="entrar.html";return}
 construirCheckout();
 $("#checkout").hidden=true;$("#checkoutBox").hidden=false;
 $("#ck-resumo").innerHTML="";freteAtual=0;cupomAtual=null;
 $("#ck-cupom").value="";$("#ck-cupom-msg").textContent="";$("#ck-remover").hidden=true;
 $("#ck-resumo").innerHTML=`<div class="row"><span>Subtotal</span><b>${brl(subtotalCarrinho())}</b></div>
  <div class="row"><span>Frete</span><b>informe o CEP</b></div>
  <div class="row"><span>Total</span><b>${brl(subtotalCarrinho())}</b></div>`;
}
$("#checkout").onclick=abrirCheckout;

document.addEventListener("click",e=>{
 const a=e.target.closest("[data-add]");if(a)return add(+a.dataset.add,a.dataset.quiet);
 const d=e.target.closest("[data-dec]");if(d)dec(+d.dataset.dec)});
$("#menu").onclick=()=>$("#nav").classList.toggle("open");

function authUI(){
 $("#navLogin").textContent=user?"Olá, "+user.name.split(" ")[0]:"Entrar";
 if(!$("#authBox"))return;
 $("#authBox").hidden=!!user;$("#userBox").hidden=!user;
 if(user){$("#hello").textContent="Olá, "+user.name.split(" ")[0]+"!";$("#uinfo").textContent=user.email+" · Preferência: "+(user.r||"—")+(user.cpf?"":" · CPF pendente")}
}
async function carregarSessao(){
 try{const d=await apiFetch("/api/me");user={id:d.usuario.id,name:d.usuario.nome,email:d.usuario.email,admin:d.usuario.admin,cpf:d.usuario.cpf,r:d.usuario.preferencia};store.set("iz_user",user)}
 catch(e){user=null;store.set("iz_user",null)}
 authUI()
}

function initHome(){
$("#chips").innerHTML=[
  ["sg","images/chips/sem-gluten.png","🌾"],
  ["sl","images/chips/sem-lactose.png","🥛"],
  ["vg","images/chips/vegano.png","🌱"],
  ["sa","images/chips/sem-acucar.png","🍬"],
  ["so","images/chips/sem-ovo.png","🥚"]
].map(([k,img,e])=>`<a class="chip" href="catalogo.html?tag=${k}"><b>${pic(img,e,TAGS[k])}</b>${TAGS[k]}</a>`).join("");
 const destaques=PRODUTOS.filter(p=>p.destaque);
 $("#featured").innerHTML=(destaques.length?destaques:PRODUTOS.slice(0,4)).map(card).join("");
 const homeBlog=$("#homeBlog");
 if(homeBlog)homeBlog.innerHTML=POSTS.slice(0,3).map(postCard).join("");
 const newsForm=$("#newsForm");
 if(newsForm)newsForm.onsubmit=e=>{e.preventDefault();e.target.reset();toast("Inscrição confirmada! 💌")};
}

function initShop(){
 const u=new URLSearchParams(location.search);
 const fresh=()=>({tags:new Set(u.get("tag")&&TAGS[u.get("tag")]?[u.get("tag")]:[]),cat:"",q:u.get("q")||"",pr:60,ord:"rel"});
 let st=fresh();

const drawF=()=>{
  $("#tagF").innerHTML=Object.entries(TAGS).map(([k,v])=>`<label class="check"><input type="checkbox" value="${k}" ${st.tags.has(k)?"checked":""}> ${v}</label>`).join("");
  $("#cat").innerHTML=`<option value="">Todas</option>`+CATS.map((c,i)=>`<option value="${i}" ${String(i)===st.cat?"selected":""}>${c}</option>`).join("");
  $("#q").value=st.q;$("#pr").value=st.pr;$("#ord").value=st.ord;$("#pv").textContent=brl(+st.pr)};
 
 const drawL=()=>{
  const semAcento=v=>v.normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase();
  let r=PRODUTOS.filter(p=>[...st.tags].every(t=>p.t.includes(t))&&(st.cat===""||p.c===+st.cat)&&p.p<=st.pr&&semAcento(p.n).includes(semAcento(st.q)));
  if(st.ord==="asc")r.sort((a,b)=>a.p-b.p);if(st.ord==="desc")r.sort((a,b)=>b.p-a.p);if(st.ord==="az")r.sort((a,b)=>a.n.localeCompare(b.n,"pt-BR"));
  $("#res").textContent=r.length+(r.length===1?" produto encontrado":" produtos encontrados");
  $("#list").innerHTML=r.length?r.map(card).join(""):`<div class="empty">😕 Nenhum produto com esses filtros.<br>Tente remover alguma restrição.</div>`};
 $("#tagF").addEventListener("change",e=>{e.target.checked?st.tags.add(e.target.value):st.tags.delete(e.target.value);drawL()});
 $("#cat").onchange=e=>{st.cat=e.target.value;drawL()};
 $("#q").oninput=e=>{st.q=e.target.value;drawL()};
 $("#pr").oninput=e=>{st.pr=+e.target.value;$("#pv").textContent=brl(st.pr);drawL()};
 $("#ord").onchange=e=>{st.ord=e.target.value;drawL()};
 $("#clear").onclick=()=>{st={tags:new Set(),cat:"",q:"",pr:60,ord:"rel"};drawF();drawL()};
 drawF();drawL();
}

function initAuth(){
 const err=(el,m)=>{el.parentElement.querySelector(".err").textContent=m||"";return !m};
 const okMail=v=>/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
 const login=(u,msg)=>{user=u;store.set("iz_user",u);store.set("iz_flash",msg);location.href="catalogo.html"};
 $$(".tabs button").forEach(b=>b.onclick=()=>{$$(".tabs button").forEach(x=>x.classList.toggle("on",x===b));$("#fIn").hidden=b.dataset.t!=="in";$("#fUp").hidden=b.dataset.t!=="up"});
 $("#fUp").onsubmit=async e=>{e.preventDefault();const n=$("#su-n"),m=$("#su-e"),s=$("#su-s");
  const v=[err(n,n.value.trim().length<2?"Informe seu nome":""),err(m,okMail(m.value)?"":"E-mail inválido"),err(s,s.value.length<6?"Mínimo de 6 caracteres":"")];
  if(v.includes(false))return;
  try{const d=await apiFetch("/api/registro",{metodo:"POST",corpo:{nome:n.value.trim(),email:m.value.toLowerCase(),senha:s.value,preferencia:$("#su-r").value}});
   login({id:d.usuario.id,name:d.usuario.nome,email:d.usuario.email,admin:d.usuario.admin,cpf:d.usuario.cpf,r:d.usuario.preferencia},"Conta criada! Bem-vindo(a) 🌿")}
  catch(ex){err(m,ex.message)}};
 $("#fIn").onsubmit=async e=>{e.preventDefault();const m=$("#li-e"),s=$("#li-s");
  if(!err(m,okMail(m.value)?"":"E-mail inválido")|!err(s,s.value?"":"Informe a senha"))return;
  try{const d=await apiFetch("/api/login",{metodo:"POST",corpo:{email:m.value.toLowerCase(),senha:s.value}});
   login({id:d.usuario.id,name:d.usuario.nome,email:d.usuario.email,admin:d.usuario.admin,cpf:d.usuario.cpf,r:d.usuario.preferencia},"Olá de novo, "+d.usuario.nome.split(" ")[0]+"!")}
  catch(ex){err(s,ex.message)}};
 $("#logout").onclick=async()=>{try{await apiFetch("/api/logout",{metodo:"POST"})}catch(e){}user=null;store.set("iz_user",null);authUI();toast("Você saiu da conta")};
 const preencherPerfil=()=>{if(!user)return;
  $("#pf-nome").value=user.name||"";$("#pf-cpf").value=user.cpf||"";$("#pf-pref").value=user.r||""};
 preencherPerfil();
 $("#fPerfil").onsubmit=async e=>{e.preventDefault();
  const nome=$("#pf-nome").value.trim(),cpf=$("#pf-cpf").value.trim(),pref=$("#pf-pref").value;
  try{const d=await apiFetch("/api/usuarios/"+user.id,{metodo:"PUT",
    corpo:{nome,cpf,preferencia:pref}});
   user={...user,name:d.usuario.nome,cpf:d.usuario.cpf,r:d.usuario.preferencia};
   store.set("iz_user",user);authUI();preencherPerfil();toast("Dados salvos ✔");
  }catch(ex){toast(ex.message)}};
}
function initBlog(){$("#blogList").innerHTML=POSTS.map(postCard).join("")}
function initPost(){
 const b=POSTS.find(x=>x.id===+new URLSearchParams(location.search).get("id"));
 if(b)document.title=b.t+" — Intolerância Zero";
 $("#article").innerHTML=b?`<a class="back" href="blog.html">← Voltar ao blog</a><div class="cover">${pic(b.img,b.e,b.t)}</div><span class="tag">${b.cat}</span><h1 style="margin-top:12px">${b.t}</h1><p class="meta">${b.d} · Equipe Intolerância Zero</p>${b.ps.map(x=>`<p>${x}</p>`).join("")}<p><a class="btn" href="catalogo.html">Ver produtos relacionados</a></p>`:`<a class="back" href="blog.html">← Blog</a><p>Post não encontrado.</p>`;
}

const dataBR=iso=>{try{return new Date(iso).toLocaleDateString("pt-BR")}catch(e){return iso}};
const STATUS_LABEL={pendente:"Pendente",pago:"Pago",enviado:"Enviado",entregue:"Entregue",cancelado:"Cancelado"};

async function initPedidos(){
 const box=$("#listaPedidos");
 try{
  const d=await apiFetch("/api/pedidos");
  const pedidos=d.pedidos||[];
  if(!pedidos.length){box.innerHTML=`<div class="empty">Você ainda não fez pedidos 🌱<br><a href="catalogo.html">Ver catálogo</a></div>`;return}
  box.innerHTML=pedidos.map(p=>`<div class="card pedido" id="pedido-${p.id}">
    <div class="row"><b>Pedido #${p.id}</b><span class="tag st-${p.status}">${STATUS_LABEL[p.status]||p.status}</span></div>
    <small>${dataBR(p.criado_em)} · ${p.forma_pagamento.toUpperCase()} · entrega ${p.cep_entrega}</small>
    <div class="row price"><span>${brl(p.total)}</span>
      <span><button class="btn sm ghost" data-itens="${p.id}">Ver itens</button>
      ${["pendente","pago"].includes(p.status)?`<button class="btn sm ghost" data-cancelar="${p.id}">Cancelar</button>`:""}</span></div>
    <div class="itens" id="itens-${p.id}" hidden></div></div>`).join("");
  box.onclick=async e=>{
   const ver=e.target.closest("[data-itens]"),cancelar=e.target.closest("[data-cancelar]");
   if(ver){const alvo=$("#itens-"+ver.dataset.itens);
     if(!alvo.hidden){alvo.hidden=true;return}
     try{const det=await apiFetch("/api/pedidos/"+ver.dataset.itens);
       alvo.innerHTML=(det.pedido.itens||[]).map(i=>`<div class="row"><span>${i.quantidade}× ${i.nome}</span><span>${brl(i.preco_unitario*i.quantidade)}</span></div>`).join("");
       alvo.hidden=false}catch(ex){toast(ex.message)}}
   if(cancelar){if(!confirm("Cancelar o pedido #"+cancelar.dataset.cancelar+"?"))return;
     try{await apiFetch("/api/pedidos/"+cancelar.dataset.cancelar,{metodo:"DELETE"});toast("Pedido cancelado");initPedidos()}catch(ex){toast(ex.message)}}
  };
 }catch(e){
  if(e.status===401){store.set("iz_flash","Entre para ver seus pedidos");location.href="entrar.html";return}
  box.innerHTML=`<div class="empty">Não foi possível carregar seus pedidos.</div>`;
 }
}

(async()=>{
 renderCart();authUI();await carregarSessao();
 try{await carregarProdutos()}catch(e){}
 ({inicio:initHome,catalogo:initShop,entrar:initAuth,blog:initBlog,post:initPost,pedidos:initPedidos}[document.body.dataset.page]||(()=>{}))();
 renderCart();
 const flash=store.get("iz_flash");if(flash){store.set("iz_flash",null);toast(flash)}
})();