# Sistema de Cotações BCB

<img src="https://github.com/user-attachments/assets/fa8327ea-b037-4334-9b23-98178193ef6e" width="90" />
<img src="https://github.com/user-attachments/assets/5d9e43ee-019a-45bd-9273-b283262c977b" width="90" />

---

📌 Visão Geral

Este é um aplicativo desktop desenvolvido em Python para consulta de cotações do dólar e euro utilizando dados oficiais do Banco Central do Brasil. 

O sistema inclui:

Autenticação de usuários

Consulta em tempo real via API do BCB

Comparativo com o fechamento anterior

Salvamento dos dados em TXT e CSV

Interface intuitiva com logo do BCB

---

🛠️ Pré-requisitos
- Python 3.8 ou superior

Bibliotecas padrão do Python

Pillow (para manipulação de imagens)

bash
Copy
pip install pillow

---

🔐 Credenciais de Acesso

Usuário padrão:

Login: admin

Senha: 1234

---

⚙️ Funcionalidades

Tela de Login
- Autenticação segura

Validação de credenciais

Painel Principal
- Seletor de moedas:

Dólar comercial (série 10813)

Euro comercial (série 21619)

Informações exibidas:

Último fechamento

Valor atual

Fechamento anterior

Variação percentual

Data/hora da última atualização

Ações:

- Atualizar dados

- Exportar para TXT

- Exportar para CSV

---

📊 Fontes de Dados

As cotações são obtidas diretamente da API pública do Banco Central do Brasil:

- Dólar: Série 10813

- Euro: Série 21619

---

🎨 Design

Interface em azul claro com 34% de transparência

Layout responsivo e intuitivo

![image](https://github.com/user-attachments/assets/37c9db54-0637-4652-bbbe-1d25e5ac2430)

---

📁 Estrutura de Arquivos

Os arquivos gerados são salvos no mesmo diretório do aplicativo:

cotacao_dolar.txt / cotacao_euro.txt

cotacao_dolar.csv / cotacao_euro.csv

---

🚀 Como Executar

Clone o repositório ou baixe o arquivo .py

Instale as dependências:

bash
Copy
pip install pillow
Execute o aplicativo:

bash
Copy
python sistema_cotacoes.py

---

📝 Notas de Desenvolvimento

Desenvolvido usando apenas bibliotecas padrão do Python (exceto Pillow)

Código modular e documentado

Tratamento de erros robusto

Compatível com Windows, macOS e Linux

---

📜 Licença
Este projeto está licenciado sob a licença MIT FL-3.0.

✉️ Contato

![pepe](https://github.com/user-attachments/assets/f2245289-602b-4515-a818-a472f93839f7)
