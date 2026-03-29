import os
from pyngrok import ngrok
import streamlit.web.bootstrap as bootstrap

NGROK_AUTH_TOKEN = "33MSb89z2kR90ybC0ZM62L4Xb9r_2MwFLsGdc1fRB5iGXxVfz"


def start_ngrok():
    # Set the auth token
    if NGROK_AUTH_TOKEN and NGROK_AUTH_TOKEN != "YOUR_AUTHTOKEN_HERE":
        ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    else:
        print("⚠️ Warning: No Ngrok Auth Token provided. Session will expire quickly.")

    # Start ngrok tunnel on port 8501 (Streamlit's default)
    public_url = ngrok.connect(8501).public_url
    print(f"\n🚀 Public URL: {public_url}")
    print("   (Share this link with others to access your local app)\n")

    # Run the Streamlit app
    os.system("streamlit run abcd.py")


if __name__ == "__main__":
    start_ngrok()
