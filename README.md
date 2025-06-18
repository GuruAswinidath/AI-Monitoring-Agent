# AI-Monitoring-Agent

# 🤖 AI Meeting Assistant (Video/Text)

This is a **Streamlit-based AI application** that extracts and summarizes actionable insights from meeting recordings or transcripts and emails the summary to a recipient. It leverages **Whisper** for speech-to-text and **spaCy** for Natural Language Processing.

---

## 🚀 Features

- 📤 Upload `.mp4` or `.txt` files
- 🧠 Automatically extract:
  - 🗓️ Deadlines
  - 📩 Requests
  - 🚀 Progress updates
  - 📋 Assigned tasks
- ✉️ Send the extracted meeting summary to any email via Gmail
- 📄 View full transcript and structured summary inside the app

---

## 📁 How It Works

- **Video (.mp4)**: Extracts audio → Transcribes with Whisper → Analyzes with spaCy
- **Text (.txt)**: Directly analyzed using spaCy
- Categorizes sentences using keyword-based filtering
- Sends structured summary to recipient email via Gmail SMTP

---

## 🛠️ Technologies Used

| Technology  | Purpose                         |
|-------------|---------------------------------|
| Streamlit   | UI and Web App Framework        |
| Whisper     | Speech-to-text transcription    |
| spaCy       | NLP to extract meeting insights |
| MoviePy     | Audio extraction from video     |
| smtplib     | Sending email with Python       |

---
