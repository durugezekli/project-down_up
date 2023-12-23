import plotly.offline
import plotly.graph_objs as go
import numpy as np

def cylinder(r, h, a=0, nt=100, nv=50):
    theta = np.linspace(0, 2*np.pi, nt)
    v = np.linspace(a, a+h, nv )
    theta, v = np.meshgrid(theta, v)
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    z = v
    return x, y, z

def boundary_circle(r, h, nt=100):
    theta = np.linspace(0, 2*np.pi, nt)
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    z = h*np.ones(theta.shape)
    return x, y, z

c = cylinder(2, 6, 1)
b1 = boundary_circle(2, 0)
b2 = boundary_circle(2, 6)

fig = go.Figure(
    data=[
        go.Surface(
            x=c[1],
            y=c[2], 
            z=c[0], 
            colorscale=[[0, "gold"], [0.5, "mediumturquoise"], [1, "magenta"]],
            showscale=False,  
            lighting_ambient=0.7, 
            lighting=dict(specular=0.3),
            hoverinfo="skip"
        ),
    ],
)

R = 1.5
fig.update_layout(scene=dict(domain_x=[0, 0], camera_eye=dict(x=-0.76*R, y=1.8*R, z=0.92*R)), showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
fig.update_scenes(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False)

plotly.offline.plot(fig, config={"displayModeBar": False, "responsive": True})

with open("temp-plot.html", "r", encoding="utf-8") as fr: readed = fr.read()
with open("temp-plot.html", "w", encoding="utf-8") as fw: 
    raw = readed.split('class="plotly-graph-div" style="')
    raw[1] = raw[1].split('"', maxsplit=1)
    raw[1][0] = "height: calc(min(100vh, 100vw) - 16px); width: calc(min(100vh, 100vw) - 16px); margin: auto;"
    fw.write(raw[0] + 'class="plotly-graph-div" style="' + raw[1][0] + '"' + raw[1][1])