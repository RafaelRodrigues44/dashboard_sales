import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import io
import logging

from datetime import datetime

# Setup logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class SalesDataLoader:
    """
    Class responsible for loading the sales dataset.

    Methods:
        load_data(path: str) -> pd.DataFrame:
            Loads Excel data from the given file path.
    """

    @staticmethod
    def load_data(path: str) -> pd.DataFrame:
        """
        Load Excel data from the specified file path.

        Args:
            path (str): Path to the Excel file.

        Returns:
            pd.DataFrame: Loaded DataFrame with sales data.
        """
        try:
            data = pd.read_excel(path)
            logging.info("Data loaded successfully from %s", path)
            return data
        except Exception as e:
            logging.error("Error loading data: %s", e)
            raise


class SalesFilter:
    """
    Class for filtering the dataset based on user selection.

    Methods:
        apply_filters(df, state, month) -> pd.DataFrame:
            Returns the filtered DataFrame.
    """

    @staticmethod
    def apply_filters(df: pd.DataFrame, state: str, month: str) -> pd.DataFrame:
        """
        Apply filters to the sales dataset.

        Args:
            df (pd.DataFrame): Sales dataset.
            state (str): Selected state.
            month (str): Selected month.

        Returns:
            pd.DataFrame: Filtered dataset.
        """
        filtered_df = df.copy()
        if month != 'TODOS':
            filtered_df = filtered_df[filtered_df['Mês'] == month]
        if state != 'BRASIL':
            filtered_df = filtered_df[filtered_df['Estado'] == state]
        logging.info("Filters applied - State: %s | Month: %s", state, month)
        return filtered_df


class SalesGrouper:
    """
    Class for grouping and aggregating the filtered dataset.

    Methods:
        group_and_format(df, metric, dimension) -> pd.DataFrame:
            Returns aggregated and formatted DataFrame.
    """

    def __init__(self, metric: str, dimension: str):
        self.metric = metric
        self.dimension = dimension

    def _format_value(self, value: float) -> str:
        """
         Format value based on the metric type.

         Args:
        value (float): Numeric value to format.

        Returns:
           str: Formatted value with proper units and bold style.
        """
       if self.metric == 'Margem (%)':
           return f"<b>{value:,.2f}%</b>".replace(",", "X").replace(".", ",").replace("X", ".")
       elif self.metric == 'Quantidade Vendida':
           return f"<b>{int(round(value))}</b>"
       elif "R$" in self.metric:
           return f"<b>R$ {value:,.2f}</b>".replace(",", "X").replace(".", ",").replace("X", ".")
       else:
           return f"<b>{value:,.2f}</b>".replace(",", "X").replace(".", ",").replace("X", ".")

    def group_and_format(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Group the dataset by the selected dimension and aggregate the selected metric.

        Args:
            df (pd.DataFrame): Filtered sales data.

        Returns:
            pd.DataFrame: Aggregated and formatted DataFrame.
        """
        grouped = df.groupby(self.dimension).agg({self.metric: 'sum'}).reset_index()
        grouped = grouped.sort_values(by=self.metric, ascending=False)
        grouped['label'] = grouped[self.metric].apply(self._format_value)
        logging.info("Data grouped by %s and metric %s", self.dimension, self.metric)
        return grouped


class SalesChart:
    """
    Class responsible for creating the sales bar chart.

    Methods:
        generate_chart(df, metric, dimension, state, month) -> go.Figure:
            Returns the plotly chart figure.
    """

    @staticmethod
    def generate_chart(df: pd.DataFrame, metric: str, dimension: str, state: str, month: str) -> go.Figure:
        """
        Generate a plotly bar chart with the aggregated data.

        Args:
            df (pd.DataFrame): Aggregated sales data.
            metric (str): Selected metric.
            dimension (str): Selected dimension.
            state (str): Selected state.
            month (str): Selected month.

        Returns:
            go.Figure: Plotly bar chart figure.
        """
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df[dimension],
            y=df[metric],
            text=df['label'],
            textposition='outside',
            marker_color='orange',
            textfont=dict(size=14, color='black'),
            showlegend=False
        ))

        avg = df[metric].mean()
        fig.add_trace(go.Scatter(
            x=df[dimension],
            y=[avg] * len(df),
            mode='lines',
            name='Média',
            line=dict(color='blue', width=4, dash='dot')
        ))

        month_title = month if month != 'TODOS' else 'Todos os Meses'
        title = f'{metric} por {dimension} - {state} / {month_title}'

        fig.update_layout(
            title=dict(text=title, x=0.5, xanchor='center', font=dict(size=20, color='black')),
            xaxis=dict(title=dimension, tickangle=-45, tickfont=dict(size=12, color='black'), automargin=True),
            yaxis=dict(title=metric, tickfont=dict(size=12, color='black'), showgrid=False),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=12, color='black')),
            margin=dict(l=40, r=40, t=80, b=100),
            height=550
        )

        logging.info("Chart generated successfully")
        return fig


class DashboardApp:
    """
    Main dashboard application class.

    Methods:
        run() -> None:
            Launches the dashboard UI.
    """

    def run(self):
        """
        Run the Streamlit dashboard app.
        """
        st.set_page_config(
            page_title="Dashboard de Vendas",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        st.title("📊 Dashboard de Vendas")

        data = SalesDataLoader.load_data("data/vendas_brasil_2025.xlsx")

        states = ['BRASIL'] + sorted(data['Estado'].unique())
        months = ['TODOS'] + sorted(data['Mês'].unique())
        metrics = ['Quantidade Vendida', 'Receita Total (R$)', 'Lucro (R$)', 'Margem (%)']
        dimensions = ['Produto', 'Estado', 'Mês']

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            selected_state = st.selectbox("Estado", states)
        with col2:
            selected_month = st.selectbox("Mês", months)
        with col3:
            selected_metric = st.selectbox("Métrica", metrics)
        with col4:
            selected_dimension = st.selectbox("Dimensão", dimensions)

        filtered_data = SalesFilter.apply_filters(data, selected_state, selected_month)
        if filtered_data.empty:
            st.warning("⚠️ Nenhum dado disponível para os filtros selecionados.")
            return

        grouper = SalesGrouper(metric=selected_metric, dimension=selected_dimension)
        grouped_data = grouper.group_and_format(filtered_data)

        chart = SalesChart.generate_chart(grouped_data, selected_metric, selected_dimension, selected_state, selected_month)
        st.plotly_chart(chart, use_container_width=True)

        # Export chart as PNG
        buffer = io.BytesIO()
        chart.write_image(buffer, format='png')
        buffer.seek(0)

        st.download_button(
            label="📥 Baixar gráfico em PNG",
            data=buffer,
            file_name="grafico_vendas.png",
            mime="image/png"
        )


if __name__ == "__main__":
    DashboardApp().run()
