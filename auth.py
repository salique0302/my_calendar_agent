import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def handle_authentication():
    """
    Handles user authentication, login, and registration.
    Returns the authenticator object.
    """
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookies']['name'],
        config['cookies']['key'],
        config['cookies']['expiry_days']
    )

    with st.sidebar:
        st.title("User Authentication")
        login_tab, register_tab = st.tabs(["Login", "Register"])

        with login_tab:
            authenticator.login()

        with register_tab:
            try:
                if authenticator.register_user():
                    st.success('User registered successfully! Please go to the Login tab.')
                    # Update the config file with the new user
                    with open('config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
            except Exception as e:
                st.error(e)
    
    return authenticator