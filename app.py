import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import io
import logging

# Setup logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class SalesDataLoader:
    @staticmethod
    def load_data(path: str) -> pd.DataFrame:
        try:
            data = pd.read_excel(path)
            logging.info("Data loaded successfully from %s", path)
            return data
        except Exception as e:
            logging.error("Error loading data: %s", e)
            raise

class SalesFilter:
    @staticmethod
    def apply_filters(df: pd.DataFrame, state: str, month: str) -> pd.DataFrame:
        filtered_df = df.copy()
        if month != 'TODOS':
            filtered_df = filtered_df[filtered_df['Mês'] == month]
        if state != 'BRASIL':
            filtered_df = filtered_df[filtered_df['Estado'] == state]
        logging.info("Filters applied - State: %s | Month: %s", state, month)
        return filtered_df

class SalesGrouper:
    def __init__(self, metric: str, dimension: str):
        self.metric = metric
        self.dimension = dimension

    def _format_value(self, value: float) -> str:
        if self.metric == 'Margem (%)':
            return f"<b>{value:,.2f}%</b>".replace(",", "X").replace(".", ",").replace("X", ".")
        elif self.metric == 'Quantidade Vendida':
            return f"<b>{int(round(value))}</b>"
        elif "R$" in self.metric:
            return f"<b>R$ {value:,.2f}</b>".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            return f"<b>{value:,.2f}</b>".replace(",", "X").replace(".", ",").replace("X", ".")

    def group_and_format(self, df: pd.DataFrame) -> pd.DataFrame:
        grouped = df.groupby(self.dimension).agg({self.metric: 'sum'}).reset_index()
        grouped = grouped.sort_values(by=self.metric, ascending=False)
        grouped['label'] = grouped[self.metric].apply(self._format_value)
        logging.info("Data grouped by %s and metric %s", self.dimension, self.metric)
        return grouped

class SalesChart:
    @staticmethod
    def generate_chart(df: pd.DataFrame, metric: str, dimension: str, state: str, month: str) -> go.Figure:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df[dimension],
            y=df[metric],
            text=df['label'],
            textposition='outside',
            marker=dict(color=df[metric], colorscale='Blues', opacity=0.9),
            textfont=dict(size=10, color='black'),
            showlegend=False
        ))
        avg = df[metric].mean()
        fig.add_trace(go.Scatter(
            x=df[dimension],
            y=[avg] * len(df),
            mode='lines',
            name='Média',
            line=dict(color='red', width=4, dash='dot')
        ))
        month_title = month if month != 'TODOS' else 'Todos os Meses'
        title = f'{metric} por {dimension} - {state} / {month_title}'
        fig.update_layout(
            title=dict(text=title, x=0.5, xanchor='center', font=dict(size=20, color='black')),
            xaxis=dict(title=dimension, tickangle=-45, tickfont=dict(size=10, color='black'), automargin=True),
            yaxis=dict(title=metric, tickfont=dict(size=10, color='black'), showgrid=False),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10, color='black')),
            margin=dict(l=40, r=40, t=80, b=100),
            height=550
        )
        logging.info("Chart generated successfully")
        return fig

class DashboardApp:
    def run(self):
        st.set_page_config(page_title="Dashboard de Vendas", layout="wide", initial_sidebar_state="expanded")
        st.title("📊 Dashboard de Vendas")

        data = SalesDataLoader.load_data("data/vendas_brasil_2025.xlsx")

        states = ['BRASIL'] + sorted(data['Estado'].unique())
        months = ['TODOS'] + sorted(data['Mês'].unique())
        metrics = ['Quantidade Vendida', 'Receita Total (R$)', 'Lucro (R$)', 'Margem (%)']
        dimensions = ['Produto', 'Estado', 'Mês']

        col1, col2, col3, col4 = st.columns(4)
        with col1: selected_state = st.selectbox("Estado", states)
        with col2: selected_month = st.selectbox("Mês", months)
        with col3: selected_metric = st.selectbox("Métrica", metrics)
        with col4: selected_dimension = st.selectbox("Dimensão", dimensions)

        filtered_data = SalesFilter.apply_filters(data, selected_state, selected_month)
        if filtered_data.empty:
            st.warning("⚠️ Nenhum dado disponível para os filtros selecionados.")
            return

        grouper = SalesGrouper(metric=selected_metric, dimension=selected_dimension)
        grouped_data = grouper.group_and_format(filtered_data)

        chart = SalesChart.generate_chart(grouped_data, selected_metric, selected_dimension, selected_state, selected_month)

        # Mostrar gráfico interativo
        st.plotly_chart(chart, use_container_width=True)

        # Exportação segura: HTML para download (não depende de Chrome)
        html_bytes = chart.to_html().encode("utf-8")
        st.download_button(
            label="📥 Baixar gráfico em HTML",
            data=html_bytes,
            file_name="grafico_vendas.html",
            mime="text/html"
        )

if __name__ == "__main__":
    DashboardApp().run()
