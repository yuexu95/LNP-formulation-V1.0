"""

This is the main page, that you have to run with "streamlit run" to launch the app locally.
Streamlit automatically create the tabs in the left sidebar from the .py files located in /pages
Here we just have the home page, with a short description of the tabs, and some images

"""


import streamlit as st

st.set_page_config(
    page_title="Home page",
    page_icon="👋",
    layout="centered")


# Main Description
st.title("👋 LNP Formulation Calculator")
st.markdown("Designed for quick, accurate lipid nanoparticle (LNP) formulation workflows for pDNA and mRNA.")
st.markdown("Developed by **Yue Xu**, YongLi Lab @ BCM — more at https://yuexu95.github.io/")
st.markdown("Have feedback or feature requests? Email: **yue.xu@bcm.edu**.")
st.markdown("---")
# Description of the features. 
with st.container():
    st.markdown("""
    ### Explore in the left sidebar

    - **General info**: Overview of LNP formulation concepts and calculation principles.
    - **pDNA Formulation**: Calculator for plasmid DNA, with N/P ratio and detailed volumes.
    - **mRNA Formulation**: Calculator for mRNA, mirroring the pDNA workflow and outputs.
    - **Formulation Optimization**: Design and optimize LNP formulations based on desired properties.
    - **References**: Key literature and resources for LNP formulation knowledge.
    """)             




st.markdown(
    """
    ### Key features
    - **N/P ratio metrics** for quick quality checks.
    - **Bulk volumes**: auto-summed master mixes (ethanol ×1.5, aqueous ×1.2) and totals for multi-batch prep.
    - **History & export**: each run saved; download CSV for record-keeping.

    ### Quick start
    1. Run locally: `streamlit run 👋Homepage.py`
    2. Open a calculator page, enter parameters, and click **Calculate**.
    3. Expand **Bulk View details** in History to see multi-batch volumes.

    ### Enjoy the app!
    """
)

# --- Conversational Chat (ChatGPT-like with streaming) ---
st.markdown("---")
st.subheader("💬 Quick Chat")
st.caption("Ask questions about LNP formulations or the app. Uses streaming from OpenAI if `OPENAI_API_KEY` is in secrets; otherwise a local helper replies.")

# Check for OpenAI API key in Streamlit secrets
has_openai = "OPENAI_API_KEY" in st.secrets

# Initialize chat state
if "home_chat_messages" not in st.session_state:
    st.session_state.home_chat_messages = [
        {"role": "assistant", "content": "Hi! How can I help with LNP formulations today?"}
    ]

# Render chat history
for msg in st.session_state.home_chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Local fallback helper
def local_reply(prompt: str) -> str:
    prompt = prompt.strip()
    if not prompt:
        return "Could you share more details about your question?"
    tips = [
        "Ethanol master mix is often scaled ×1.5.",
        "For RNA/DNA: P (μmol) ≈ mass (μg) / 330.",
        "Bulk volumes: aqueous ×1.2; lipids/ethanol ×1.5.",
        "Export your formulation history as CSV from the history panel.",
    ]
    return f"You said: '{prompt}'.\n\nQuick tip: {tips[hash(prompt) % len(tips)]}"

# Chat input
user_msg = st.chat_input("Type your message…")
if user_msg:
    st.session_state.home_chat_messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    # Generate assistant reply (with streaming if OpenAI available)
    with st.chat_message("assistant"):
        try:
            if has_openai:
                from openai import OpenAI
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.home_chat_messages],
                    stream=True,
                )
                reply = st.write_stream(stream)
            else:
                reply = local_reply(user_msg)
        except Exception as e:
            reply = f"Local fallback: {local_reply(user_msg)}\n\n(Error: {str(e)[:100]})"
            st.markdown(reply)
    st.session_state.home_chat_messages.append({"role": "assistant", "content": reply})

# Sidebar helper for chat
with st.sidebar:
    st.subheader("Chat Settings")
    st.toggle("Use OpenAI (OPENAI_API_KEY in secrets)", value=has_openai, disabled=True)
