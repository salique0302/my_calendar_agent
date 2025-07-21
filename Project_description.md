📅 Calendar AI Assistant 🤖
      An intelligent AI assistant built using Streamlit, LangChain, Google Calendar API, and Gemini (Google Generative AI). It helps users manage their Google Calendar via natural language commands — such as creating events, listing upcoming meetings, or (soon) summarizing past meetings.


🚀 Features
•	🔐 User Login/Registration system with secure password hashing.
•	🧠 LLM-powered AI Agent that understands and executes calendar-related commands.
•	📅 Google Calendar Integration: Create new events, list upcoming events, summarize meetings (coming soon).
•	🌐 Streamlit Web Interface for seamless user experience.
•	💾 Credential Management: Safe use of st.secrets for deployment, session-based and persistent OAuth2 token handling.



🧱 Project Structure

📁 your-project/
├── main.py                  # Main Streamlit app
├── auth.py                  # Handles login, register, config.yaml
├── calendar_tools.py        # Google Calendar API tools for LangChain
├── generate_keys.py         # Hash your password for config.yaml
├── config.yaml              # (Generated if not found - stores users)
├── credentials.json         # (Generated from Streamlit secrets)
└── README.md                # Project documentation


🧠 How It Works
1. User Authentication
Uses streamlit_authenticator to provide login, registration, and session management. User info (hashed passwords) is stored in a config.yaml file.
2. Google Calendar Authentication (OAuth2)
Handles credentials.json generation from Streamlit secrets. Stores OAuth tokens in session and local .pickle file.
3. LangChain Agent + Tools
Uses Structured Chat Zero-Shot Agent. Tools include:
•	CreateCalendarEventTool - Create calendar events
•	ListCalendarEventsTool - List upcoming events
•	SummarizeMeetingTool - Placeholder for meeting summaries
4. User Interface (Streamlit)
Text input for user query, process button, loading spinner, and response from AI agent.



🧪 Sample Use Cases
•	Schedule a meeting with John tomorrow at 4 PM.
•	List my meetings for this week.
•	Create a calendar event titled Team Sync at 3 PM today with alice@example.com and bob@example.com.



🌍 Time Zone Support
The app assumes users are in the Asia/Kolkata (IST) time zone. All event times are parsed and formatted accordingly.


🔧 Deployment Tips
If you're deploying to Streamlit Cloud, set the following secrets: CONFIG_YAML and GOOGLE_CREDENTIALS_JSON
Redirect URI for Google OAuth2 should be: urn:ietf:wg:oauth:2.0:oob


🔒 Security Notes
•	Passwords are hashed using bcrypt.
•	OAuth tokens are stored safely using pickle.
•	Secrets and local credentials files should not be pushed to GitHub.


📈 Future Improvements
•	Summarize past meetings using Gemini Pro + Transcript
•	Multi-user calendar views
•	Date/time parsing improvements with natural language
•	Add voice-to-text query input
•	Notification system via email


📄 License
This project is licensed under the MIT License.
