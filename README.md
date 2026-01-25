# Reddit-persona-generator

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![Reddit API](https://img.shields.io/badge/API-Reddit-orange)
![Gemini AI](https://img.shields.io/badge/AI-Google%20Gemini-yellow)
![Open Source](https://img.shields.io/badge/Open%20Source-💡-brightgreen)

---

## 📖 Overview
Generates user personas from Reddit profiles using Python and LLMs.

The extracted project contains the following relevant files:

* `python persona_generator.py` — Main script (possibly misnamed with a space).
* `requirements.txt` — Lists Python dependencies.
* Multiple `*_persona.txt` files — Output examples or templates.
* `.env`, `.gitignore`, LICENSE, and an existing `README.md`.

I'll now review the contents of the main script (`python persona_generator.py`) to understand what the project does, so I can generate a proper `README.md`.


The main script is a **Reddit Persona Generator** that uses:

* **PRAW** (Python Reddit API Wrapper) to fetch Reddit user data.
* **Google Gemini** (via `google.generativeai`) to generate personas based on Reddit user activity.
* **dotenv** to load environment variables for API keys and credentials.



This project generates AI-based personas for Reddit users by analyzing their posts and comments using PRAW (Reddit API) and Google Gemini (Generative AI).

## ✨ Features

- Fetches Reddit user history using the Reddit API
- Uses Google Gemini to create personality summaries
- Outputs persona descriptions to text files
- Easy setup with `.env` for API keys

## 📁 Project Structure

```

reddit\_persona\_generator/
├── python persona\_generator.py   # Main script
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables (not shared)
├── \*\_persona.txt                # Generated persona files
├── requirements.txt               # Python dependencies
├── .gitignore
├── LICENSE
└── README.md

````

## 🛠️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/reddit_persona_generator.git
cd reddit_persona_generator
````

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Setup `.env` file**

Create a `.env` file in the project root with the following:

```env
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_user_agent
REDDIT_USERNAME=target_reddit_username
GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key
```

## 🚀 Usage

Run the main script:

```bash
python "python persona_generator.py"
```

The generated persona will be saved in a text file named like `username_persona.txt`.

## 📌 Requirements

* Python 3.8+
* Reddit API credentials (via [Reddit App](https://www.reddit.com/prefs/apps))
* Google Gemini API Key

## 🚀 Future Improvements

* Add support for multiple Reddit usernames in one run
* Integrate OpenAI GPT models as alternative persona generators
* Implement sentiment analysis on user comments
* Create a web dashboard for generating and visualizing personas
* Export personas in JSON/CSV formats in addition to .txt
* Add language detection and multi-language support

## 🔐 Note

Do **not** share your `.env` file publicly as it contains sensitive API credentials.

## 📄 License

This project is licensed under the MIT License – see the LICENSE file for details.
---
