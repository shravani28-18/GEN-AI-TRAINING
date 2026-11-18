
import streamlit as st
import requests
import json
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(
    page_title="PashuSeva",
    page_icon="🐄",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/ask"
BASE_DIR = Path(__file__).resolve().parent.parent
FEEDBACK_FILE = BASE_DIR / "data" / "feedback.json"

# Translate displayed numbers into Devanagari digits
def local_number(value, language):
    text = str(value)
    if language in ["मराठी", "हिंदी"]:
        digits = str.maketrans("0123456789", "०१२३४५६७८९")
        return text.translate(digits)
    return text


# All UI translations
TEXT = {
    "English": {
        "title": "🐄 PashuSeva",
        "subtitle": "Smart Animal Care Assistant",
        "animal": "Select Animal",
        "animals": ["Cow", "Buffalo", "Calf"],
        "feed_title": "🥬 Daily Feed Plate",
        "feed_note": "Estimated daily fodder guide for adult dairy animals.",
        "count": "Number of adult animals",
        "requirement": "Daily fodder requirement",
        "dry": "Dry Fodder",
        "legume": "Green Legume",
        "non_legume": "Green Non-legume",
        "total_green": "Total green fodder",
        "chart": "Daily Feed Plate",
        "water": "💧 Water Reminder: Keep clean drinking water available.",
        "mineral": "🧂 Mineral Mixture Reminder: Follow recommended NDDB feeding guidance.",
        "reference": "Reference: NDDB – Feeding of Dairy Animals",
        "guide": "Open NDDB Feeding Guide",
        "chat": "Ask your question",
        "placeholder": "Ask about feeding, diseases, vaccination...",
        "sources": "📚 Sources",
        "helpful": "👍 Helpful",
        "not_helpful": "👎 Not helpful",
        "thanks": "Thank you for your feedback!",
        "thinking": "Thinking...",
        "error": "Backend connection failed. Please check whether FastAPI is running.",
        "no_answer": "No answer received.",
        "range_note": "Actual needs depend on animal type, body weight and milk yield."
    },
    "मराठी": {
        "title": "🐄 पशुसेवा",
        "subtitle": "जनावरांच्या काळजीसाठी स्मार्ट सहाय्यक",
        "animal": "जनावर निवडा",
        "animals": ["गाय", "म्हैस", "वासरू"],
        "feed_title": "🥬 दैनिक चारा ताट",
        "feed_note": "प्रौढ दुग्धजन्य जनावरांसाठी अंदाजे दैनिक चारा मार्गदर्शन.",
        "count": "प्रौढ जनावरांची संख्या",
        "requirement": "दैनिक चाऱ्याची गरज",
        "dry": "सुका चारा",
        "legume": "द्विदल हिरवा चारा",
        "non_legume": "अद्विदल हिरवा चारा",
        "total_green": "एकूण हिरवा चारा",
        "chart": "दैनिक चारा ताट",
        "water": "💧 पाण्याची सूचना: जनावरांना नेहमी स्वच्छ पिण्याचे पाणी द्या.",
        "mineral": "🧂 खनिज मिश्रण: NDDB च्या शिफारशीनुसार खनिज मिश्रण द्या.",
        "reference": "संदर्भ: NDDB – दुग्धजन्य जनावरांचा आहार",
        "guide": "NDDB आहार मार्गदर्शक उघडा",
        "chat": "तुमचा प्रश्न विचारा",
        "placeholder": "खाद्य, आजार, लसीकरण याबद्दल विचारा...",
        "sources": "📚 संदर्भ",
        "helpful": "👍 उपयुक्त",
        "not_helpful": "👎 उपयुक्त नाही",
        "thanks": "तुमच्या अभिप्रायाबद्दल धन्यवाद!",
        "thinking": "विचार करत आहे...",
        "error": "Backend कनेक्शन झाले नाही. FastAPI चालू आहे का तपासा.",
        "no_answer": "उत्तर मिळाले नाही.",
        "range_note": "प्रत्यक्ष गरज जनावराचा प्रकार, वजन आणि दूध उत्पादनावर अवलंबून असते."
    },
    "हिंदी": {
        "title": "🐄 पशुसेवा",
        "subtitle": "पशु देखभाल स्मार्ट सहायक",
        "animal": "पशु चुनें",
        "animals": ["गाय", "भैंस", "बछड़ा"],
        "feed_title": "🥬 दैनिक चारा प्लेट",
        "feed_note": "वयस्क डेयरी पशुओं के लिए अनुमानित दैनिक चारा मार्गदर्शन।",
        "count": "वयस्क पशुओं की संख्या",
        "requirement": "दैनिक चारे की आवश्यकता",
        "dry": "सूखा चारा",
        "legume": "दलहनी हरा चारा",
        "non_legume": "गैर-दलहनी हरा चारा",
        "total_green": "कुल हरा चारा",
        "chart": "दैनिक चारा प्लेट",
        "water": "💧 पानी की सलाह: पशुओं को हमेशा साफ पीने का पानी दें।",
        "mineral": "🧂 खनिज मिश्रण: NDDB की सलाह के अनुसार खनिज मिश्रण दें।",
        "reference": "संदर्भ: NDDB – डेयरी पशुओं का आहार",
        "guide": "NDDB आहार मार्गदर्शिका खोलें",
        "chat": "अपना प्रश्न पूछें",
        "placeholder": "चारा, बीमारी, टीकाकरण के बारे में पूछें...",
        "sources": "📚 स्रोत",
        "helpful": "👍 उपयोगी",
        "not_helpful": "👎 उपयोगी नहीं",
        "thanks": "आपकी प्रतिक्रिया के लिए धन्यवाद!",
        "thinking": "सोच रहा है...",
        "error": "Backend से कनेक्शन नहीं हुआ। FastAPI चालू है या नहीं जांचें।",
        "no_answer": "कोई उत्तर प्राप्त नहीं हुआ।",
        "range_note": "वास्तविक आवश्यकता पशु के प्रकार, वजन और दूध उत्पादन पर निर्भर करती है।"
    }
}

# Language selector
language = st.selectbox(
    "Select Language / भाषा निवडा / भाषा चुनें",
    ["English", "मराठी", "हिंदी"]
)

t = TEXT[language]

st.title(t["title"])
st.caption(t["subtitle"])

st.divider()

# Animal selection
animal_type = st.selectbox(
    t["animal"],
    t["animals"]
)

# Daily Feed Plate
st.divider()
st.subheader(t["feed_title"])
st.caption(t["feed_note"])

adult_count = st.number_input(
    t["count"],
    min_value=1,
    max_value=100,
    value=1,
    step=1
)

st.caption(
    f"{t['range_note']} "
    f"{local_number(adult_count, language)}"
)

# Estimated daily requirements per adult animal
dry_min = 4 * adult_count
dry_max = 6 * adult_count

green_min = 15 * adult_count
green_max = 20 * adult_count

# Midpoint used for chart
dry = 5 * adult_count
green = 17.5 * adult_count

# Green fodder ratio: legume : non-legume = 1 : 3
legume = green * 0.25
non_legume = green * 0.75

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {t['requirement']}")

    st.metric(
        t["dry"],
        f"{local_number(dry_min, language)}–{local_number(dry_max, language)} kg"
    )

    st.metric(
        t["legume"],
        f"{local_number(round(green_min * 0.25, 1), language)}–"
        f"{local_number(round(green_max * 0.25, 1), language)} kg"
    )

    st.metric(
        t["non_legume"],
        f"{local_number(round(green_min * 0.75, 1), language)}–"
        f"{local_number(round(green_max * 0.75, 1), language)} kg"
    )

    st.caption(
        f"{t['total_green']}: "
        f"{local_number(green_min, language)}–"
        f"{local_number(green_max, language)} kg"
    )

with col2:
    st.markdown(f"### {t['chart']}")

    labels = [t["dry"], t["legume"], t["non_legume"]]
    values = [dry, legume, non_legume]

    custom_values = [
        f"{local_number(round(value, 1), language)} kg"
        for value in values
    ]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                customdata=custom_values,
                hole=0,
                textinfo="percent",
                hovertemplate="%{label}<br>%{customdata}<extra></extra>"
            )
        ]
    )

    fig.update_layout(
        title=t["chart"],
        showlegend=True,
        margin=dict(t=50, b=20, l=10, r=10)
    )

    st.plotly_chart(fig, use_container_width=True)

st.info(t["water"])
st.info(t["mineral"])

st.caption(t["reference"])

st.link_button(
    t["guide"],
    "https://nddb.coop/farmer/animal-nutrition/feeding-of-dairy-animals"
)

st.divider()

# Chat section
st.subheader(t["chat"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("citations"):
            with st.expander(t["sources"]):
                for citation in message["citations"]:
                    st.write(citation)

        if message["role"] == "assistant" and message.get("feedback") is None:
            col1, col2 = st.columns(2)

            with col1:
                if st.button(t["helpful"], key=f"up_{i}"):
                    message["feedback"] = "positive"

            with col2:
                if st.button(t["not_helpful"], key=f"down_{i}"):
                    message["feedback"] = "negative"

            if message.get("feedback"):
                FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)

                feedback_data = {
                    "timestamp": datetime.now().isoformat(),
                    "question": message.get("question", ""),
                    "answer": message["content"],
                    "feedback": message["feedback"]
                }

                existing_feedback = []

                if FEEDBACK_FILE.exists():
                    try:
                        existing_feedback = json.loads(
                            FEEDBACK_FILE.read_text(encoding="utf-8")
                        )
                    except json.JSONDecodeError:
                        existing_feedback = []

                existing_feedback.append(feedback_data)

                FEEDBACK_FILE.write_text(
                    json.dumps(
                        existing_feedback,
                        indent=2,
                        ensure_ascii=False
                    ),
                    encoding="utf-8"
                )

                st.success(t["thanks"])

# Chat input
question = st.chat_input(t["placeholder"])

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner(t["thinking"]):
            try:
                language_instruction = {
                    "English": "Answer in English.",
                    "मराठी": "उत्तर मराठीत द्या.",
                    "हिंदी": "उत्तर हिंदी में दें."
                }

                final_question = (
                    f"{language_instruction[language]}\n"
                    f"Animal: {animal_type}\n"
                    f"Question: {question}"
                )

                response = requests.post(
                    API_URL,
                    json={
                        "question": final_question,
                        "animal_profile": None,
                        "approved": False,
                        "thread_id": "pashuseva-streamlit"
                    },
                    timeout=120
                )

                response.raise_for_status()
                result = response.json()

                answer = result.get("answer", t["no_answer"])
                citations = result.get("citations", [])

                st.markdown(answer)

                if citations:
                    with st.expander(t["sources"]):
                        for citation in citations:
                            st.write(citation)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "citations": citations,
                    "question": question,
                    "feedback": None
                })

            except requests.exceptions.RequestException:
                st.error(t["error"])
