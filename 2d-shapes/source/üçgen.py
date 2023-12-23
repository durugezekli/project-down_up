import plotly.offline
import plotly.graph_objs as go

fig = go.Figure(
    data=go.Scatter(x=[-0.5, 0, 0.5, -0.5], y=[-0.5, 0.5, -0.5, -0.5], fill="toself", line=dict(color="magenta"), hoverinfo="skip"),
    layout=go.Layout(xaxis={"showgrid": False}, yaxis={"showgrid": False})
)

fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), xaxis_visible=False, yaxis_visible=False, xaxis_range=[-1, 1], yaxis_range=[-1, 1], plot_bgcolor="rgba(0, 0, 0, 0)", paper_bgcolor="rgba(0, 0, 0, 0)")

plotly.offline.plot(fig, config={"displayModeBar": False, "responsive": True, "staticPlot": True})

with open("temp-plot.html", "r", encoding="utf-8") as fr: readed = fr.read()
with open("temp-plot.html", "w", encoding="utf-8") as fw: 
    raw = readed.split('class="plotly-graph-div" style="')
    raw[1] = raw[1].split('"', maxsplit=1)
    raw[1][0] = "height: calc(min(100vh, 100vw) - 16px); width: calc(min(100vh, 100vw) - 16px); margin: auto;"
    fw.write(raw[0] + 'class="plotly-graph-div" style="' + raw[1][0] + '"' + raw[1][1])