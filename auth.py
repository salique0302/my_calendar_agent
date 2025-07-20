import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

def ensure_config_file_exists():
    """
    Checks if config.yaml exists. If not, it creates it from Streamlit secrets.
    This makes the app work both locally and when deployed.
    """
    # Check if the config file already exists (for local development)
    if not os.path.exists('config.yaml'):
        # If not, create it from Streamlit secrets (for deployment)
        # This requires a secret named CONFIG_YAML in your Streamlit Cloud settings
        if "CONFIG_YAML" in st.secrets:
            with open('config.yaml', 'w') as file:
                file.write(st.secrets["CONFIG_YAML"])
        else:
            # If the secret is not set, stop the app with an error
            st.error("Authentication configuration (CONFIG_YAML) is missing from Streamlit secrets.")
            st.stop()

def handle_authentication():
    """
    Handles user authentication, login, and registration.
    Returns the authenticator object.
    """
    # Ensure the config file is present before trying to open it
    ensure_config_file_exists()

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
