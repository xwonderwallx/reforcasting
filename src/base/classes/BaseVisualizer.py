import string

from pygments.lexers import go


class BaseVisualizer:
    def __init__(self, data):
        self._data = data
        self._figure = go.Figure()

    def _add_column(self, x_data, y_data, column_name: string, mode: string):
        return go.Scatter(
            x=x_data,
            y=y_data,
            mode=mode,
            name=column_name
        )

    def _add_trace(self, x_data, y_data, column_name: string, mode: string):
        self._figure.add_trace(self._add_column(x_data, y_data, column_name, mode))

    def _update_layout(self, title: string, xaxis_title: string, yaxis_title: string, hovermode: string):
        self._figure.update_layout(
            title=title,
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            hovermode=hovermode
        )
