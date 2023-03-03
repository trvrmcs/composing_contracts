from typing import Dict
import plotly.graph_objects as go
from .processes import Process, DAYS


def plot(p: Process) -> go.Figure:
    values = [p(day) for day in DAYS]
    return go.Figure(data=[go.Scatter(y=values, x=DAYS)])


def plots(processes: Dict[str, Process]) -> go.Figure:
    return go.Figure(
        data=[
            go.Scatter(y=[p(day) for day in DAYS], x=DAYS, name=str(name))
            for name, p in processes.items()
        ]
    )
