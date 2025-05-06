# AutoWriter - AI Resume Generator

**AutoWriter** is an AI-powered utility app that generates **tailored resumes** from your personal information and any job description you provide.

> **Note:** This is a prototype version. It may have limitations, quirks, or unexpected behavior — but hey, that's part of the fun. Use it while the OpenAI credits last!

## Demo

Try it here: [Live App Link](https://autowriter-mf7nhfvlfybkvuhx8v4hpc.streamlit.app)

## Features

- Clean, simple interface using **Streamlit**
- Enter once: Add personal info, education, work experience, projects, and certifications
- Paste a job description and get a **custom-tailored resume** instantly
- Resume generated using **OpenAI GPT-3.5**
- Download editable Word (.docx) file
- Smart Edit and Quick Apply modes (WIP for future)
- No account/login required

## Tech Stack

- Python
- Streamlit
- OpenAI GPT-3.5 API
- python-docx
- dotenv

## How It Works

1. Enter your personal details (once).
2. Paste a job description in Tab 2.
3. The app prompts GPT to tailor a resume.
4. Download the generated .docx file instantly.

## Setup Instructions

1. Clone the repo:

```bash
git clone https://github.com/harsh-aithal/AutoWriter.git
cd AutoWriter
```

2. Create a `.streamlit/secrets.toml` file with your OpenAI API key:

```toml
OPENAI_API_KEY = "your_openai_api_key_here"
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app.py
```

## Roadmap / Upcoming Features

- **Smart Edit Mode**: Interactive resume editing with real-time suggestions.
- **Quick Apply Mode**: Generate resumes with one click for new job posts.
- **Save multiple profiles** for different roles or versions.
- **PDF download support** with better formatting.
- Option to **store and re-use past resumes**.

## Limitations

- Resume formatting is basic (Word only).
- No backend/database (yet) — all data is session-based.
- Works best in desktop browser.
- Still experimental — you may run into minor bugs or formatting issues.

## Acknowledgments

- Powered by [OpenAI GPT-3.5](https://openai.com)
- Built with [Streamlit](https://streamlit.io)
- Inspired by jobseekers tired of copying/pasting their details again and again.

---

**Made with caffeine, curiosity, and just enough free credits.**
