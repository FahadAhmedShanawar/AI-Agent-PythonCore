import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
import base64
from typing import Dict, List
import pandas as pd

class UIHelpers:
    @staticmethod
    def create_pie_chart(by_category: Dict[str, float]) -> str:
        """Create pie chart of spending by category"""
        if not by_category:
            return ""

        fig = px.pie(
            values=list(by_category.values()),
            names=list(by_category.keys()),
            title="Spending by Category"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')

        return UIHelpers._fig_to_base64(fig)

    @staticmethod
    def create_bar_chart(by_category: Dict[str, float]) -> str:
        """Create bar chart of spending by category"""
        if not by_category:
            return ""

        fig = px.bar(
            x=list(by_category.keys()),
            y=list(by_category.values()),
            title="Spending by Category",
            labels={'x': 'Category', 'y': 'Amount'}
        )

        return UIHelpers._fig_to_base64(fig)

    @staticmethod
    def create_trend_chart(expenses: List[Dict]) -> str:
        """Create trend chart (placeholder - implement with actual time series)"""
        # For now, return empty - implement with proper time series data
        return ""

    @staticmethod
    def _fig_to_base64(fig) -> str:
        """Convert plotly figure to base64 encoded PNG"""
        buffer = BytesIO()
        fig.write_image(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        return f"data:image/png;base64,{image_base64}"
