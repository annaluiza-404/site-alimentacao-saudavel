(function(){
  const AVATAR="images/chuchubot.png";
  const avatarHTML=()=>/\.(png|jpe?g|svg|webp|gif)$/i.test(AVATAR)
    ?`<img src="${AVATAR}" alt="ChuchuBot">`:AVATAR;

  const RESPOSTAS=[
    {k:["oi","olá","ola","bom dia","boa tarde","boa noite","hey"],
     t:"Oi! Eu sou o ChuchuBot 🥒 Posso te ajudar com dúvidas sobre glúten, lactose, rótulos e receitas. Sobre o que quer conversar?"},
    {k:["celíaca","celiaca","celíaco","alergia","intolerância","intolerancia","diferença","diferenca"],
     t:"Intolerância costuma causar desconforto digestivo, enquanto alergia envolve o sistema imunológico e pode ser grave. Em caso de sintomas recorrentes, procure um médico antes de cortar alimentos por conta própria.",
     l:{href:"post.html?id=1",label:"Ler: Glúten, lactose ou alergia?"}},
    {k:["glúten","gluten"],
     t:"O glúten está no trigo, na cevada e no centeio. Para quem evita, vale olhar farinhas alternativas como arroz e milho, e conferir sempre o rótulo.",
     l:{href:"catalogo.html?tag=sg",label:"Ver produtos sem glúten"}},
    {k:["lactose","leite","queijo"],
     t:"Para evitar a lactose, existem bebidas vegetais e versões sem lactose de vários produtos. Atenção a termos como soro de leite e caseína nos rótulos.",
     l:{href:"catalogo.html?tag=sl",label:"Ver produtos sem lactose"}},
    {k:["vegano","vegana","vegetal"],
     t:"Temos vários produtos veganos, de pães a queijo vegetal de castanhas.",
     l:{href:"catalogo.html?tag=vg",label:"Ver produtos veganos"}},
    {k:["açúcar","acucar","diabetes","diet"],
     t:"Na seção sem açúcar você encontra granola, barrinhas e outros snacks. Se tem diabetes, converse com seu médico ou nutricionista sobre o que cabe na sua rotina.",
     l:{href:"catalogo.html?tag=sa",label:"Ver produtos sem açúcar"}},
    {k:["ovo"],
     t:"Para quem evita ovo, temos macarrão, brownie e outros itens. Dá para filtrar por “Sem ovo” no catálogo.",
     l:{href:"catalogo.html?tag=so",label:"Ver produtos sem ovo"}},
    {k:["rótulo","rotulo","contaminação","contaminacao","embalagem"],
     t:"Procure a frase de alerta obrigatória e termos como malte, extrato de cevada, caseína e soro de leite. Na dúvida, prefira produtos com selo de certificação.",
     l:{href:"post.html?id=3",label:"Ler: Como ler rótulos"}},
    {k:["receita","café da manhã","cafe da manha","cozinhar","bolo"],
     t:"Tenho ideias rápidas de café da manhã sem glúten e sem lactose, prontas em menos de 15 minutos!",
     l:{href:"post.html?id=2",label:"Ver 5 cafés da manhã"}},
    {k:["despensa","organizar","cozinha"],
     t:"Separe utensílios e prateleiras para evitar contaminação cruzada e comece pelo básico: farinhas alternativas, bebida vegetal e snacks de emergência.",
     l:{href:"post.html?id=4",label:"Ler: Montando uma despensa segura"}},
    {k:["entrega","frete","prazo","pedido","comprar","pagamento"],
     t:"Para dúvidas sobre pedidos e entrega, fale com nosso atendimento: contato@intoleranciazero.com.br, de segunda a sexta, das 9h às 18h."},
    {k:["obrigado","obrigada","valeu","brigado"],
     t:"De nada! Qualquer dúvida é só chamar 💚"}
  ];
  const PADRAO={t:"Ainda estou aprendendo e não entendi muito bem 🤔 Tente perguntar sobre glúten, lactose, rótulos ou receitas, ou dê uma olhada nos nossos artigos.",
    l:{href:"blog.html",label:"Ver todos os artigos"}};
  const SUGESTOES=["O que é intolerância?","Como ler rótulos?","Ideias de receitas","Produtos sem glúten"];

  const norm=s=>s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"");
  function responder(txt){
    const n=norm(txt);
    return RESPOSTAS.find(r=>r.k.some(k=>n.includes(norm(k))))||PADRAO;
  }

  const root=document.createElement("div");
  root.className="cb";
  root.innerHTML=`
    <button class="cb-fab" aria-label="Abrir chat com o ChuchuBot">
      <span class="cb-ava">${avatarHTML()}</span><span class="cb-lbl">Pergunte ao ChuchuBot</span>
    </button>
    <section class="cb-panel" role="dialog" aria-label="Chat com o ChuchuBot">
      <header class="cb-head">
        <span class="cb-ava">${avatarHTML()}</span>
        <div class="cb-title"><b>ChuchuBot</b><small>Assistente da Intolerância Zero</small></div>
        <button class="cb-close" aria-label="Fechar chat">✕</button>
      </header>
      <div class="cb-msgs" aria-live="polite"></div>
      <div class="cb-sugs"></div>
      <form class="cb-form" autocomplete="off">
        <input type="text" placeholder="Digite sua dúvida…" aria-label="Mensagem" maxlength="300">
        <button aria-label="Enviar">➤</button>
      </form>
      <div class="cb-note">O ChuchuBot não substitui orientação médica.</div>
    </section>`;
  document.body.appendChild(root);

  const $c=s=>root.querySelector(s);
  const msgs=$c(".cb-msgs"),input=$c(".cb-form input"),sugs=$c(".cb-sugs");
  let started=false;

  function addMsg(text,who,link){
    const m=document.createElement("div");
    m.className="cb-msg "+who;
    if(who==="bot"){const a=document.createElement("span");a.className="cb-ava";a.innerHTML=avatarHTML();m.appendChild(a)}
    const t=document.createElement("div");t.className="cb-txt";
    t.textContent=text;               // textContent evita injeção de HTML
    if(link){t.appendChild(document.createElement("br"));
      const a=document.createElement("a");a.href=link.href;a.textContent=link.label+" →";t.appendChild(a)}
    m.appendChild(t);msgs.appendChild(m);msgs.scrollTop=msgs.scrollHeight;
    return m;
  }
  function typing(){
    const m=document.createElement("div");m.className="cb-msg bot cb-typing";
    m.innerHTML=`<span class="cb-ava">${avatarHTML()}</span><div class="cb-txt"><i></i><i></i><i></i></div>`;
    msgs.appendChild(m);msgs.scrollTop=msgs.scrollHeight;return m;
  }
  function enviar(txt){
    txt=txt.trim();if(!txt)return;
    addMsg(txt,"me");input.value="";sugs.hidden=true;
    const t=typing(),r=responder(txt);
    setTimeout(()=>{t.remove();addMsg(r.t,"bot",r.l)},600+Math.random()*500);
  }
  function abrir(o){
    root.classList.toggle("open",o);
    if(o){
      if(!started){started=true;
        addMsg("Oi! Eu sou o ChuchuBot 🥒 Tire suas dúvidas sobre alimentação sem glúten, sem lactose e muito mais.","bot")}
      setTimeout(()=>input.focus(),50);
    }
  }

  SUGESTOES.forEach(s=>{const b=document.createElement("button");b.type="button";b.textContent=s;b.onclick=()=>enviar(s);sugs.appendChild(b)});
  $c(".cb-fab").onclick=()=>abrir(true);
  $c(".cb-close").onclick=()=>abrir(false);
  $c(".cb-form").onsubmit=e=>{e.preventDefault();enviar(input.value)};
  document.addEventListener("keydown",e=>{if(e.key==="Escape"&&root.classList.contains("open"))abrir(false)});
})();