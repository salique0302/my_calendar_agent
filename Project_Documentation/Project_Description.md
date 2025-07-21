# 📅 Calendar AI Assistant 🤖

An intelligent AI assistant built using **Streamlit**, **LangChain**, **Google Calendar API**, and **Gemini (Google Generative AI)**.  
It helps users manage their **Google Calendar** via natural language — like scheduling meetings, listing events, or summarizing past ones.

---

## 🚀 Features

- 🔐 Secure login & registration with hashed passwords
- 🧠 Gemini-powered LangChain agent to understand user instructions
- 📅 Integration with Google Calendar API
  - Create events
  - List events
  - Summarize (placeholder)
- 🌐 Clean Streamlit UI
- 💾 Credential & token management for both local & deployed versions

---

## 📁 Project Structure


---

## 🧠 How It Works

### 1. 🔐 User Authentication
- Uses `streamlit_authenticator` to manage login/registration
- Passwords are **hashed using bcrypt**
- User data is stored in a `config.yaml` file
- If not present, file is generated using `CONFIG_YAML` from `st.secrets`

### 2. 🔑 Google Calendar Authentication
- Automatically checks and creates `credentials.json` using `GOOGLE_CREDENTIALS_JSON` from secrets
- Uses OAuth2 flow (code-based)
- Token saved as `.pickle` and in session state for reuse

### 3. 🤖 LangChain Agent + Tools
LLM agent (Gemini via LangChain) routes user prompts to correct tool:

| Tool                      | Purpose                              |
|---------------------------|--------------------------------------|
| `create_calendar_event`   | Create new events                    |
| `list_calendar_events`    | List upcoming events                 |
| `summarize_last_meeting`  | Placeholder for meeting summaries    |

### 4. 🖥️ Streamlit UI
- Login/Logout Sidebar
- Text input for commands
- Agent handles and responds accordingly

---

## 🧪 Sample Use Cases

- “Schedule a meeting with John tomorrow at 4 PM.”
- “List my meetings for this week.”
- “Create a calendar event titled Team Sync at 3 PM today with alice@example.com and bob@example.com.”

---

## 🌍 Time Zone Support

The assistant assumes the user's time zone is **Asia/Kolkata (IST)** by default.

---

## 🔧 Deployment Tips (Streamlit Cloud)

### Required Secrets:
- `CONFIG_YAML` → contents of your config.yaml file
- `GOOGLE_CREDENTIALS_JSON` → OAuth2 JSON credentials from Google

### Google OAuth2 Setup:
- Enable **Google Calendar API**
- Create OAuth client with type: **Desktop App**
- Set redirect URI: `urn:ietf:wg:oauth:2.0:oob`

---

## 🔒 Security Notes

- bcrypt used for secure password hashing
- `.pickle` token files and sensitive config are not pushed to GitHub
- `config.yaml` and `credentials.json` handled smartly via secrets

---

## 📈 Future Improvements

- ✅ Real summarization using Gemini Pro + transcripts
- ✅ Natural language enhancements for date/time
- ✅ Multi-user calendar views
- ✅ Voice input support
- ✅ Email reminders or alerts

---

## 📄 License

Licensed under the **MIT License**.
