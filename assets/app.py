import os
import uuid
import time
import streamlit as st
from google import genai
from css_loader import load_all_css

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Campus Helpdesk",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# SESSION STATE
# =====================================================

if "chats" not in st.session_state:

    first_chat_id = str(uuid.uuid4())

    st.session_state.chats = {
        first_chat_id: {
            "title": "New Chat",
            "messages": []
        }
    }

    st.session_state.current_chat = first_chat_id

# =====================================================
# GEMINI API
# =====================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=GEMINI_API_KEY
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(f"""
<style>
{load_all_css()}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
    <div style="
        font-size: 45px;
        font-weight: 800;
        color: var(--text-color);
        line-height: 1.2;
        padding-top: 6px;
        padding-bottom: 4px;
        letter-spacing: 0.5px;
    ">
        Campus Helpdesk 🎓
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="
        font-size: 22px;
        font-weight: 900 !important;
        color: var(--text-color);
    ">
        <strong>💬 Percakapan</strong>
    </div>
    """, unsafe_allow_html=True)

    # =================================================
    # NEW CHAT BUTTON
    # =================================================

    new_chat_container = st.container()

    with new_chat_container:

        st.markdown('<div class="new-chat-anchor"></div>',
        unsafe_allow_html=True)

        if st.button(
            "➕ Obrolan Baru",
            use_container_width=True
        ):

            new_chat_id = str(uuid.uuid4())

            st.session_state.chats[new_chat_id] = {
                "title": "New Chat",
                "messages": []
            }

            st.session_state.current_chat = new_chat_id

            st.rerun()

    st.divider()

    # =================================================
    # CHAT HISTORY
    # =================================================

    for chat_id, chat_data in list(st.session_state.chats.items()):

        if len(chat_data["messages"]) == 0:
            continue

        title = chat_data["title"]
        display_title = title if len(title) <= 19 else title[:19] + "..."

        col1, col2 = st.columns([0.85, 0.15], gap="small")

        chat_container = st.container()

        with chat_container:

            # =============================================
            # OPEN CHAT
            # =============================================
            with col1:

                st.markdown('<div class="chat-list-anchor"></div>',
                unsafe_allow_html=True)

                if st.button(
                    display_title,
                    key=f"chat_{chat_id}",
                    use_container_width=True
                ):
                    st.session_state.current_chat = chat_id
                    st.rerun()

            # =============================================
            # DELETE CHAT
            # =============================================

            with col2:

                st.markdown('<div class="delete-chat-anchor"></div>',
                unsafe_allow_html=True)

                if st.button(
                    "✕",
                    key=f"delete_{chat_id}",
                    use_container_width=True
                ):
                    del st.session_state.chats[chat_id]

                    if len(st.session_state.chats) == 0:
                        new_chat_id = str(uuid.uuid4())
                        st.session_state.chats[new_chat_id] = {
                            "title": "New Chat",
                            "messages": []
                        }
                        st.session_state.current_chat = new_chat_id
                    else:
                        st.session_state.current_chat = list(st.session_state.chats.keys())[0]

                    st.rerun()

# =====================================================
# MAIN CHAT AREA
# =====================================================

current_chat = st.session_state.chats[
    st.session_state.current_chat
]

# =====================================================
# WELCOME SCREEN
# =====================================================

if len(current_chat["messages"]) == 0:

    st.title(
        "Selamat datang di Campus Helpdesk"
    )

    st.markdown("""
    Asisten AI untuk membantu mencari informasi seputar:

    - 🏛️ Universitas
    - 📍 Lokasi Kampus
    - 📚 Kurikulum
    - 💰 UKT (Uang Kuliah Tunggal)
    - 🏢 Fasilitas Kampus
    - 🌐 Akreditasi
    - 🚀 Prospek Karier
    - 📖 Beasiswa
    """)

    st.divider()

    st.markdown("#### Pilih menu di bawah ini :")

    inline_menu = st.container()

    with inline_menu:

      st.markdown('<div class="inline-menu-anchor"></div>',
      unsafe_allow_html=True)

      col1, col2, col3, col4 = st.columns(4)

      with col1:

          if st.button("🏛️ Universitas", use_container_width=True):
              st.session_state["quick_prompt"] = (
                  "Rekomendasikan universitas terbaik di Indonesia"
              )

          if st.button("📍 Lokasi", use_container_width=True):
              st.session_state["quick_prompt"] = (
                  "Rekomendasi kampus berdasarkan lokasi"
              )

      with col2:

          if st.button("📚 Kurikulum", use_container_width=True):
              st.session_state["quick_prompt"] = (
                  "Informasi kurikulum dan mata kuliah"
              )

          if st.button("💰 UKT", use_container_width=True):
              st.session_state["quick_prompt"] = (
                  "Informasi UKT kampus"
              )

      with col3:

          if st.button("🏢 Fasilitas", use_container_width=True):
              st.session_state["quick_prompt"] = (
                  "Kampus dengan fasilitas terbaik"
              )

          if st.button("🌐 Akreditasi", use_container_width=True):
              st.session_state["quick_prompt"] = (
                  "Informasi akreditasi kampus"
              )

      with col4:

          if st.button("🚀 Karier", use_container_width=True):
              st.session_state["quick_prompt"] = (
                  "Prospek kerja tiap jurusan"
              )

          if st.button("📖 Beasiswa", use_container_width=True):
              st.session_state["quick_prompt"] = (
                  "Cari informasi beasiswa"
              )

      st.markdown("""<br>
      Atau ketik pertanyaan pada kolom chat.
      <br><br><br>""", unsafe_allow_html=True)

# =====================================================
# SHOW CHAT
# =====================================================

for message in current_chat["messages"]:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =====================================================
# QUICK PROMPT
# =====================================================

prompt = None

if "quick_prompt" in st.session_state:

    prompt = st.session_state.quick_prompt

    del st.session_state.quick_prompt

# =====================================================
# CHAT INPUT
# =====================================================

user_input = st.chat_input(
    "Tanyakan sesuatu..."
)

if user_input:
    prompt = user_input

# =====================================================
# PROCESS CHAT
# =====================================================

if prompt:

    # =================================================
    # SAVE USER MESSAGE
    # =================================================

    current_chat["messages"].append({
        "role": "user",
        "content": prompt
    })

    # =================================================
    # SHOW USER MESSAGE
    # =================================================

    with st.chat_message("user"):

        st.markdown(prompt)

    # =================================================
    # AI RESPONSE
    # =================================================

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        full_response = ""

        try:

            response = client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=prompt
            )

            bot_reply = response.text

        except Exception as e:

            error_message = str(e)

            # =================================================
            # GEMINI LIMIT ERROR
            # =================================================

            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:

                bot_reply = """
                Permintaan Anda sementara tidak dapat diproses karena limit.

                Mohon coba kembali beberapa saat lagi.
                """

            # =================================================
            # API KEY ERROR
            # =================================================

            elif "API key" in error_message:

                bot_reply = """API Key yang Anda masukkan tidak valid."""

            # =================================================
            # GENERAL ERROR
            # =================================================

            else:

                bot_reply = f"""Terjadi kesalahan."""

        # =============================================
        # TYPING EFFECT
        # =============================================

        import re

        full_response = ""

        parts = re.split(r'(\s+|\n)', bot_reply)

        for part in parts:

            full_response += part

            response_placeholder.markdown(full_response + "▌")

            time.sleep(0.005)

        response_placeholder.markdown(full_response)

    # =================================================
    # SAVE AI RESPONSE
    # =================================================

    current_chat["messages"].append({
        "role": "assistant",
        "content": full_response
    })

    # =================================================
    # AUTO TITLE CHAT
    # =================================================

    if current_chat["title"] == "New Chat":

        current_chat["title"] = prompt[:30]

    st.rerun()