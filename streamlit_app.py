import os
import sys
import requests
import streamlit as st
from markdown2 import markdown  # Richer HTML rendering

# Add current path to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import generate_newsletter

# --- Email formatting ---
def build_html_email(newsletter_md):
    html_body = markdown(newsletter_md)
    html_template = f"""
    <html>
        <body style="font-family:Arial,sans-serif;padding:20px;background-color:#f9f9f9;">
            <h2 style="color:#004080;">Weekly AI, Data & Fintech Updates</h2>
            <hr style="border:1px solid #ddd;"/>
            <div style="padding:20px;background-color:#ffffff;border-radius:8px;">
                {html_body}
            </div>
            <hr style="border:1px solid #ddd;"/>
            <footer style="font-size:12px;color:#888;text-align:center;margin-top:20px;">
            </footer>
        </body>
    </html>
    """
    return html_template

# --- Streamlit App Starts ---
st.set_page_config(page_title="Weekly Newsletter", layout="wide")
st.title("🧠 Weekly Newsletter: AI, Data & Fintech")

# Generate newsletter
if st.button("📰 Generate Newsletter"):
    with st.spinner("Fetching and summarizing latest updates..."):
        try:
            newsletter = generate_newsletter()
            st.session_state['newsletter'] = newsletter
            st.success("✅ Newsletter generated successfully!")
        except Exception as e:
            st.error(f"⚠️ Failed to generate newsletter: {e}")
            import traceback
            st.text(traceback.format_exc())

# Get newsletter from session
newsletter = st.session_state.get('newsletter', '')

if newsletter:
    st.markdown("---")
    
    # Build HTML and show preview
    full_newsletter_html = build_html_email(newsletter)
    st.markdown(full_newsletter_html, unsafe_allow_html=True)

    # Send via Email Section
    st.markdown("---")
    st.subheader("📧 Send via Email")
    send_email_option = st.checkbox("Send this newsletter to recipients?")

    if send_email_option:
        to_emails_input = st.text_input("Enter recipient email(s) separated by commas")

        if st.button("📤 Send Email"):
            if not to_emails_input:
                st.warning("⚠️ Please enter at least one recipient email.")
            else:
                to_emails = [email.strip() for email in to_emails_input.split(",") if email.strip()]
                email_html = full_newsletter_html

                email_data = {
                    "subject": "Weekly AI, Data & Fintech Newsletter",
                    "body_html": email_html,
                    "to_emails": to_emails,
                }

                with st.spinner("Sending email..."):
                    try:
                        response = requests.post(
                            "http://127.0.0.1:5001/send-email",  # Your local email backend
                            json=email_data,
                            timeout=30,
                        )
                        resp_json = response.json()
                        if resp_json.get("success"):
                            st.success("✅ Newsletter sent successfully!")
                        else:
                            st.error(f"❌ Failed to send email: {resp_json.get('error')}")
                    except Exception as e:
                        st.error(f"❌ Error calling email service: {e}")
