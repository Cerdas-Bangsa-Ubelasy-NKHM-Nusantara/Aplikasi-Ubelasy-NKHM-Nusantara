# ubelasy/bank_api.py
import requests
import streamlit as st

def submit_to_bank(application_data):
    """
    Mengirim data pengajuan ke bank mitra via API (sandbox).
    application_data: dict yang berisi data pinjaman, profil debitur, dll.
    """
    bank_id = application_data.get("bank_id")
    # Ambil endpoint dan API key dari secrets
    api_config = st.secrets.get(f"BANK_API_{bank_id.upper()}", {})
    endpoint = api_config.get("endpoint")
    api_key = api_config.get("api_key")
    
    if not endpoint:
        # Jika tidak dikonfigurasi, gunakan dummy response
        print("No API endpoint for bank, using mock.")
        return {"status": "success", "message": "Pengajuan diterima (mock)"}
    
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        response = requests.post(endpoint, json=application_data, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}
