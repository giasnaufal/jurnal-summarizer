import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

st.set_page_config(page_title="AI Journal Summarizer", page_icon="📑", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stButton>button {
        background: linear-gradient(45deg, #3b82f6, #8b5cf6);
        color: white; border: none; padding: 12px 30px;
        border-radius: 8px; font-weight: bold; width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4); }
    .card { background-color: #1e293b; padding: 25px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #334155; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #3b82f6;'>📑 Smart Journal Summarizer AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.1rem;'>Ubah jurnal ilmiah menjadi rangkuman poin penting dalam hitungan detik.</p>", unsafe_allow_html=True)
st.write("---")

kolom_kiri, kolom_kanan = st.columns([1, 1.5], gap="large")

with kolom_kiri:
    st.markdown("<div class='card'><h3>🛠️ Pengaturan & Unggah</h3>", unsafe_allow_html=True)
    api_key = st.text_input("1. Masukkan Gemini API Key Anda:", type="password")
    uploaded_file = st.file_uploader("2. Unggah Berkas PDF Jurnal:", type=["pdf"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    tombol_proses = st.button("✨ Mulai Rangkum Sekarang")

with kolom_kanan:
    st.markdown("<h3>📝 Hasil Rangkuman</h3>", unsafe_allow_html=True)
    
    if tombol_proses:
        if not api_key:
            st.error("Silakan isi Gemini API Key terlebih dahulu!")
        elif not uploaded_file:
            st.warning("Silakan unggah file PDF jurnal Anda terlebih dahulu!")
        else:
            with st.spinner("AI sedang membaca dan menganalisis jurnal..."):
                try:
                    reader = PdfReader(uploaded_file)
                    teks_jurnal = ""
                    for halaman in reader.pages[:15]:
                        teks_jurnal += halaman.extract_text()
                    
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"""
                    Anda adalah asisten akademik senior. Tolong buat rangkuman yang sangat rapi,
                    mudah dipahami, dan profesional dalam Bahasa Indonesia dari teks jurnal ini.
                    Format struktur outputnya menjadi:
                    - **Judul & Latar Belakang**
                    - **Metode Penelitian**
                    - **Temuan Utama / Hasil**
                    - **Kesimpulan**
                    
                    Teks Jurnal: {teks_jurnal}
                    """
                    
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='card'>{response.text}</div>", unsafe_allow_html=True)
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan teknis: {e}")
