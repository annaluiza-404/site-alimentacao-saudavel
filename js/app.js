const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const brl=v=>v.toLocaleString("pt-BR",{style:"currency",currency:"BRL"});
const store={get(k){try{return JSON.parse(localStorage.getItem(k))}catch(e){return null}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};
function toast(m){const t=$("#toast");t.textContent=m;t.classList.add("show");clearTimeout(toast.h);toast.h=setTimeout(()=>t.classList.remove("show"),2400)}
const pic=(src,fb,alt)=>`<img src="${src}" alt="${alt}" loading="lazy" onerror="this.replaceWith(document.createTextNode('${fb}'))">`;
let cart=store.get("iz_cart")||[],user=store.get("iz_user");

const card=p=>`<div class="card"><div class="img">${pic(p.img,p.e,p.n)}</div><div class="body"><small>${CATS[p.c]}</small><h3>${p.n}</h3>
<div class="tags">${p.t.slice(0,3).map(k=>`<span class="tag">${TAGS[k]}</span>`).join("")}</div>
<div class="row price"><span>${brl(p.p)}</span><button class="btn sm" data-add="${p.id}">Adicionar</button></div></div></div>`;
const postCard=b=>`<a class="card post" href="post.html?id=${b.id}"><div class="img">${pic(b.img,b.e,b.t)}</div><div class="body"><span class="tag" style="align-self:flex-start">${b.cat}</span><h3>${b.t}</h3><small>${b.d}</small></div></a>`;

/* Carrinho (compartilhado entre as páginas via localStorage) */
function renderCart(){
 $("#count").textContent=cart.reduce((s,i)=>s+i.q,0);
 $("#cartList").innerHTML=cart.length?cart.map(i=>{const p=P.find(x=>x.id===i.id);return `<div class="item"><div class="e">${pic(p.img,p.e,p.n)}</div><div class="i"><b>${p.n}</b><br><small>${brl(p.p)}</small></div><div class="qty"><button data-dec="${p.id}">−</button>${i.q}<button data-add="${p.id}" data-quiet="1">+</button></div></div>`}).join(""):`<p class="empty">Seu carrinho está vazio 🌱</p>`;
 $("#total").textContent=brl(cart.reduce((s,i)=>s+i.q*P.find(x=>x.id===i.id).p,0));
}
const saveCart=()=>store.set("iz_cart",cart);
function add(id,quiet){const i=cart.find(x=>x.id===id);i?i.q++:cart.push({id,q:1});saveCart();renderCart();if(!quiet)toast("Adicionado ao carrinho ✔")}
function dec(id){const i=cart.find(x=>x.id===id);if(!i)return;if(--i.q<=0)cart=cart.filter(x=>x!==i);saveCart();renderCart()}
const openCart=o=>{$("#drawer").classList.toggle("open",o);$("#scrim").classList.toggle("open",o)};
$("#cartBtn").onclick=()=>openCart(true);$("#closeCart").onclick=$("#scrim").onclick=()=>openCart(false);
$("#checkout").onclick=()=>{
 if(!cart.length)return toast("Seu carrinho está vazio");
 if(!user){store.set("iz_flash","Entre para finalizar a compra");location.href="entrar.html";return}
 cart=[];saveCart();renderCart();openCart(false);toast("Pedido realizado! Obrigado, "+user.name.split(" ")[0]+" 💚")};
document.addEventListener("click",e=>{
 const a=e.target.closest("[data-add]");if(a)return add(+a.dataset.add,a.dataset.quiet);
 const d=e.target.closest("[data-dec]");if(d)dec(+d.dataset.dec)});
$("#menu").onclick=()=>$("#nav").classList.toggle("open");
$("#theme").onclick=()=>{const r=document.documentElement,dark=r.dataset.theme?r.dataset.theme==="dark":matchMedia("(prefers-color-scheme:dark)").matches;r.dataset.theme=dark?"light":"dark";store.set("iz_theme",r.dataset.theme)};
if(store.get("iz_theme"))document.documentElement.dataset.theme=store.get("iz_theme");

function authUI(){
 $("#navLogin").textContent=user?"Olá, "+user.name.split(" ")[0]:"Entrar";
 if(!$("#authBox"))return;
 $("#authBox").hidden=!!user;$("#userBox").hidden=!user;
 if(user){$("#hello").textContent="Olá, "+user.name.split(" ")[0]+"!";$("#uinfo").textContent=user.email+" · Preferência: "+user.r}
}

/* ---------- Páginas ---------- */
function initHome(){
 $("#chips").innerHTML=[["sg","🌾"],["sl","🥛"],["vg","🌱"],["sa","🍬"],["so","🥚"]].map(([k,e])=>`<a class="chip" href="catalogo.html?tag=${k}"><b>${e}</b>${TAGS[k]}</a>`).join("");
 $("#featured").innerHTML=P.filter(p=>[1,4,7,12].includes(p.id)).map(card).join("");
 $("#homeBlog").innerHTML=POSTS.slice(0,3).map(postCard).join("");
 $("#newsForm").onsubmit=e=>{e.preventDefault();e.target.reset();toast("Inscrição confirmada! 💌")};
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
  let r=P.filter(p=>[...st.tags].every(t=>p.t.includes(t))&&(st.cat===""||p.c===+st.cat)&&p.p<=st.pr&&p.n.toLowerCase().includes(st.q.toLowerCase()));
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
 $("#fUp").onsubmit=e=>{e.preventDefault();const n=$("#su-n"),m=$("#su-e"),s=$("#su-s");
  const v=[err(n,n.value.trim().length<2?"Informe seu nome":""),err(m,okMail(m.value)?"":"E-mail inválido"),err(s,s.value.length<6?"Mínimo de 6 caracteres":"")];
  if(v.includes(false))return;const users=store.get("iz_users")||[];
  if(users.some(x=>x.email===m.value.toLowerCase()))return err(m,"E-mail já cadastrado");
  const u={name:n.value.trim(),email:m.value.toLowerCase(),pass:s.value,r:$("#su-r").value};users.push(u);store.set("iz_users",users);login(u,"Conta criada! Bem-vindo(a) 🌿")};
 $("#fIn").onsubmit=e=>{e.preventDefault();const m=$("#li-e"),s=$("#li-s");
  if(!err(m,okMail(m.value)?"":"E-mail inválido")|!err(s,s.value?"":"Informe a senha"))return;
  const u=(store.get("iz_users")||[]).find(x=>x.email===m.value.toLowerCase()&&x.pass===s.value);
  if(!u)return err(s,"E-mail ou senha incorretos");login(u,"Olá de novo, "+u.name.split(" ")[0]+"!")};
 $("#logout").onclick=()=>{user=null;store.set("iz_user",null);authUI();toast("Você saiu da conta")};
}
function initBlog(){$("#blogList").innerHTML=POSTS.map(postCard).join("")}
function initPost(){
 const b=POSTS.find(x=>x.id===+new URLSearchParams(location.search).get("id"));
 if(b)document.title=b.t+" — Intolerância Zero";
 $("#article").innerHTML=b?`<a class="back" href="blog.html">← Voltar ao blog</a><div class="cover">${pic(b.img,b.e,b.t)}</div><span class="tag">${b.cat}</span><h1 style="margin-top:12px">${b.t}</h1><p class="meta">${b.d} · Equipe Intolerância Zero</p>${b.ps.map(x=>`<p>${x}</p>`).join("")}<p><a class="btn" href="catalogo.html">Ver produtos relacionados</a></p>`:`<a class="back" href="blog.html">← Blog</a><p>Post não encontrado.</p>`;
}

renderCart();authUI();
({inicio:initHome,catalogo:initShop,entrar:initAuth,blog:initBlog,post:initPost}[document.body.dataset.page]||(()=>{}))();
const flash=store.get("iz_flash");if(flash){store.set("iz_flash",null);toast(flash)}
