const ph=(kw,lock,w=600,h=450)=>`images/${kw.split(",")[0]}-${lock}.jpg`;
const TAGS={sg:"Sem glúten",sl:"Sem lactose",vg:"Vegano",sa:"Sem açúcar",so:"Sem ovo"};
const CATS=["Pães e massas","Doces e biscoitos","Snacks","Bebidas","Mercearia"];
const P=[
{id:1,n:"Pão de forma de arroz",c:0,p:18.9,t:["sg","sl","vg"],e:"🍞",img:"images/produtos/pao-arroz.jpg"},
{id:2,n:"Macarrão de milho 500g",c:0,p:12.5,t:["sg","sl","vg","so"],e:"🍝",img:"images/produtos/macarrao-milho.jpg"},
{id:3,n:"Cookie de aveia sem glúten",c:1,p:14.9,t:["sg","sl"],e:"🍪",img:"images/produtos/cookie-aveia.jpg"},
{id:4,n:"Brownie de cacau 70%",c:1,p:21.0,t:["sg","sl","vg","so"],e:"🍫",img:"images/produtos/brownie.jpg"},
{id:5,n:"Barrinha de castanhas",c:2,p:9.9,t:["sg","sl","vg","sa"],e:"🥜",img:"images/produtos/barrinha-castanhas.jpg"},
{id:6,n:"Chips de batata-doce",c:2,p:11.5,t:["sg","sl","vg","sa","so"],e:"🍠",img:"images/produtos/chips-batata-doce.jpg"},
{id:7,n:"Bebida de amêndoas 1L",c:3,p:16.9,t:["sl","vg","sg","sa"],e:"🥛",img:"images/produtos/leite-amendoas.jpg"},
{id:8,n:"Kombucha de gengibre",c:3,p:13.9,t:["sg","sl","vg"],e:"🍵",img:"images/produtos/kombucha-gengibre.jpg"},
{id:9,n:"Farinha de arroz integral",c:4,p:8.9,t:["sg","sl","vg","sa","so"],e:"🌾",img:"images/produtos/farinha-arroz.jpg"},
{id:10,n:"Pasta de amendoim integral",c:4,p:19.9,t:["sg","sl","vg","sa"],e:"🥜",img:"images/produtos/pasta-amendoim.jpg"},
{id:11,n:"Mix de farinhas para bolo",c:4,p:24.9,t:["sg","sl","vg"],e:"🧁",img:"images/produtos/mix-farinhas.jpg"},
{id:12,n:"Queijo vegetal de castanhas",c:4,p:42.0,t:["sg","sl","vg","so"],e:"🧀",img:"images/produtos/queijo-castanhas.jpg"},
{id:13,n:"Granola sem açúcar",c:2,p:27.5,t:["sl","vg","sa"],e:"🥣",img:"images/produtos/granola.jpg"},
{id:14,n:"Pão de queijo sem lactose",c:0,p:22.0,t:["sg","sl"],e:"🥯",img:"images/produtos/pao-de-queijo.jpg"}];
const POSTS=[
{id:1,e:"🌾",img:"images/blog/gluten-ou-alergia.jpg",cat:"Guia",t:"Glúten, lactose ou alergia? Entenda as diferenças",d:"12 out 2026",ps:["Intolerância, alergia e doença celíaca costumam ser confundidas, mas funcionam de formas bem diferentes no corpo. A intolerância à lactose, por exemplo, vem da falta da enzima lactase e causa desconforto digestivo.","Já a alergia envolve o sistema imunológico e pode ser grave. Em caso de sintomas recorrentes, procure um médico para um diagnóstico correto antes de cortar alimentos por conta própria."]},
{id:2,e:"🥣",img:"images/blog/cafe-manha.jpg",cat:"Receitas",t:"5 cafés da manhã sem glúten e sem lactose",d:"28 out 2026",ps:["Panqueca de banana com aveia certificada, tapioca recheada, mingau de arroz com canela, torradas de pão de arroz com pasta de amendoim e vitamina de bebida vegetal.","Todas ficam prontas em menos de 15 minutos e usam ingredientes que você encontra aqui na loja."]},
{id:3,e:"🔍",img:"images/blog/rotulo.jpg",cat:"Dicas",t:"Como ler rótulos sem cair em pegadinhas",d:"02 nov 2026",ps:["Procure a frase de alerta obrigatória, mas também fique atento a termos como caseína, soro de leite, malte e extrato de cevada, que podem indicar lactose ou glúten.","Na dúvida, escolha produtos com selo de certificação e prefira fabricantes que informam o risco de contaminação cruzada."]},
{id:4,e:"🛒",img:"images/blog/despensa.jpg",cat:"Bem-estar",t:"Montando uma despensa segura em casa",d:"05 nov 2026",ps:["Separe utensílios e prateleiras para evitar contaminação cruzada, principalmente se a casa tem pessoas sem restrição.","Comece pelo básico: farinhas alternativas, bebida vegetal, uma boa pasta de oleaginosas e snacks para emergências."]}];