import os
import streamlit as st
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate


# =================================================
# 🔑 API KEY (SAFE)
# =================================================
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")


# =================================================
# 🤖 LLM INITIALIZATION (SAFE MODE)
# =================================================
def load_llm():
    if not HF_TOKEN:
        return None

    return ChatHuggingFace(
        llm=HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            temperature=0.3,
            max_new_tokens=300,
            huggingfacehub_api_token=HF_TOKEN
        )
    )


llm = load_llm()


# =================================================
# 🤖 AI WEATHER SUMMARY
# =================================================
def ai_weather_summary(current_weather):
    """
    Generates a human-friendly AI weather explanation.
    Falls back gracefully if AI is unavailable.
    """

    # 🔁 FALLBACK (NO AI)
    if llm is None:
        return (
            f"Currently it is {current_weather['main']['temp']}°C with "
            f"{current_weather['weather'][0]['description']}. "
            f"Humidity is around {current_weather['main']['humidity']}%. "
            f"Plan your day accordingly."
        )

    try:
        prompt = ChatPromptTemplate.from_template("""
You are a smart AI weather assistant.

Weather data:
Temperature: {temp} °C
Humidity: {humidity} %
Wind Speed: {wind} m/s
Condition: {condition}

Tasks:
1. Explain today's weather in simple language.
2. Detect possible micro-climate patterns.
3. Give comfort or travel suggestions.
4. Keep the response short and friendly.
""")

        response = llm.invoke(
            prompt.format(
                temp=current_weather["main"]["temp"],
                humidity=current_weather["main"]["humidity"],
                wind=current_weather["wind"]["speed"],
                condition=current_weather["weather"][0]["description"]
            )
        )

        return response.content.strip()

    except Exception:
        return (
            f"Weather is {current_weather['weather'][0]['description']} "
            f"with temperature {current_weather['main']['temp']}°C. "
            f"Stay hydrated and check updates regularly."
        )


# =================================================
# 🌫️🧠 AI SAFETY & TRAVEL ADVICE
# =================================================
def ai_safety_advice(current_weather, aqi_value):
    """
    Generates safety, health, and travel advice.
    """

    if llm is None:
        return (
            "Check air quality before outdoor activity. "
            "Carry water, protect yourself from heat or rain, "
            "and wear a mask if pollution is high."
        )

    try:
        prompt = ChatPromptTemplate.from_template("""
You are an AI safety and travel advisor.

Weather conditions:
Temperature: {temp} °C
Humidity: {humidity} %
Wind Speed: {wind} m/s
Condition: {condition}

Air Quality Index (AQI): {aqi}

Tasks:
1. Give health precautions based on AQI.
2. Suggest travel or outdoor advice.
3. Mention mask, umbrella, hydration, or sun protection if needed.
4. Keep it short and practical.
""")

        response = llm.invoke(
            prompt.format(
                temp=current_weather["main"]["temp"],
                humidity=current_weather["main"]["humidity"],
                wind=current_weather["wind"]["speed"],
                condition=current_weather["weather"][0]["description"],
                aqi=aqi_value
            )
        )

        return response.content.strip()

    except Exception:
        return (
            "Air quality may affect sensitive groups. "
            "Limit long outdoor exposure and take basic precautions."
        )


# =================================================
# 🌍 AI TRANSLATION (CACHED)
# =================================================
def translate_text(text, target_lang):
    """
    Cached AI translation for voice output.
    """

    if llm is None:
        return text  # fallback: return original

    if "translation_cache" not in st.session_state:
        st.session_state.translation_cache = {}

    cache_key = f"{target_lang}:{text}"

    if cache_key in st.session_state.translation_cache:
        return st.session_state.translation_cache[cache_key]

    lang_map = {
        "bn": "Bengali",
        "or": "Odia"
    }

    try:
        prompt = ChatPromptTemplate.from_template("""
Translate the following weather report into {language}.
Keep it short, natural, and suitable for voice output.

Text:
{text}
""")

        response = llm.invoke(
            prompt.format(
                language=lang_map[target_lang],
                text=text
            )
        )

        translated = response.content.strip()
        st.session_state.translation_cache[cache_key] = translated
        return translated

    except Exception:
        return text
