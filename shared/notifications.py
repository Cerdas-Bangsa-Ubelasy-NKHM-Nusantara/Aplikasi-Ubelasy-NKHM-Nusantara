# shared/notifications.py
import streamlit as st
import uuid

def show_toast(message, type="success", duration=3000):
    """
    Menampilkan notifikasi di pojok kanan atas layar.
    
    Parameters:
    - message: teks notifikasi
    - type: "success", "error", "warning", "info"
    - duration: waktu tampil dalam milidetik (default 3000ms)
    """
    colors = {
        "success": "#4CAF50",
        "error": "#F44336",
        "warning": "#FF9800",
        "info": "#2196F3"
    }
    bg_color = colors.get(type, "#4CAF50")
    
    # Generate ID unik untuk setiap notifikasi
    notif_id = f"toast_{uuid.uuid4().hex[:8]}"
    
    html = f"""
    <div id="{notif_id}" style="
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: {bg_color};
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 9999;
        font-family: 'Segoe UI', Roboto, sans-serif;
        font-size: 14px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 10px;
        opacity: 0;
        transform: translateX(100%);
        transition: opacity 0.3s ease, transform 0.3s ease;
        pointer-events: none;
    ">
        <span>{'✅' if type=='success' else '❌' if type=='error' else '⚠️' if type=='warning' else 'ℹ️'}</span>
        <span>{message}</span>
    </div>
    <script>
        (function() {{
            var notif = document.getElementById('{notif_id}');
            if (notif) {{
                // Muncul dengan animasi
                setTimeout(function() {{
                    notif.style.opacity = '1';
                    notif.style.transform = 'translateX(0)';
                }}, 100);
                // Hilang setelah durasi
                setTimeout(function() {{
                    notif.style.opacity = '0';
                    notif.style.transform = 'translateX(100%)';
                    setTimeout(function() {{
                        if (notif && notif.remove) notif.remove();
                    }}, 300);
                }}, {duration});
            }}
        }})();
    </script>
    """
    st.markdown(html, unsafe_allow_html=True)
