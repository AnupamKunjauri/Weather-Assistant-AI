import streamlit as st
from datetime import datetime
from pathlib import Path

from weather_api import (
    get_coordinates,
    get_current_weather,
    get_forecast,
    get_air_quality
)

from charts import temperature_chart, wind_chart, humidity_chart
from llm_engine import ai_weather_summary, ai_safety_advice


# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="AI Weather Assistant",
    layout="wide"
)


# =================================================
# SESSION STATE
# =================================================
if "music_playing" not in st.session_state:
    st.session_state.music_playing = False


# =================================================
# 🎵 BACKGROUND MUSIC (SAFE VERSION)
# =================================================
st.markdown("### 🎵 Background Music")

col_m1, col_m2 = st.columns(2)

with col_m1:
    if st.button("▶️ Play Music"):
        st.session_state.music_playing = True

with col_m2:
    if st.button("⏸️ Stop Music"):
        st.session_state.music_playing = False

audio_path = Path(
    "Ultratech_Cement_Weather_Report_Aaj_Tak_5_December_2014_128KBPS.mp3"
)

if st.session_state.music_playing and audio_path.exists():
    with open(audio_path, "rb") as f:
        st.audio(f.read(), format="audio/mp3", loop=True)


# =================================================
# 🎙️ VOICE ASSISTANT
# =================================================
def speak(text, lang="en"):
    safe = text.replace("\n", " ")

    js = f"""
    <script>
    const synth = window.speechSynthesis;
    document.querySelectorAll("audio").forEach(a => a.pause());

    const utter = new SpeechSynthesisUtterance("{safe}");

    const langMap = {{
        en: "en-US",
        hi: "hi-IN",
        bn: "bn-IN",
        or: "or-IN"
    }};
    utter.lang = langMap["{lang}"] || "en-US";

    synth.cancel();
    synth.speak(utter);
    </script>
    """
    st.components.v1.html(js, height=0)


# =================================================
# HEADER
# =================================================
hour = datetime.now().hour
header_img = "day_person.png" if 6 <= hour < 18 else "night_person.png"

st.markdown("""
<style>
.glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(14px);
    border-radius: 16px;
    padding: 22px;
    border: 1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="glass">', unsafe_allow_html=True)
cl, cr = st.columns([4, 1])

with cl:
    st.title("🌍 AI Weather Assistant")
    st.caption("Smart • Human-friendly • Real-time Weather Intelligence")

with cr:
    if Path(header_img).exists():
        st.image(header_img, width=180)

st.markdown("</div>", unsafe_allow_html=True)


# =================================================
# USER INPUT
# =================================================
city = st.text_input(
    "Enter City Name",
    placeholder="e.g. Delhi, Mumbai, London"
)


# =================================================
# MAIN LOGIC
# =================================================
if city:
    location, error = get_coordinates(city)

    if error:
        st.error(error)
        st.stop()

    lat, lon = location

    current = get_current_weather(lat, lon)
    forecast = get_forecast(lat, lon)
    hourly = forecast.get("list", [])

    # -------------------------------------------------
    # CURRENT WEATHER
    # -------------------------------------------------
    st.subheader(f"📍 Current Weather in {city}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌡️ Temperature", f"{current['main']['temp']} °C")
    c2.metric("💧 Humidity", f"{current['main']['humidity']} %")
    c3.metric("💨 Wind", f"{current['wind']['speed']} m/s")
    c4.metric("☁️ Condition", current["weather"][0]["main"])

    st.divider()

    # -------------------------------------------------
    # CHARTS
    # -------------------------------------------------
    st.subheader("📈 Weather Trends (Next 24 Hours)")
    st.plotly_chart(
        temperature_chart(hourly),
        use_container_width=True
    )

    a, b = st.columns(2)
    with a:
        st.plotly_chart(wind_chart(hourly), use_container_width=True)
    with b:
        st.plotly_chart(humidity_chart(hourly), use_container_width=True)

    st.divider()

    # -------------------------------------------------
    # AQI
    # -------------------------------------------------
    aqi_data = get_air_quality(lat, lon)
    aqi_value = aqi_data["list"][0]["main"]["aqi"]

    aqi_labels = {
        1: "🟢 Good",
        2: "🟡 Fair",
        3: "🟠 Moderate",
        4: "🔴 Poor",
        5: "🟣 Very Poor"
    }

    st.subheader("🌫️ Air Quality Index")
    st.metric("AQI Level", aqi_labels.get(aqi_value, "Unknown"))

    st.divider()

    # -------------------------------------------------
    # AI INSIGHTS
    # -------------------------------------------------
    st.subheader("🤖 AI Weather Insights")
    ai_summary = ai_weather_summary(current)
    st.success(ai_summary)

    st.subheader("🧠 AI Safety & Travel Advice")
    advice = ai_safety_advice(current, aqi_value)
    st.warning(advice)

    st.divider()

    # -------------------------------------------------
    # VOICE WEATHER
    # -------------------------------------------------
    st.subheader("🎙️ Voice Weather Assistant")

    lang_ui = st.selectbox(
        "Language",
        ["English", "Hindi", "Bengali", "Odia"]
    )

    lang_code = {
        "English": "en",
        "Hindi": "hi",
        "Bengali": "bn",
        "Odia": "or"
    }[lang_ui]

    voice_text = (
        f"Weather update for {city}. "
        f"Temperature {current['main']['temp']} degree Celsius. "
        f"Humidity {current['main']['humidity']} percent. "
        f"{ai_summary}"
    )

    if st.button("🔊 Speak Weather"):
        speak(voice_text, lang_code)

    st.divider()

    # -------------------------------------------------
    # MAP
    # -------------------------------------------------
    st.subheader("🗺️ Weather Map")

    map_type = st.radio(
        "Map Type",
        ["🌧️ Rain Radar", "🌡️ Temperature Map"],
        horizontal=True
    )

    if map_type == "🌧️ Rain Radar":
        st.components.v1.iframe(
            f"https://www.rainviewer.com/map.html?loc={lat},{lon},8",
            height=450
        )
    else:
        st.components.v1.iframe(
            f"https://openweathermap.org/weathermap"
            f"?layer=temperature&lat={lat}&lon={lon}&zoom=8",
            height=450
        )
