README.md

# Dashboard de Vendas - Streamlit

Este projeto é um dashboard interativo de vendas desenvolvido em Python, utilizando as bibliotecas Streamlit, Pandas e Plotly. Ele permite a análise de métricas de vendas por estado, mês, dimensão e métrica, com visualização gráfica e opção de download.

## Funcionalidades

- Leitura de dados a partir do arquivo Excel `vendas_brasil_2025.xlsx`
- Filtros interativos por:
  - Estado
  - Mês
  - Métrica (por exemplo, Receita, Vendas, Lucro)
  - Dimensão (por exemplo, Categoria, Subcategoria)
- Gráfico de barras com linha de média (destacada em azul)
- Download do gráfico gerado em formato PNG

## Estrutura do Projeto

projeto/ ├── app.py ├── requirements.txt ├── README.md └── data/ └── vendas_brasil_2025.xlsx


## Requisitos

- Python 3.8 ou superior
- pip

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

    Instale as dependências:

pip install -r requirements.txt

Conteúdo do requirements.txt:

streamlit
pandas
plotly
openpyxl

Execução Local

Execute o seguinte comando na raiz do projeto:

streamlit run app.py

O Streamlit abrirá automaticamente o navegador padrão em http://localhost:8501. Caso isso não ocorra, acesse manualmente esse endereço.
Deploy Online
1. Streamlit Community Cloud

A aplicação pode ser publicada gratuitamente na nuvem utilizando a plataforma oficial do Streamlit:

    Crie uma conta em: https://streamlit.io/cloud

    Conecte seu repositório GitHub

    Selecione o arquivo app.py como ponto de entrada

    Confirme que o arquivo vendas_brasil_2025.xlsx está incluído no repositório, preferencialmente na pasta data/

A plataforma instalará automaticamente as dependências listadas em requirements.txt.
2. Dash Enterprise (caso a aplicação seja reescrita em Dash)

Caso deseje migrar para Dash (Plotly), será necessário reestruturar o código em vez de usar Streamlit. O deploy pode ser feito através do Dash Enterprise, com suporte a autenticação, escalabilidade e segurança.

Para instalar o Dash:

pip install dash

Mais informações: https://plotly.com/dash
Considerações Finais

Este projeto é uma base para dashboards analíticos e pode ser expandido com:

    Upload de arquivos pelo usuário

    Integração com bancos de dados relacionais (ex: PostgreSQL, MySQL)

    Autenticação de usuários

    Exportação de relatórios automáticos


---

Se quiser, posso gerar os arquivos `requirements.txt` e `README.md` diretamente para você. Deseja que eu salve isso num arquivo?

