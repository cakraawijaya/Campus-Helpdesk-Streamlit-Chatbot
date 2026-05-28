import os
import uuid
import time
import re
import streamlit as st
from google import genai
from css_loader import load_all_css



# =====================================================================================
# PAGE CONFIG
# =====================================================================================

# Configure the main Streamlit page settings
# such as browser title, icon, layout, and sidebar behavior
st.set_page_config(
    page_title="Campus Helpdesk",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)



# =====================================================================================
# SESSION STATE
# =====================================================================================

# Check whether chat data already exists in session_state
# If not, create the first chat automatically
if "chats" not in st.session_state:

    # Generate a unique ID for the first chat
    first_chat_id = str(uuid.uuid4())

    # Store the first chat data inside session_state
    # with a default title and empty message list
    st.session_state.chats = {
        first_chat_id: {
            "title": "New Chat",
            "messages": [],
            "created_at": time.time()
        }
    }

    # Set the first chat as the currently active chat
    st.session_state.current_chat = first_chat_id



# =====================================================================================
# GEMINI API
# =====================================================================================

# Load the Gemini API Key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Create a Gemini API client using the API Key
client = genai.Client(
    api_key=GEMINI_API_KEY
)



# =====================================================================================
# CUSTOM CSS
# =====================================================================================

# Inject all custom CSS styles into the Streamlit page
# to customize the application appearance
st.markdown(f"""
<style>
{load_all_css()}
</style>
""", unsafe_allow_html=True)



# =====================================================================================
# SIDEBAR
# =====================================================================================

# Create the Streamlit sidebar area
with st.sidebar:

    # Display the application title inside the sidebar
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

    # Display a divider line inside the sidebar
    st.divider()

    # Display the conversation section title in the sidebar
    st.markdown("""
    <div style="
        font-size: 22px;
        font-weight: 900 !important;
        color: var(--text-color);
    ">
        <strong>💬 Percakapan</strong>
    </div>
    """, unsafe_allow_html=True)


    # NEW CHAT BUTTON
    # Create a container for the new chat button
    new_chat_container = st.container()

    # Add components inside the new chat container
    with new_chat_container:

        # HTML anchor used for custom CSS styling
        st.markdown('<div class="new-chat-anchor"></div>',
        unsafe_allow_html=True)

        # Button to create a new conversation
        if st.button("➕ Obrolan Baru", use_container_width=True):

            # Generate a unique ID for the new chat
            new_chat_id = str(uuid.uuid4())

            # Add the new chat into session_state
            st.session_state.chats[new_chat_id] = {
                "title": "New Chat",
                "messages": [],
                "created_at": time.time()
            }

            # Set the newly created chat as the active chat
            st.session_state.current_chat = new_chat_id

            # Refresh the app so changes appear immediately
            st.rerun()

    # Display another divider line in the sidebar
    st.divider()

    # CHAT HISTORY
    # Loop through all saved chats in session_state
    sorted_chats = sorted(
        st.session_state.chats.items(),
        key=lambda x: x[1].get("created_at", 0),
        reverse=True
    )

    for chat_id, chat_data in sorted_chats:

        # Hide empty chats
        if len(chat_data["messages"]) == 0:
            continue

        # Retrieve chat title
        title = chat_data["title"]

        # Always shorten title
        display_title = (
            title if len(title) <= 29
            else title[:29] + "..."
        )

        # First user prompt for tooltip
        first_user_prompt = ""

        for msg in chat_data["messages"]:

            if msg["role"] == "user":
                first_user_prompt = msg["content"]
                break

        # Chat item container
        chat_container = st.container()

        with chat_container:

            # HTML anchor for custom styling
            st.markdown('<div class="chat-list-anchor"></div>',
            unsafe_allow_html=True)

            # Open chat button
            if st.button(
                display_title,
                key=f"chat_{chat_id}",
                use_container_width=True,
                help=first_user_prompt
            ):

                # Set active chat
                st.session_state.current_chat = chat_id

                # Refresh app
                st.rerun()



# =====================================================================================
# MAIN CHAT AREA
# =====================================================================================

# Retrieve the currently active chat data
current_chat = st.session_state.chats[
    st.session_state.current_chat
]

# =====================================================================================
# TOP ACTION BAR
# =====================================================================================

# Show delete button only if chat has messages
if len(current_chat["messages"]) > 0:
        
    # Close chat container
    close_chat_container = st.container()

    with close_chat_container:

            # HTML anchor for custom styling
            st.markdown('<div class="delete-chat-anchor"></div>', unsafe_allow_html=True)

            clicked = st.button("Tutup Obrolan", key="delete_current_chat")

            if clicked:
                del st.session_state.chats[st.session_state.current_chat]

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



# =====================================================================================
# WELCOME SCREEN
# =====================================================================================

# Check whether the current chat is still empty
if len(current_chat["messages"]) == 0:

    # Display the welcome page title
    st.title("Selamat datang di Campus Helpdesk")

    # Display the application feature description
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

    # Display a divider line on the main page
    st.divider()

    # Display instructions for quick menu selection
    st.markdown("#### Pilih menu di bawah ini :")

    # Create a container for the quick menu buttons
    inline_menu = st.container()

    # Add components inside the quick menu container
    with inline_menu:

        # HTML anchor used for custom quick menu styling
        st.markdown('<div class="inline-menu-anchor"></div>',
        unsafe_allow_html=True)

        # Create four columns for quick menu buttons
        col1, col2, col3, col4 = st.columns(4)

        # First quick menu column
        with col1:

            # Button for university recommendations
            if st.button("🏛️ Universitas", use_container_width=True):

                # Store the quick prompt inside session_state
                st.session_state["quick_prompt"] = (
                    "Rekomendasikan universitas yang ada di Indonesia berdasarkan peringkat terbaik."
                )

            # Button for location-based campus recommendations
            if st.button("📍 Lokasi", use_container_width=True):

                # Save the location quick prompt
                st.session_state["quick_prompt"] = (
                    "Rekomendasikan universitas yang ada di Indonesia berdasarkan lokasi."
                )

        # Second quick menu column
        with col2:

            # Button for curriculum information
            if st.button("📚 Kurikulum", use_container_width=True):

                # Save the curriculum quick prompt
                st.session_state["quick_prompt"] = (
                    "Rekomendasikan universitas yang ada di Indonesia berdasarkan mata kuliah dan kurikulum terbaik."
                )

            # Button for tuition fee information
            if st.button("💰 UKT", use_container_width=True):

                # Save the tuition fee quick prompt
                st.session_state["quick_prompt"] = (
                    "Rekomendasikan universitas yang ada di Indonesia berdasarkan UKT terendah hingga tertinggi."
                )

        # Third quick menu column
        with col3:

            # Button for campus facilities recommendations
            if st.button("🏢 Fasilitas", use_container_width=True):

                # Save the facilities quick prompt
                st.session_state["quick_prompt"] = (
                    "Rekomendasikan universitas yang ada di Indonesia berdasarkan fasilitas terbaik."
                )

            # Button for accreditation information
            if st.button("🌐 Akreditasi", use_container_width=True):

                # Save the accreditation quick prompt
                st.session_state["quick_prompt"] = (
                    "Rekomendasikan universitas yang ada di Indonesia berdasarkan akreditasi terbaik di wilayah masing-masing."
                )

        # Fourth quick menu column
        with col4:

            # Button for career prospects information
            if st.button("🚀 Karier", use_container_width=True):

                # Save the career quick prompt
                st.session_state["quick_prompt"] = (
                    "Berikan informasi terkait prospek kerja di tiap jurusan dan kasih saran terkait relevansi dunia kerja saat ini."
                )

            # Button for scholarship information
            if st.button("📖 Beasiswa", use_container_width=True):

                # Save the scholarship quick prompt
                st.session_state["quick_prompt"] = (
                    "Berikan informasi terkait beasiswa yang sedang berlangsung dan akan datang."
                )

        # Display additional instructions below the quick menu
        st.markdown("""<br>Atau ketik pertanyaan pada kolom chat.<br><br>""", unsafe_allow_html=True)



# =====================================================================================
# SHOW CHAT
# =====================================================================================

# Display all messages from the active chat history
for message in current_chat["messages"]:

    # Create a chat bubble based on the message role
    # such as user or assistant
    with st.chat_message(message["role"]):

        # Display the chat message content
        st.markdown(message["content"])



# =====================================================================================
# QUICK PROMPT
# =====================================================================================

# Variable used to store the current user prompt
prompt = None

# Check whether a quick prompt has been selected
if "quick_prompt" in st.session_state:

    # Retrieve the quick prompt value
    prompt = st.session_state.quick_prompt

    # Remove the quick prompt after it has been used
    del st.session_state.quick_prompt



# =====================================================================================
# CHAT INPUT
# =====================================================================================

# Create a chat input field at the bottom of the page
user_input = st.chat_input("Tanyakan sesuatu...")

# Check whether the user submitted a message
if user_input:

    # Save the user input as the current prompt
    prompt = user_input



# =====================================================================================
# PROCESS CHAT
# =====================================================================================

# Check whether there is a prompt to process
if prompt:

    # SAVE USER MESSAGE
    # Save the user's message into chat history
    current_chat["messages"].append({"role": "user", "content": prompt})


    # SHOW USER MESSAGE
    # Create a chat bubble for the user message
    with st.chat_message("user"):

        # Display the user's message content
        st.markdown(prompt)


    # AI RESPONSE
    # Create a chat bubble for the AI response
    with st.chat_message("assistant"):

        # Create a placeholder for the typing animation effect
        response_placeholder = st.empty()

        # Loading text
        response_placeholder.markdown("AI sedang berpikir...")
        full_response = ""

        # Start the Gemini API request process
        try:

            # Send the user prompt to the Gemini model
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            # Retrieve the generated text response from Gemini
            if response.text:
                bot_reply = response.text
            
            # If the response is empty
            else:
                bot_reply = """
                Maaf, saya tidak dapat menghasilkan jawaban untuk pertanyaan tersebut.

                Silakan coba pertanyaan lain.
                """

        # Handle errors that occur during the API request
        except Exception as e:

            # Convert the error object into a readable string
            error_message = str(e)


            # GEMINI LIMIT ERROR
            # Check whether the error is caused by API rate limits
            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:

                # Display a message when the API usage limit is reached
                bot_reply = """
                Permintaan Anda sementara tidak dapat diproses karena limit.

                Mohon coba kembali beberapa saat lagi.
                """


            # API KEY ERROR
            # Check whether the API Key is invalid
            elif "API key" in error_message:

                # Display an invalid API Key error message
                bot_reply = """API Key yang Anda masukkan tidak valid."""


            # GENERAL ERROR
            # Handle all other unexpected errors
            else:

                # Display a general error message
                bot_reply = f"""Terjadi kesalahan."""


        # TYPING EFFECT
        # Variable used to store the complete AI response
        full_response = ""

        # Split the response text into parts
        # to create a typing animation effect
        parts = re.split(r'(\s+|\n)', bot_reply)

        # Display the AI response gradually
        for part in parts:

            # Append each text part into the final response
            full_response += part

            # Display the typing cursor animation
            response_placeholder.markdown(full_response + "▌")

            # Add a short delay for a smoother typing effect
            time.sleep(0.005)

        # Display the final response without the cursor
        response_placeholder.markdown(full_response)


    # SAVE AI RESPONSE
    # Save the AI response into chat history
    current_chat["messages"].append({"role": "assistant", "content": full_response})


    # AUTO TITLE CHAT
    # Check whether the chat still uses the default title
    if current_chat["title"] == "New Chat":

        # Automatically set the chat title
        # using the first user prompt
        current_chat["title"] = prompt[:30]

    # Refresh the app after the chat process is complete
    st.rerun()