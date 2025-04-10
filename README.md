# Dashboard de Vendas - Streamlit

Este projeto é um dashboard interativo de vendas desenvolvido em Python, utilizando as bibliotecas Streamlit, Pandas e Plotly. Ele permite a análise visual de métricas de vendas com base em filtros dinâmicos por estado, mês, dimensão e métrica.

Aviso: Todos os dados utilizados são mockados (dados fictícios) e foram gerados exclusivamente para fins de demonstração.

## Funcionalidades: 

    Leitura de dados a partir do arquivo Excel data/vendas_brasil_2025.xlsx

    Filtros interativos por:

        Estado

        Mês

        Métrica (ex: Receita, Vendas, Lucro)

        Dimensão (ex: Categoria, Subcategoria)

    Gráfico de barras com linha de média destacada

    Download do gráfico gerado em formato PNG

## Estrutura do Projeto

projeto/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    └── vendas_brasil_2025.xlsx

## Requisitos

    Python 3.8 ou superior

    pip (gerenciador de pacotes do Python)

## Instalação Local

### Clone este repositório:

```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
```
   
### Acesse o diretório do projeto:

    cd dashboard_sales

  Instale as dependências:

  ```bash
    pip install -r requirements.txt
  ```

## Execute o projeto com o Streamlit:

```Bash
   streamlit run app.py
```
   
  Acesse o dashboard:

  O navegador será aberto automaticamente em: http://localhost:8501

  Caso isso não ocorra, abra manualmente este endereço.

## Acesso Online

Você pode acessar o dashboard hospedado na Streamlit Cloud neste link:

  https://dashboardsalesgit-gxc8gfwfzeb3zcqfs3kgqn.streamlit.app/
  
## Deploy Online com Streamlit Cloud

Para hospedar sua própria versão gratuitamente:

    Acesse: https://streamlit.io/cloud

     Crie uma conta e conecte seu repositório GitHub

     Selecione o arquivo app.py como ponto de entrada

     Certifique-se de que o arquivo data/vendas_brasil_2025.xlsx está presente no repositório na pasta "data"

As dependências serão instaladas automaticamente a partir de requirements.txt.
Alternativa: Deploy com Dash

Caso queira migrar este projeto para o framework Dash (Plotly), será necessário reescrever a aplicação. O deploy poderá ser feito via Dash Enterprise, com suporte para autenticação, escalabilidade e segurança empresarial.

Instalação do Dash:

```Bash
''pip install dash
```

Mais informações: https://plotly.com/dash

## Considerações Finais

Este projeto pode ser expandido com:

    Upload de arquivos pelo usuário

    Integração com bancos de dados (PostgreSQL, MySQL, SQLite)

    Autenticação de usuários com Streamlit

    Exportação automática de relatórios (PDF, Excel)

    Agendamento de envios por e-mail com métricas

## Autor

Projeto desenvolvido por Rafael Rodrigues com fins de portfólio.
Os dados utilizados são fictícios e destinados exclusivamente à demonstração técnica.


