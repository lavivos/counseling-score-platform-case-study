"""Utils plotting"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px


def scatter_plot(x, y, option="static", xlabel=None, ylabel=None, **kwargs):
    """Scatter plot"""
    assert option in ("static", "interactive")
    if option == "static":
        return matplotlib_scatter_plot(x,
                                       y,
                                       xlabel=xlabel,
                                       ylabel=ylabel,
                                       **kwargs)
    return plotly_scatter_plot(x, y, xlabel=xlabel, ylabel=ylabel, **kwargs)


def plotly_scatter_plot(x, y, xlabel=None, ylabel=None, **kwargs):
    """Plot a scatter plot using plotly modules"""
    width, height = kwargs.pop("width", 10), kwargs.pop("height", 6)
    color = kwargs.pop("color")
    xlabel = xlabel if xlabel else x.name
    ylabel = ylabel if ylabel else y.name
    fig = go.FigureWidget([
        go.Scatter(x=x,
                   y=y,
                   mode='markers',
                   opacity=0.65,
                   marker=dict(color=color))
    ])
    fig.update_layout(width=width * 96,
                      height=height * 96,
                      xaxis_title=xlabel,
                      yaxis_title=ylabel,
                      font=dict(size=12),
                      template="none")
    return fig


def matplotlib_scatter_plot(x, y, xlabel=None, ylabel=None, **kwargs):
    """Plot a scatter plot using matplotlib modules"""
    width, height = kwargs.pop("width", 10), kwargs.pop("height", 6)
    setup_rc_params()
    fig, axis = plt.subplots(figsize=(width, height))
    axis.scatter(x, y, s=15, **kwargs)
    xlabel = xlabel if xlabel else x.name
    ylabel = ylabel if ylabel else y.name
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)
    return fig


def setup_rc_params():
    """Setup matplotlib general parameters"""
    plt.style.use('seaborn-whitegrid')
    mpl.rcParams["font.size"] = 12
    mpl.rcParams["font.weight"] = "bold"


def priority_scatter_plot(estimator, y, option, **kwargs):
    """Scatter"""
    assert option in ("static", "interactive")
    width, height = kwargs.pop("width", 10), kwargs.pop("height", 6)
    estimator.X_target[
        "PositiveGain"] = estimator.X_target["PerformanceGain"] > 0
    estimator.X_target["20-FinalGrade"] = 20 - y
    if option == "static":
        fig, axis = plt.subplots(figsize=(width, height))
        axis.plot([], [],
                  '',
                  color='black',
                  label="Points to maximal grade (20-FinalGrade)")
        sns.scatterplot(data=estimator.X_target,
                        x="PerformanceGain",
                        y="Complexity",
                        hue="20-FinalGrade",
                        size="20-FinalGrade",
                        legend="full",
                        ax=axis)
        custom_legend_columns = estimator.X_target["20-FinalGrade"].nunique(
        ) // 3
        axis.legend(bbox_to_anchor=(0, 1.02, 1, 0.2),
                    loc="lower left",
                    mode="expand",
                    borderaxespad=0,
                    ncol=custom_legend_columns)
        return fig
    hover_data = [
        "FirstName", "FamilyName", "FinalGrade", "ExpectedGrade",
        "PerformanceGain", "Complexity"
    ]
    fig = px.scatter(estimator.X_target,
                     x="PerformanceGain",
                     y="Complexity",
                     color="20-FinalGrade",
                     size='20-FinalGrade',
                     hover_data=hover_data)
    fig.update_layout(
        width=width * 96,  # inches to pixels
        height=height * 96,
        font=dict(size=12),
        template="none")
    return fig
