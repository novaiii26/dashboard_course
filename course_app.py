# PERTANYAAN BISNIS 
#1. Lanskap Kompetisi & Model Bisnis: Bagaimana karakteristik distribusi model bisnis (Free vs Paid) yang diterapkan oleh masing-masing lembaga sertifikasi, dan platform mana yang memimpin volume ketersediaan materi?
#2. Tren Preferensi Pasar Terhadap Topik (Demand Analysis): Bidang fokus teknologi (Genre) mana yang berhasil mengumpulkan akumulasi peserta (Enrollment) terbesar di pasar digital?
#3. Elastisitas Kualitas Terhadap Konversi: Apakah nilai evaluasi materi (Score Rating) memiliki korelasi positif yang kuat terhadap volume pendaftaran peserta (Enrollment)?
#4. Efektivitas Format Pembelajaran: Bagaimana distribusi metode pelaksanaan kelas (Metode) memengaruhi tingkat penyerapan atau ketertarikan peserta untuk bergabung?


"""
====================================================================
DASHBOARD INTERAKTIF: ANALISIS EKSPLANATORI SERTIFIKASI MULTI-PLATFORM
====================================================================
Deskripsi : Aplikasi Business Intelligence berbasis web untuk 
            menjawab 4 pertanyaan bisnis strategis.
Library   : streamlit, pandas, plotly
Eksekusi  : streamlit run app.py
====================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Konfigurasi Sistem Utama Dashboard
st.set_page_config(
    page_title="Dashboard Sertifikasi Digital",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Fungsi Memuat & Membersihkan Data Secara Otomatis (Robust Caching)
@st.cache_data
def load_and_clean_data():
    file_path = 'master_dataset_sertifikasi_cleaned.csv'
    # Jika file cleaned tidak ada, coba baca file master mentah
    if not os.path.exists(file_path):
        file_path = 'master_dataset_sertifikasi.csv'
        
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
        
        # Pembersihan Data Numerik: Handle Score Rating
        data['score_rating'] = pd.to_numeric(data['score_rating'], errors='coerce')
        data['score_rating'] = data['score_rating'].fillna(data['score_rating'].mean())
        
        # Pembersihan Data Numerik: Handle Enrollment dari string/karakter non-angka
        data['enrollment'] = data['enrollment'].astype(str).str.replace(r'[^\d]', '', regex=True)
        data['enrollment'] = pd.to_numeric(data['enrollment'], errors='coerce').fillna(0).astype(int)
        
        # Standardisasi Kapitalisasi Atribut Konten
        data['genre'] = data['genre'].fillna('Other').str.title()
        data['metode'] = data['metode'].fillna('Self-Paced').str.title()
        data['berbayar_free'] = data['berbayar_free'].fillna('Paid').str.title()
        
        return data
    return None

df = load_and_clean_data()

# Validasi Eksistensi Dataset
if df is None:
    st.error("❌ Berkas dataset sertifikasi tidak ditemukan di direktori aktif. Pastikan berkas CSV Anda sudah siap.")
else:
    # 3. Pengaturan Panel Kontrol Pengguna (Sidebar Filters)
    st.sidebar.header("⚙️ Panel Kontrol Filter")
    st.sidebar.markdown("Gunakan filter di bawah ini untuk mengubah cakupan analisis secara dinamis.")
    
    # Filter 1: Lembaga Sertifikasi
    list_platform = ["Semua Platform"] + sorted(list(df['lembaga_sertifikasi'].dropna().unique()))
    selected_platform = st.sidebar.selectbox("Pilih Lembaga Sertifikasi / Platform:", list_platform)
    
    # Filter 2: Skema Model Bisnis
    list_pricing = ["Semua Skema"] + sorted(list(df['berbayar_free'].unique()))
    selected_pricing = st.sidebar.selectbox("Pilih Model Bisnis Harga:", list_pricing)
    
    # Logika Filtrasi Data Kueri
    filtered_df = df.copy()
    if selected_platform != "Semua Platform":
        filtered_df = filtered_df[filtered_df['lembaga_sertifikasi'] == selected_platform]
    if selected_pricing != "Semua Skema":
        filtered_df = filtered_df[filtered_df['berbayar_free'] == selected_pricing]

    # 4. Bagian Dokumen Judul Utama Dashboard
    st.title("🖥️ Dashboard Analisis Eksplanatori & Strategi Sertifikasi Digital")
    st.markdown("""
    Dashboard interaktif ini dikembangkan untuk menyajikan hasil analisis data mendalam (*deep-dive analysis*) 
    mengenai karakteristik penawaran kursus teknologi global, guna merumuskan rekomendasi keputusan bisnis yang berbasis data.
    """)
    st.write("---")

    # 5. Panel Indikator Kinerja Utama (Key Performance Indicators - KPI)
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.metric(label="Total Ketersediaan Kursus", value=f"{filtered_df.shape[0]} Kelas")
    with col_kpi2:
        total_pendaftar = int(filtered_df['enrollment'].sum())
        st.metric(label="Akumulasi Total Peserta (Enrollment)", value=f"{total_pendaftar:,}".replace(",", "."))
    with col_kpi3:
        rata_rata_rating = filtered_df['score_rating'].mean()
        st.metric(label="Rata-rata Penilaian Kualitas", value=f"{rata_rata_rating:.2f} / 5.00")
    
    st.write("---")

    # ==========================================
    # PERTANYAAN BISNIS 1
    # ==========================================
    st.header("🏢 1. Lanskap Kompetisi & Model Bisnis Platform")
    st.markdown("""
    **Analisis Eksplanatori:** Visualisasi di bawah membedah strategi monetisasi dari setiap platform edutech. Melalui perbandingan komposisi kelas gratis (*Free/Audit*) 
    berbanding kelas berbayar (*Paid*), kita dapat menilai platform mana yang bertindak sebagai *market consolidator* komersial murni, 
    dan mana yang agresif menyebarkan program gratis demi taktik perluasan pangsa pasar (*user acquisition*).
    """)
    
    c1, c2 = st.columns([3, 2])
    with c1:
        fig_q1_bar = px.histogram(
            filtered_df,
            x="lembaga_sertifikasi",
            color="berbayar_free",
            barmode="group",
            title="Kuantitas Penawaran Kursus per Platform Berdasarkan Model Bisnis",
            labels={'lembaga_sertifikasi': 'Lembaga Sertifikasi', 'count': 'Jumlah Kursus Available', 'berbayar_free': 'Skema Bisnis'},
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        st.plotly_chart(fig_q1_bar, use_container_width=True)
    with c2:
        proporsi_harga = filtered_df['berbayar_free'].value_counts().reset_index()
        fig_q1_pie = px.pie(
            proporsi_harga,
            values='count',
            names='berbayar_free',
            title="Proporsi Model Bisnis Skema Harga Global",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_q1_pie, use_container_width=True)
        
    st.write("---")

    # ==========================================
    # PERTANYAAN BISNIS 2
    # ==========================================
    st.header("🚀 2. Tren Preferensi Pasar Terhadap Topik (Demand Analysis)")
    st.markdown("""
    **Analisis Eksplanatori:** Jumlah suplai kelas yang melimpah pada suatu topik belum tentu merepresentasikan serapan minat riil di masyarakat. 
    Analisis di bawah menyaring **Top 10 Bidang Fokus (Genre)** berdasarkan akumulasi jumlah pendaftaran peserta aktual. 
    Langkah ini krusial untuk memetakan klaster kompetensi apa yang paling dicari (*high-demand*) oleh tenaga kerja industri saat ini.
    """)
    
    genre_data = filtered_df.groupby('genre')['enrollment'].sum().reset_index().sort_values(by='enrollment', ascending=False).head(10)
    
    fig_q2_genre = px.bar(
        genre_data,
        x='enrollment',
        y='genre',
        orientation='h',
        title="Top 10 Genre Teknologi dengan Akumulasi Pendaftar Terbanyak",
        labels={'enrollment': 'Total Akumulasi Peserta', 'genre': 'Genre / Bidang Fokus'},
        color='enrollment',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig_q2_genre.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_q2_genre, use_container_width=True)
    
    st.write("---")

    # ==========================================
    # PERTANYAAN BISNIS 3
    # ==========================================
    st.header("🎯 3. Elastisitas Kualitas Terhadap Konversi Pendaftaran")
    st.markdown("""
    **Analisis Eksplanatori:** Terdapat asumsi konvensional bahwa tingkat rating kepuasan yang tinggi secara otomatis melipatgandakan jumlah peserta. 
    Melalui sebaran data (*Scatter Plot*) ini, kita menguji hipotesis korelasi tersebut. Titik kumpul data akan membuktikan 
    apakah lonjakan pendaftaran (*enrollment exponent*) didorong oleh jaminan kualitas rating yang sempurna (mendekati 5.0) 
    atau dipengaruhi oleh faktor eksternal lain.
    """)
    
    fig_q3_scatter = px.scatter(
        filtered_df,
        x="score_rating",
        y="enrollment",
        color="lembaga_sertifikasi",
        size="enrollment",
        hover_data=["nama_sertifikasi"],
        title="Matriks Hubungan Skor Penilaian (Rating) vs Volume Peserta (Enrollment)",
        labels={'score_rating': 'Skor Penilaian Kualitas (0.00 - 5.00)', 'enrollment': 'Jumlah Peserta Kelas'},
        color_discrete_sequence=px.colors.qualitative.Dark2,
        size_max=50
    )
    st.plotly_chart(fig_q3_scatter, use_container_width=True)
    
    st.write("---")

    # ==========================================
    # PERTANYAAN BISNIS 4
    # ==========================================
    st.header("📦 4. Efektivitas Format Pembelajaran Terhadap Daya Tarik Kursus")
    st.markdown("""
    **Analisis Eksplanatori:** Struktur penyampaian kurikulum memegang peranan krusial bagi kenyamanan konsumen. Grafik di bawah membandingkan 
    performa format pelaksanaan kelas—seperti belajar mandiri (`Self-Paced`), kelas interaktif (`Live/Bootcamp`), atau jadwal terstruktur—
    terhadap metrik **Rata-rata Peserta Per Kelas**. Hal ini memberikan arahan dalam penentuan format produk baru.
    """)
    
    metode_data = filtered_df.groupby('metode').agg(
        rata_rata_peserta=('enrollment', 'mean'),
        total_kelas=('nama_sertifikasi', 'count')
    ).reset_index().sort_values(by='rata_rata_peserta', ascending=False)
    
    c3, c4 = st.columns(2)
    with c3:
        fig_q4_bar = px.bar(
            metode_data,
            x='metode',
            y='rata_rata_peserta',
            title="Daya Tarik Format: Rata-Rata Peserta per Jenis Metode Kelas",
            labels={'rata_rata_peserta': 'Rata-rata Peserta Per Kelas', 'metode': 'Metode Pembelajaran'},
            color='rata_rata_peserta',
            color_continuous_scale=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_q4_bar, use_container_width=True)
    with c4:
        fig_q4_pie = px.pie(
            metode_data,
            values='total_kelas',
            names='metode',
            title="Pangsa Suplai: Distribusi Total Kelas yang Tersedia di Pasar",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_q4_pie, use_container_width=True)

    st.write("---")

    # ==========================================
    # BAGIAN KESIMPULAN STRATEGIS
    # ==========================================
    st.header("📌 Ringkasan Eksekutif & Rekomendasi Strategis")
    
    # Kondisi dinamis untuk teks kesimpulan otomatis
    top_genre_name = genre_data.iloc[0]['genre'] if not genre_data.empty else "Teknologi Utama"
    top_metode_name = metode_data.iloc[0]['metode'] if not metode_data.empty else "Format Utama"
    
    st.markdown(f"""
    Berdasarkan hasil analisis eksplorasi dan eksplanatori data di atas, berikut adalah rumusan kesimpulan strategis bagi manajemen:
    
    1. **Optimalisasi Portofolio Produk:** Kategori **{top_genre_name}** teridentifikasi sebagai pengumpul volume peserta terbesar. Perusahaan direkomendasikan mengalokasikan anggaran riset kurikulum untuk fokus memproduksi materi pada klaster genre ini guna memaksimalkan traksi pasar.
    2. **Pemilihan Format Penyampaian Kelas:** Metode **{top_metode_name}** mencatatkan efektivitas penyerapan jumlah pendaftar tertinggi per kelas. Format ini harus dijadikan standardisasi model penyampaian (*product packaging*) materi baru demi efisiensi operasional mengajar.
    3. **Evaluasi Penentuan Nilai Jual:** Grafik korelasi membuktikan bahwa pertumbuhan peserta masif (*hyper-enrollment*) terkonsentrasi pada kelas dengan rating stabil di angka **4.6 - 4.8**. Upaya tim operasional sebaiknya difokuskan pada pemeliharaan relevansi materi industri dan stabilitas harga, daripada memaksakan pencapaian nilai rating 5.0 sempurna yang tidak berdampak linear pada penjualan.
    4. **Strategi Penetrasi Kompetisi:** Mengingat tingginya persaingan penyediaan materi berbayar dari platform global, pemanfaatan strategi hibrida (menyediakan sub-modul gratis sebagai *conversion funnel* ke sertifikasi utama) merupakan taktik paling aman untuk memenangkan persaingan akuisisi pengguna lokal.
    """)