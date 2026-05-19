import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# Pengaturan tampilan web
st.set_page_config(page_title="AI Journal Summarizer", page_icon="📑", layout="wide")

# Perbaikan CSS: Kotak hasil menggunakan warna putih (light mode card) agar teks hitam sangat kontras dan mudah dibaca
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
    .card-input { background-color: #1e293b; padding: 25px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #334155; color: #f8fafc; }
    .card-output { background-color: #ffffff; padding: 30px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #e2e8f0; color: #0f172a; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .card-output h1, .card-output h2, .card-output h3, .card-output p, .card-output li, .card-output strong { color: #0f172a !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #3b82f6;'>📑 Smart Journal Summarizer AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.1rem;'>Ubah jurnal ilmiah menjadi rangkuman poin penting dalam hitungan detik.</p>", unsafe_allow_html=True)
st.write("---")

kolom_kiri, kolom_kanan = st.columns([1, 1.5], gap="large")

with kolom_kiri:
    st.markdown("<div class='card-input'><h3>🛠️ Pengaturan & Unggah</h3>", unsafe_allow_html=True)
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
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    prompt = f"""
                    Anda adalah asisten akademik senior. Tolong buat rangkuman yang sangat rapi,
                    mudah dipahami, dan profesional dalam Bahasa Indonesia dari teks jurnal ini.
                    Format struktur outputnya wajib menggunakan poin penanda markdown (bullet points) agar jelas:
                    
                    ### 📌 Judul & Latar Belakang
                    (Isi poin latar belakang di sini)
                    
                    ### 🔬 Metode Penelitian
                    (Isi poin metode di sini)
                    
                    ### 📊 Temuan Utama / Hasil
                    (Isi poin hasil di sini)
                    
                    ### 💡 Kesimpulan
                    (Isi poin kesimpulan di sini)
                    
                    Teks Jurnal: {teks_jurnal}
                    """
                    
                    response = model.generate_content(prompt)
                    
                    # Menggunakan class card-output yang berwarna putih bersih
                    st.markdown(f"<div class='card-output'>{response.text}</div>", unsafe_allow_html=True)
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan teknis: {e}")
