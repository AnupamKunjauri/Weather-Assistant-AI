import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# =================================================
# 🌡️ TEMPERATURE CHART
# - Gradient markers
# - Max / Min markers
# - Smooth curve
# - Optional sunrise / sunset shading
# =================================================
def temperature_chart(hourly, sunrise=None, sunset=None):
    df = pd.DataFrame([
        {
            "time": datetime.fromtimestamp(h["dt"]),
            "temp": h["main"]["temp"]
        }
        for h in hourly[:24]
    ])

    max_row = df.loc[df["temp"].idxmax()]
    min_row = df.loc[df["temp"].idxmin()]

    fig = go.Figure()

    # 🌈 Temperature line
    fig.add_trace(go.Scatter(
        x=df["time"],
        y=df["temp"],
        mode="lines+markers",
        line=dict(width=3, shape="spline"),
        marker=dict(
            size=7,
            color=df["temp"],
            colorscale="Turbo",
            showscale=True,
            colorbar=dict(title="°C")
        ),
        hovertemplate="🕒 %{x|%I:%M %p}<br>🌡 %{y:.1f}°C",
        name="Temperature"
    ))

    # 🔺 Max temperature
    fig.add_trace(go.Scatter(
        x=[max_row["time"]],
        y=[max_row["temp"]],
        mode="markers+text",
        marker=dict(size=13, color="#FF5252"),
        text=[f"Max {max_row['temp']:.1f}°C"],
        textposition="top center",
        name="Max"
    ))

    # 🔻 Min temperature
    fig.add_trace(go.Scatter(
        x=[min_row["time"]],
        y=[min_row["temp"]],
        mode="markers+text",
        marker=dict(size=13, color="#42A5F5"),
        text=[f"Min {min_row['temp']:.1f}°C"],
        textposition="bottom center",
        name="Min"
    ))

    # 🌗 Night shading (optional but recommended)
    if sunrise and sunset:
        fig.add_vrect(
            x0=df["time"].min(),
            x1=datetime.fromtimestamp(sunrise),
            fillcolor="rgba(0,0,0,0.25)",
            layer="below",
            line_width=0
        )
        fig.add_vrect(
            x0=datetime.fromtimestamp(sunset),
            x1=df["time"].max(),
            fillcolor="rgba(0,0,0,0.25)",
            layer="below",
            line_width=0
        )

    fig.update_layout(
        title="🌡️ Temperature Trend (Next 24 Hours)",
        xaxis_title="Time",
        yaxis_title="Temperature (°C)",
        template="plotly_dark",
        height=420,
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig


# =================================================
# 🌬️ WIND SPEED CHART
# =================================================
def wind_chart(hourly):
    df = pd.DataFrame([
        {
            "time": datetime.fromtimestamp(h["dt"]),
            "wind": h["wind"]["speed"]
        }
        for h in hourly[:24]
    ])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["time"],
        y=df["wind"],
        mode="lines+markers",
        line=dict(width=3, shape="spline"),
        fill="tozeroy",
        hovertemplate="🕒 %{x|%I:%M %p}<br>🌬 %{y:.1f} m/s",
        name="Wind Speed"
    ))

    fig.update_layout(
        title="🌬️ Wind Speed (m/s)",
        xaxis_title="Time",
        yaxis_title="m/s",
        template="plotly_dark",
        height=340,
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig


# =================================================
# 💧 HUMIDITY CHART
# =================================================
def humidity_chart(hourly):
    df = pd.DataFrame([
        {
            "time": datetime.fromtimestamp(h["dt"]),
            "humidity": h["main"]["humidity"]
        }
        for h in hourly[:24]
    ])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["time"],
        y=df["humidity"],
        mode="lines+markers",
        line=dict(width=3, shape="spline"),
        hovertemplate="🕒 %{x|%I:%M %p}<br>💧 %{y}% RH",
        name="Humidity"
    ))

    fig.update_layout(
        title="💧 Humidity (%)",
        xaxis_title="Time",
        yaxis_title="%",
        template="plotly_dark",
        height=340,
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig
