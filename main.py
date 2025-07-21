import os
import datetime
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentType, initialize_agent
from zoneinfo import ZoneInfo
import logging

# Import our custom modules
from auth import handle_authentication
from calendar_tools import CreateCalendarEventTool, ListCalendarEventsTool, SummarizeMeetingTool

# --- Setup and Configuration ---
logging.basicConfig(level=logging.INFO)
load_dotenv()

# --- Main Application Logic ---
def main():
    st.set_page_config(page_title="📅 Calendar AI Assistant", page_icon="🤖")

    # Handle user authentication and get the authenticator object
    authenticator = handle_authentication()

    # --- MAIN APP (RUNS ONLY AFTER SUCCESSFUL LOGIN) ---
    if st.session_state.get("authentication_status"):
        with st.sidebar:
            st.title(f"Welcome {st.session_state['name']}")
            authenticator.logout('Logout')

        st.title("📅 Calendar AI Assistant")
        st.write("I can help you manage your Google Calendar. Try asking me to schedule a meeting or list your upcoming events!")

        # FIX: The redundant check for credentials.json has been removed.
        # The logic to create this file from secrets is now correctly handled
        # inside the calendar_tools.py file when a tool is actually used.
            
        try:
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)
            
            tools = [
                CreateCalendarEventTool(username=st.session_state["username"]), 
                ListCalendarEventsTool(username=st.session_state["username"]), 
                SummarizeMeetingTool(username=st.session_state["username"])
            ]
            
            agent = initialize_agent(
                tools, llm,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True, handle_parsing_errors=True
            )
        except Exception as e:
            st.error(f"Error initializing the AI agent: {e}")
            return

        user_request = st.text_input("What would you like to do?", placeholder="e.g., Schedule a meeting for tomorrow at 10am")

        if st.button("Process Request"):
            if user_request:
                with st.spinner("Agent is thinking..."):
                    try:
                        local_tz_name = "Asia/Kolkata"
                        now_in_local_tz = datetime.datetime.now(ZoneInfo(local_tz_name))

                        prompt = f"""
                        You are a helpful AI assistant that manages a user's Google Calendar.
                        The user's local timezone is {local_tz_name}.
                        The current date and time is: {now_in_local_tz.strftime('%A, %B %d, %Y %I:%M %p %Z')}.
                        When generating date and time strings for the tools, assume the user is referring to their local time unless they specify otherwise.
                        Based on the user's request below, decide which tool to use.
                        User Request: "{user_request}"
                        """
                        response = agent.run(prompt)
                        st.success("Task Complete!")
                        st.markdown(response)
                    except Exception as e:
                        st.error(f"An error occurred while processing your request: {e}")
            else:
                st.warning("Please enter a request.")

    elif st.session_state.get("authentication_status") == False:
        st.error('Username/password is incorrect')
    elif st.session_state.get("authentication_status") == None:
        st.info('Please login or register to continue.')

if __name__ == '__main__':
    main()
