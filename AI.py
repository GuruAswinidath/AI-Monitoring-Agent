
import streamlit as st
import os
import whisper
import spacy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from moviepy.editor import VideoFileClip
import tempfile

# Load models
@st.cache_resource
def load_models():
    return whisper.load_model("base"), spacy.load("en_core_web_sm")

model, spacy_model = load_models()

def send_email(to_email, subject, body, sender_email, sender_password):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Failed to send email: {e}"

def extract_meeting_notes(text):
    DEADLINE_KEYWORDS = ['by', 'before', 'due', 'deadline']
    REQUEST_KEYWORDS = ['can you', 'please', 'i request', 'kindly']
    PROGRESS_KEYWORDS = ['completed', 'in progress', 'started', 'done']
    TASK_KEYWORDS = ['assign', 'responsible for', 'take care of', 'work on']

    doc = spacy_model(text)
    deadlines, requests, progress, tasks = [], [], [], []

    for sent in doc.sents:
        s = sent.text.lower()
        if any(k in s for k in DEADLINE_KEYWORDS): deadlines.append(sent.text)
        if any(k in s for k in REQUEST_KEYWORDS): requests.append(sent.text)
        if any(k in s for k in PROGRESS_KEYWORDS): progress.append(sent.text)
        if any(k in s for k in TASK_KEYWORDS): tasks.append(sent.text)

    def fmt(lst): return "\n".join([f"- {s.strip()}" for s in lst]) if lst else "No items found."

    return f"""
🗓️ **Deadlines:**
{fmt(deadlines)}

📩 **Requests:**
{fmt(requests)}

🚀 **Progress:**
{fmt(progress)}

📋 **Tasks:**
{fmt(tasks)}
"""

def process_file(uploaded_file, receiver_email, sender_email, sender_password):
    try:
        ext = os.path.splitext(uploaded_file.name)[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
            tmp_file.write(uploaded_file.read())
            file_path = tmp_file.name

        if ext == ".mp4":
            audio_path = file_path.replace(".mp4", ".wav")
            clip = VideoFileClip(file_path)
            clip.audio.write_audiofile(audio_path)
            transcript = model.transcribe(audio_path)["text"]
            os.remove(audio_path)

        elif ext == ".txt":
            with open(file_path, 'r') as f:
                transcript = f.read()

        else:
            return "❌ Unsupported file type.", "", ""

        if not transcript.strip():
            return "❌ No content found.", "", ""

        summary = extract_meeting_notes(transcript)
        email_status = send_email(receiver_email, "Meeting Summary", summary, sender_email, sender_password)

        return transcript, summary, email_status

    except Exception as e:
        return f"❌ Error: {e}", "", ""


# Streamlit UI
st.title("🤖 AI Meeting Assistant (Video/Text)")
st.markdown("Upload a `.mp4` file to extract meeting points, or a `.txt` file for direct summarization and email dispatch.")

uploaded_file = st.file_uploader("📤 Upload MP4 or TXT File", type=["mp4", "txt"])

receiver_email = st.text_input("📩 Manager's Email")
sender_email = st.text_input("✉️ Your Gmail")
sender_password = st.text_input("🔑 Your App Password", type="password")

if st.button("🧠 Process"):
    if uploaded_file and receiver_email and sender_email and sender_password:
        with st.spinner("Processing..."):
            transcript, summary, email_status = process_file(uploaded_file, receiver_email, sender_email, sender_password)

        st.subheader("📝 Transcript / Text")
        st.text_area("Transcript", transcript, height=200)

        st.subheader("📌 Summary")
        st.text_area("Summary", summary, height=250)

        st.subheader("📤 Email Status")
        st.success(email_status if "✅" in email_status else "")
        st.error(email_status if "❌" in email_status else "")
    else:
        st.warning("Please fill all fields and upload a file.")
