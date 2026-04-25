import streamlit as st

# Konfigurasi - PAKSA MODE TERANG
st.set_page_config(
    page_title="Kalkulator Waris Islam",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS PAKSA - Override semua warna Streamlit
st.markdown("""
<style>
    /* Paksa seluruh background jadi putih */
    .stApp, .stApp > header, .stApp > div, .main, .block-container {
        background-color: white !important;
    }
    
    /* Paksa semua teks jadi hitam */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    label, .stNumberInput label, .stCheckbox label, .stSelectbox label {
        color: black !important;
    }
    
    /* Card hasil */
    .result-card {
        background-color: #f0fdf4 !important;
        padding: 20px !important;
        border-radius: 15px !important;
        border-left: 5px solid #ffd700 !important;
        margin: 20px 0 !important;
    }
    
    /* Item hasil */
    .result-item {
        background: white !important;
        padding: 12px !important;
        margin: 8px 0 !important;
        border-radius: 10px !important;
        border: 1px solid #ddd !important;
    }
    
    /* Tombol */
    .stButton button {
        background-color: #ffd700 !important;
        color: black !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border-radius: 30px !important;
        border: none !important;
    }
    
    /* Input number */
    .stNumberInput input {
        color: black !important;
        background-color: white !important;
        border: 2px solid #ffd700 !important;
        border-radius: 10px !important;
    }
    
    /* Checkbox */
    .stCheckbox span {
        color: black !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f5f5dc !important;
    }
    
    [data-testid="stSidebar"] * {
        color: black !important;
    }
    
    /* Metrik */
    [data-testid="stMetricValue"] {
        color: #2d6a4f !important;
        font-size: 1.5rem !important;
    }
    
    /* Alert */
    .stAlert {
        background-color: #fff3cd !important;
        color: #856404 !important;
    }
    
    /* All text must be black */
    div, p, span, h1, h2, h3, h4, h5, li, .st-emotion-cache-10trblm {
        color: black !important;
    }
    
    /* Input field text */
    input, textarea {
        color: black !important;
        background-color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== ISI KONTEN ==========

# Header
col_title, col_logo = st.columns([4, 1])
with col_title:
    st.markdown("# ⚖️ Kalkulator Waris Islam")
    st.markdown("### FARAIDH")
    st.markdown("Berdasarkan Al-Qur'an Surah An-Nisa ayat 11-12")

st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## 🌟 Info Penting")
    st.markdown("### Aturan Faraidh")
    st.markdown("""
    **Suami**: 1/4 (ada anak), 1/2 (tidak ada anak)
    
    **Istri**: 1/8 (ada anak), 1/4 (tidak ada anak)
    
    **Ibu**: 1/6 (ada anak), 1/3 (tidak ada anak)
    
    **Ayah**: 1/6 (ada anak), Ashabah (tidak ada anak)
    
    **Anak**: Ashabah, rasio L:P = 2:1
    """)
    st.markdown("---")
    st.caption("Wassalamu'alaikum Warahmatullahi Wabarakatuh")

# Input Area
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Harta Warisan")
    total_harta = st.number_input("Total Harta (Rp)", min_value=0, value=100000000, step=10000000)
    
    st.markdown("### Ahli Waris")
    ada_suami = st.checkbox("Suami", value=True)
    ada_istri = st.checkbox("Istri", value=False)
    ada_ayah = st.checkbox("Ayah", value=False)
    ada_ibu = st.checkbox("Ibu", value=True)

with col2:
    st.markdown("### Keturunan")
    anak_l = st.number_input("Anak Laki-laki", min_value=0, value=2, step=1)
    anak_p = st.number_input("Anak Perempuan", min_value=0, value=1, step=1)

# Tombol
st.markdown("---")
hitung = st.button("HITUNG PEMBAGIAN WARIS", use_container_width=True)

# Fungsi hitung
def hitung_waris(total, suami, istri, ayah, ibu, anak_l, anak_p):
    sisa = total
    bagian = {}
    
    punya_anak = (anak_l + anak_p) > 0
    
    if suami:
        if punya_anak:
            bagian['Suami'] = sisa * 1/4
        else:
            bagian['Suami'] = sisa * 1/2
        sisa -= bagian['Suami']
    
    if istri:
        if punya_anak:
            bagian['Istri'] = sisa * 1/8
        else:
            bagian['Istri'] = sisa * 1/4
        sisa -= bagian['Istri']
    
    if ibu:
        if punya_anak:
            bagian['Ibu'] = sisa * 1/6
        else:
            bagian['Ibu'] = sisa * 1/3
        sisa -= bagian['Ibu']
    
    if ayah and punya_anak:
        bagian['Ayah'] = sisa * 1/6
        sisa -= bagian['Ayah']
    
    if punya_anak and sisa > 0:
        bobot = (anak_l * 2) + (anak_p * 1)
        if bobot > 0:
            per_bobot = sisa / bobot
            if anak_l > 0:
                bagian['Anak Laki-laki'] = per_bobot * 2 * anak_l
            if anak_p > 0:
                bagian['Anak Perempuan'] = per_bobot * 1 * anak_p
            sisa = 0
    
    if not punya_anak and ayah and sisa > 0:
        bagian['Ayah (Ashabah)'] = sisa
    
    return bagian

# Tampilkan hasil
if hitung:
    if total_harta <= 0:
        st.error("Masukkan total harta yang valid!")
    else:
        bagian = hitung_waris(total_harta, ada_suami, ada_istri, ada_ayah, ada_ibu, anak_l, anak_p)
        
        st.markdown("---")
        st.markdown("## HASIL PEMBAGIAN WARIS")
        st.markdown(f"**Total Harta: Rp {total_harta:,.0f}**")
        
        total_terbagi = 0
        urutan = ['Suami', 'Istri', 'Ibu', 'Ayah', 'Ayah (Ashabah)']
        
        for nama in urutan:
            if nama in bagian:
                nilai = bagian[nama]
                total_terbagi += nilai
                persen = (nilai / total_harta) * 100
                st.markdown(f"""
                <div class="result-item">
                    <span style="font-weight:bold;">👤 {nama}</span>
                    <span>Rp {nilai:,.0f} <span style="color:#e67e22;">({persen:.2f}%)</span></span>
                </div>
                """, unsafe_allow_html=True)
        
        if 'Anak Laki-laki' in bagian:
            nilai = bagian['Anak Laki-laki']
            total_terbagi += nilai
            persen = (nilai / total_harta) * 100
            st.markdown(f"""
            <div class="result-item">
                <span style="font-weight:bold;">Anak Laki-laki ({anak_l} orang)</span>
                <span>Rp {nilai:,.0f} <span style="color:#e67e22;">({persen:.2f}%)</span></span>
            </div>
            """, unsafe_allow_html=True)
            if anak_l > 0:
                st.caption(f"↳ Per anak laki-laki: Rp {nilai/anak_l:,.0f}")
        
        if 'Anak Perempuan' in bagian:
            nilai = bagian['Anak Perempuan']
            total_terbagi += nilai
            persen = (nilai / total_harta) * 100
            st.markdown(f"""
            <div class="result-item">
                <span style="font-weight:bold;">Anak Perempuan ({anak_p} orang)</span>
                <span>Rp {nilai:,.0f} <span style="color:#e67e22;">({persen:.2f}%)</span></span>
            </div>
            """, unsafe_allow_html=True)
            if anak_p > 0:
                st.caption(f"↳ Per anak perempuan: Rp {nilai/anak_p:,.0f}")
        
        st.markdown("---")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Total Harta", f"Rp {total_harta:,.0f}")
        with col_b:
            st.metric("Total Terbagi", f"Rp {total_terbagi:,.0f}")
        with col_c:
            persen_total = (total_terbagi / total_harta) * 100 if total_harta > 0 else 0
            st.metric("Persentase", f"{persen_total:.2f}%")
        
        sisa = total_harta - total_terbagi
        if sisa > 0.01:
            st.warning(f"Sisa harta yang belum terbagi: Rp {sisa:,.0f}")
        else:
            st.success("Alhamdulillah, harta waris telah terbagi seluruhnya!")

st.markdown("---")
st.caption("Bintan Nabilah Faradisa (111) | Dibuat berdasarkan materi Algoritma & Matematika dalam Peradaban Islam | © 2026")

# ========== END ==========
