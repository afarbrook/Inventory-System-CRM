import requests
import streamlit as st

def send_warranty_alert(to_email: str, item_name: str, expiration_date: str):
    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "api-key": st.secrets["BREVO_API_KEY"],
            "Content-Type": "application/json"
        },
        json={
            "sender": {"name": "Inventory System", "email": st.secrets["MY_EMAIL"]},
            "to": [{"email": to_email}],
            "subject": f"Warranty Expiring: {item_name}",
            "htmlContent": f"<p><b>{item_name}</b> warranty expires on {expiration_date}.</p>"
        }
    )
    return response.status_code == 201