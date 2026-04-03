# ⚙️ Sistema de Controle e Análise de Matéria-Prima

Este é um sistema completo de ponta a ponta desenvolvido para o setor metalúrgico. Ele permite o cadastro seguro de materiais recebidos e gera análises visuais interativas em tempo real sobre o estoque e fornecedores.

---

## 🚀 Funcionalidades

* **Cadastro com Validação:** Bloqueio de dados inválidos direto no servidor (Back-end).
* **Segurança Avançada (Área do Gerente):** O sistema possui um assistente de exclusão de registros em 3 etapas que exige a confirmação visual dos dados e uma chave de acesso do gerente para concluir a operação.
* **Dashboard em Tempo Real:** 3 gráficos interativos gerados automaticamente a partir dos dados inseridos:
    * Distribuição de peso por tipo de material.
    * Participação de mercado dos fornecedores (gráfico de pizza).
    * Evolução diária de entrada de carga.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Framework Web:** Flask
* **Banco de Dados:** SQLite (com SQLAlchemy)
* **Engenharia e Análise de Dados:** Pandas
* **Visualização de Dados:** Plotly
* **Interface do Usuário (Front-end):** Bootstrap 5 e JavaScript (Fetch API)

---

## 💻 Como Rodar o Projeto Localmente

1. Clone este repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)