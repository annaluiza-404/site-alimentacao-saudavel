# Intolerância Zero

E-commerce de alimentação sem glúten/lactose: frontend estático + API Flask + PostgreSQL.

> **Trabalho da disciplina SPOBDD2 – Banco de Dados** (Bacharelado em Sistemas de Informação, IFSP, Campus São Paulo), sob orientação do Prof. Dr. Francisco Veríssimo Luciano. Documentação completa no artigo *"Empresa de Alimentação Saudável Sem Glúten e Sem Lactose"*.
>
> O foco da disciplina é o banco de dados: modelagem relacional e regras de negócio **diretamente no SGBD** via Stored Procedures, Triggers, Functions e Views (requisito do artigo), consumidos por uma API Flask e por um frontend estático (com ChatBot e blog de receitas, como no projeto original de Engenharia de Software II).
>
> Os objetos do artigo (`pr_AtualizarEstoque`, `f_ProdutosPorMarca`, `trg_BaixaEstoquePedido`, `vw_CatalogoDisponivel`, em T-SQL/MySQL) foram implementados com o mesmo espírito em **PL/pgSQL (PostgreSQL)**, em snake_case: `pr_atualizar_estoque`, `f_produtos_por_marca`, `trg_baixa_estoque_pedido`, `vw_catalogo_disponivel`. Além desses, o projeto tem a trigger `trg_repoe_estoque_cancelamento`, que devolve o estoque quando um pedido é cancelado.

## Equipe

| Nome | GitHub |
|:--|:--|
| Anna Luiza Budin Borgo | [@annaluiza-404](https://github.com/annaluiza-404) |
| Luiz Otávio | [@Luizzzzzzzz](https://github.com/Luizzzzzzzz) |
| Marcos Paulo | [@MpSantana31](https://github.com/MpSantana31) |
| Mariana Calvão Weng | [@marianaweng](https://github.com/marianaweng) |

## Requisitos

- Python 3.10+
- PostgreSQL 14+ (via Docker é o jeito mais fácil)
- Docker (opcional, para o banco)

> **Nota (Linux):** use sempre `python3`: o comando `python` pode não existir na distribuição. Dentro do ambiente virtual, `venv/bin/python` já aponta para o interpretador criado pelo venv.

## 1. Banco de dados

Com Docker (porta 5432):

```bash
docker run -d --name iz_db \
  -e POSTGRES_USER=iz_app \
  -e POSTGRES_PASSWORD=iz_dev_password \
  -e POSTGRES_DB=alimentacao_saudavel \
  -p 5432:5432 \
  -v "$PWD/backend/sql:/docker-entrypoint-initdb.d" \
  postgres:16-alpine
```

Ou use um PostgreSQL próprio e ajuste as variáveis em `backend/.env`.

## 2. Backend

```bash
cd backend

# ambiente virtual + dependências
python3 -m venv venv
venv/bin/pip install -r requirements.txt

# configuração (edite se o banco não for o padrão do Docker)
cp .env.example .env

# cria tabelas, objetos PL/pgSQL e carga inicial
venv/bin/python sql/setup.py --reset
```

Rodar a API (porta 8000):

```bash
venv/bin/python app.py
```

Opções do `sql/setup.py`: `--reset` (apaga tudo e recria), `--seed` (só carga inicial).

## 3. Frontend

Servir o HTML estático (porta 5000), de novo com `python3`:

```bash
python3 -m http.server 5000 --directory frontend
```

Abrir `http://localhost:5000`.

## Configuração

- **Backend:** `backend/.env` (veja `backend/.env.example`): credenciais do banco, `SECRET_KEY` e, opcionalmente, `OPENAI_API_KEY` + `OPENAI_MODEL` (padrão `gpt-4o-mini`) para o chatbot. Sem a chave, o ChuchuBot responde com as respostas locais pré-definidas.
- **Frontend:** `frontend/js/env.js`: endereço da API (`window.ENV.API`).

As portas precisam bater: a API sobe na 8000 e o CORS do backend aceita origem `http://localhost:5000`.

## Usuários e cupons de teste (após `--reset`)

| E-mail | Senha | Papel | CPF |
|:--|:--|:--|:--|
| `admin@intoleranciazero.com` | `admin123` | admin | já cadastrado |
| `maria@email.com` | `maria123` | cliente | **não cadastrado** |

O cliente precisa de CPF para finalizar compra (cadastro progressivo): entre em **Minha conta** e salve um CPF válido (ex.: `111.444.777-35`).

Cupons: `BEMVINDO10` (10% de desconto), `FRETEGRATIS` (zera o frete, subtotal mínimo R$ 80), `EXPIRADO10` (vencido, para testar rejeição).

## Regras de frete e pagamento

Frete calculado pela região do CEP (primeiro dígito):

| CEP começa com | Região | Frete |
|:--|:--|:--|
| 0 ou 1 | São Paulo | R$ 10,00 |
| 2 ou 3 | RJ / ES / MG | R$ 15,00 |
| 7, 8 ou 9 | Centro-Oeste / Sul | R$ 18,00 |
| 4, 5 ou 6 | Nordeste / Norte | R$ 22,00 |

Formas de pagamento: `pix`, `cartao`, `boleto`. O desconto do cupom é aplicado sobre subtotal + frete.

## Endpoints principais

| Área | Rotas |
|:--|:--|
| Auth | `POST /api/registro`, `POST /api/login`, `POST /api/logout`, `GET /api/me`, `PUT /api/usuarios/<id>` (dono ou admin) |
| Catálogo | `GET /api/produtos` (`q`, `tags`, `cat`, `pr_max`, `ord`, `marca`, `destaque`), `GET /api/produtos/<id>`, `GET /api/produtos/destaques` |
| Catálogo (admin) | `GET /api/produtos/todos` (inclui inativos), `POST/PUT/DELETE /api/produtos` (multipart com campo `imagem`), `PUT /api/produtos/<id>/reativar`, CRUD de `/api/categorias` e `/api/marcas` |
| Frete e cupom | `POST /api/frete` (`cep`), `POST /api/cupom/validar` (`codigo`, `subtotal`, `frete` ou `cep`) |
| Pedidos | `GET/POST /api/pedidos`, `GET/DELETE /api/pedidos/<id>`, `PUT /api/pedidos/<id>/status` (admin) |
| Receitas | `GET /api/receitas?produto_id=<id>`, `GET /api/receitas/<id>`, `POST/PUT/DELETE /api/receitas/<id>` (admin) |
| Chatbot | `POST /api/chatbot` (`pergunta`, `historico` opcional), usando OpenAI `gpt-4o-mini` quando `OPENAI_API_KEY` está configurada |
| Imagens | `GET /uploads/<caminho>` |

Regras de acesso: escrita de catálogo, receitas e status de pedido exige admin; pedidos são visíveis apenas para o dono (admin vê todos). O checkout roda em transação única (COMMIT no sucesso, ROLLBACK em erro) e o estoque é controlado por triggers.

## Estrutura

```
backend/
  app.py            # app Flask + CORS + error handler global (ApiErro)
  config.py         # lê .env
  db.py             # conexão por request, query() e transacao() (COMMIT/ROLLBACK)
  sql/
    ddl.sql         # tabelas, extensão unaccent, checks e índices
    objetos.sql     # procedure, function, triggers (baixa e reposição) e view
    seed.sql        # carga inicial (produtos das imagens do front, cupons, pedidos, receitas)
    setup.py        # aplica ddl + objetos + seed
  repositories/     # SQL puro, uma por entidade
  services/         # regras de negócio, autorização e transações
  routes/           # blueprints "burros" (só parse e resposta)
  utils/            # validators, conversões, security (bcrypt/sessão), erros, imagens
  uploads/          # imagens de produtos enviadas
frontend/
  index.html        # home com destaques da API
  catalogo.html     # catálogo com filtros (restrição, categoria, marca, preço, ordenação)
  entrar.html       # login, cadastro e edição de perfil (CPF)
  pedidos.html      # meus pedidos (itens e cancelamento)
  admin.html        # painel admin (produtos, categorias, marcas, pedidos)
  blog.html / post.html  # receitas e posts de conteúdo (via /api/receitas)
  js/
    env.js          # configuração (URL da API)
    api.js          # fetch com cookies de sessão
    app.js          # catálogo, carrinho, checkout e pedidos
    data.js         # TAGs, categorias e emojis (fallbacks do catálogo)
    chuchubot.js    # chatbot do site
    admin.js        # painel administrativo
  css/
``` 
