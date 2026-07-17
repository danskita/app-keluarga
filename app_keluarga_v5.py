import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import json
import os
import streamlit.components.v1 as components
from fpdf import FPDF

# Konfigurasi Halaman Web App
st.set_page_config(page_title="Jadwal Keluarga", page_icon="💖", layout="wide")

# ==========================================
# INISIALISASI DATABASE LOKAL (FILE JSON)
# ==========================================
DB_FILE = 'database_keluarga.json'

# Fungsi untuk menyimpan semua perubahan ke file JSON di komputer Anda
def save_to_db():
    data = {
        'anggota': st.session_state.anggota,
        'jadwal': st.session_state.jadwal,
        'master_rutinitas': st.session_state.master_rutinitas,
        'master_sekolah': st.session_state.master_sekolah,
        'master_masakan': st.session_state.master_masakan
    }
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Fungsi untuk menarik data dari file JSON saat aplikasi pertama kali dibuka
if 'data_loaded' not in st.session_state:
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
                st.session_state.anggota = data.get('anggota', [])
                st.session_state.jadwal = data.get('jadwal', [])
                st.session_state.master_rutinitas = data.get('master_rutinitas', [])
                st.session_state.master_sekolah = data.get('master_sekolah', [])
                st.session_state.master_masakan = data.get('master_masakan', [])
        except:
            st.error("File database rusak. Membuat database baru...")
            st.session_state.anggota = []
            st.session_state.jadwal = []
            st.session_state.master_rutinitas = []
            st.session_state.master_sekolah = []
            st.session_state.master_masakan = []
    else:
        # Jika file belum ada (baru pertama kali buka)
        st.session_state.anggota = []
        st.session_state.jadwal = []
        st.session_state.master_rutinitas = []
        st.session_state.master_sekolah = []
        st.session_state.master_masakan = []
    st.session_state.data_loaded = True

# Inisialisasi Master Masakan (Bawaan Aplikasi jika data kosong)
if 'master_masakan' not in st.session_state or not st.session_state.master_masakan:
    st.session_state.master_masakan = [
        {"Hari": "Senin", "Menu Utama": "Nasi, Oseng Kangkung, Tahu Goreng, Ayam Kecap", "Buah & Susu": "Pepaya, Susu", "Kandungan Gizi": "Serat, Protein Nabati & Hewani"},
        {"Hari": "Selasa", "Menu Utama": "Nasi, Sayur Asem, Tempe Mendoan, Ikan Bakar", "Buah & Susu": "Jeruk, Susu", "Kandungan Gizi": "Vitamin C, Protein, Omega 3"},
        {"Hari": "Rabu", "Menu Utama": "Nasi, Sayur Sop, Perkedel Kentang, Telur Balado", "Buah & Susu": "Pisang, Susu", "Kandungan Gizi": "Karbohidrat Kompleks, Vitamin, Protein"},
        {"Hari": "Kamis", "Menu Utama": "Nasi, Sayur Bayam Jagung, Bakwan, Daging Sapi Lada Hitam", "Buah & Susu": "Apel, Susu", "Kandungan Gizi": "Zat Besi, Protein Tinggi"},
        {"Hari": "Jumat", "Menu Utama": "Nasi, Capcay Sayur, Tahu Bakso, Udang Saus Tiram", "Buah & Susu": "Semangka, Susu", "Kandungan Gizi": "Serat Beragam, Yodium, Protein"},
        {"Hari": "Sabtu", "Menu Utama": "Nasi, Sayur Lodeh, Tempe Bacem, Ayam Goreng Lengkuas", "Buah & Susu": "Melon, Susu", "Kandungan Gizi": "Lemak Nabati, Serat, Protein"},
        {"Hari": "Minggu", "Menu Utama": "Nasi, Soto Ayam Sayur Kol, Telur Rebus, Sate Ayam", "Buah & Susu": "Mangga, Susu", "Kandungan Gizi": "Karbohidrat, Vitamin, Protein Lengkap"}
    ]

# ==========================================
# CUSTOM CSS (TAMPILAN MODERN)
# ==========================================
custom_css = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif !important; }
    .stApp { background-color: #F8F9FA; }
    .stButton > button { border-radius: 20px; font-weight: 700; transition: all 0.3s; border: none; }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .stAlert { border-radius: 15px; }
    h1, h2, h3 { color: #2C3E50; font-weight: 800; }
    [data-testid="stDataFrame"] { border-radius: 15px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
</style>
'''
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# SISTEM GEMBOK LOGIN
# ==========================================
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #ff9800; margin-top: 50px;'>Selamat Datang di App Keluarga 💖</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Silakan masukkan <b>Username</b> dan <b>Password</b> Anda.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("form_login"):
            st.markdown("### 🔐 Akses Masuk")
            username = st.text_input("Username Keluarga")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Buka Aplikasi", type="primary", use_container_width=True):
                if username == "keluarga" and password == "rahasia":
                    st.session_state.logged_in = True
                    st.rerun()
                else: st.error("❌ Username atau Password salah!")
    st.stop()

# ==========================================
# NAVIGASI SIDEBAR
# ==========================================
st.sidebar.markdown("### 👋 Halo, Keluarga!")
st.sidebar.caption("🟢 Status: Tersimpan di Komputer Lokal")
if st.sidebar.button("🚪 Keluar Aplikasi (Logout)", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.title("Navigasi 🧭")
st.sidebar.markdown("Mau ngatur apa hari ini?")

menu = st.sidebar.radio("Menu Navigasi", [
    "🏠 Beranda Keluarga", 
    "👨‍👩‍👧‍👦 1. Kenalan Dulu (Anggota)", 
    "⚙️ 2. Rutinitas Harian (Auto)",
    "📝 3. Jadwal Tambahan",
    "🕌 4. Jadwal Ibadah",
    "🍳 5. Menu Masakan Mingguan",
    "🎒 6. Jadwal Sekolah",
    "✏️ 7. Atur Ulang Jadwal",
    "🖨️ 8. Cetak Jadwal (PDF)"
], label_visibility="collapsed")

# ==========================================
# HALAMAN 1: MASTER DATA ANGGOTA
# ==========================================
if menu == "👨‍👩‍👧‍👦 1. Kenalan Dulu (Anggota)":
    st.header("Kenalan Dulu Yuk! 👨‍👩‍👧‍👦")
    with st.form("form_anggota", clear_on_submit=True):
        nama = st.text_input("Siapa namanya?")
        status = st.selectbox("Perannya di rumah?", ["Kepala Keluarga", "Ibu Rumah Tangga", "Pelajar Mahasiswa", "SMA", "SMP", "SD", "Belum Sekolah"])
        kesehatan = st.selectbox("Kondisi kesehatannya sekarang?", ["Alhamdulillah Sehat", "Lagi Sakit", "Masa Pemulihan"])
        penyakit = st.text_input("Sakit apa? (Boleh dikosongin kalau sehat)")
        if st.form_submit_button("Simpan Data! 🚀"):
            if nama.strip() == "": st.error("Namanya belum diisi tuh!")
            else:
                st.session_state.anggota.append({"Nama": nama, "Status": status, "Kesehatan": kesehatan, "Penyakit": penyakit if kesehatan != "Alhamdulillah Sehat" else "-"})
                save_to_db() # SINKRON KE LOKAL
                st.success(f"Data {nama} udah berhasil disimpan secara permanen! 🎉")
                st.rerun()
            
    if st.session_state.anggota:
        st.markdown("---")
        st.markdown("### 📋 Daftar Orang di Rumah (Bisa diedit lho!)")
        edited_anggota = st.data_editor(pd.DataFrame(st.session_state.anggota), num_rows="dynamic", width='stretch', key="editor_anggota")
        if st.button("💾 Simpan Perubahan ke Database", type="primary"):
            st.session_state.anggota = edited_anggota.to_dict('records')
            save_to_db()
            st.success("Perubahan udah disimpen ke database lokal!")

# ==========================================
# HALAMAN 2: MASTER RUTINITAS (AUTO)
# ==========================================
elif menu == "⚙️ 2. Rutinitas Harian (Auto)":
    st.header("Atur Rutinitas Harian Biar Praktis ⏰")
    if not st.session_state.anggota: st.warning("⚠️ Hayo, isi dulu data anggota keluarga di menu 'Kenalan Dulu' ya!")
    else:
        st.markdown("### 🪄 Mau Pake Template Standar Aja?")
        if st.button("✨ Load 7 Rutinitas Standar Sekaligus", type="secondary"):
            nama_semua = ", ".join([x["Nama"] for x in st.session_state.anggota])
            template_standar = [
                {"Kegiatan": "Bangun Tidur & Beres Kasur", "Jam Mulai": "04:30", "Jam Selesai": "05:00", "Penanggung Jawab": nama_semua},
                {"Kegiatan": "Mandi Pagi Biar Seger", "Jam Mulai": "05:30", "Jam Selesai": "06:00", "Penanggung Jawab": nama_semua},
                {"Kegiatan": "Sarapan Bareng", "Jam Mulai": "06:00", "Jam Selesai": "06:30", "Penanggung Jawab": nama_semua},
                {"Kegiatan": "Sekolah / Bekerja", "Jam Mulai": "07:00", "Jam Selesai": "14:00", "Penanggung Jawab": nama_semua},
                {"Kegiatan": "Istirahat Siang", "Jam Mulai": "14:00", "Jam Selesai": "15:00", "Penanggung Jawab": nama_semua},
                {"Kegiatan": "Makan Malam", "Jam Mulai": "19:00", "Jam Selesai": "19:30", "Penanggung Jawab": nama_semua},
                {"Kegiatan": "Tidur Malam", "Jam Mulai": "21:00", "Jam Selesai": "04:30", "Penanggung Jawab": nama_semua}
            ]
            count = 0
            for ts in template_standar:
                if not any(x["Kegiatan"] == ts["Kegiatan"] for x in st.session_state.master_rutinitas):
                    st.session_state.master_rutinitas.append(ts)
                    count += 1
            if count > 0:
                save_to_db()
                st.success(f"Mantap! {count} rutinitas standar udah ditambahin ke database.")
                st.rerun() 
            else: st.info("Template ini udah ada di daftar deh.")

        st.markdown("---")
        with st.form("form_master_rutin", clear_on_submit=True):
            st.markdown("### ➕ Bikin Rutinitas Baru Sendiri")
            kegiatan = st.selectbox("Kegiatan apa nih?", ["Bangun Tidur", "Mandi Pagi", "Sarapan", "Mandi Sore", "Makan Malam", "Tidur Malam", "Jam Belajar Wajib"])
            col1, col2 = st.columns(2)
            with col1: jam_mulai = st.time_input("Jam Mulai")
            with col2: jam_selesai = st.time_input("Jam Selesai")
            pic = st.multiselect("Buat siapa aja rutinitas ini?", [x["Nama"] for x in st.session_state.anggota])
            if st.form_submit_button("Simpan Rutinitas Baru"):
                if not pic: st.error("Pilih minimal 1 orang dong!")
                else:
                    st.session_state.master_rutinitas.append({"Kegiatan": kegiatan, "Jam Mulai": jam_mulai.strftime('%H:%M'), "Jam Selesai": jam_selesai.strftime('%H:%M'), "Penanggung Jawab": ", ".join(pic)})
                    save_to_db()
                    st.success("Rutinitas tersimpan aman di Database Lokal!")
        
        if st.session_state.master_rutinitas:
            edited_rutin = st.data_editor(pd.DataFrame(st.session_state.master_rutinitas), num_rows="dynamic", width='stretch', key="editor_rutinitas")
            if st.button("💾 Simpan Editan Rutinitas"):
                st.session_state.master_rutinitas = edited_rutin.to_dict('records')
                save_to_db()
                st.success("Editan udah disimpen ke database!")
                st.rerun()
            
            st.markdown("---")
            if st.button("🚀 Tarik Jadwal Rutinitas ke Beranda", type="primary"):
                tanggal_hari_ini = datetime.today().strftime("%d-%m-%Y")
                count = 0
                for rutin in st.session_state.master_rutinitas:
                    is_duplicate = any(j["Tanggal"] == tanggal_hari_ini and j["Kegiatan"] == rutin['Kegiatan'] and j["Penanggung Jawab"] == rutin['Penanggung Jawab'] for j in st.session_state.jadwal)
                    if not is_duplicate:
                        st.session_state.jadwal.append({"Tanggal": tanggal_hari_ini, "Waktu": f"{rutin['Jam Mulai']} - {rutin['Jam Selesai']}", "Kategori": "Rutinitas Tetap", "Kegiatan": rutin['Kegiatan'], "Penanggung Jawab": rutin['Penanggung Jawab'], "Selesai": False})
                        count += 1
                if count > 0: 
                    save_to_db()
                    st.success(f"Beres! {count} rutinitas udah masuk ke Beranda.")
                else: st.info("Semua rutinitas buat hari ini udah ditarik.")

# ==========================================
# HALAMAN 3: INPUT JADWAL & TUGAS (MANUAL)
# ==========================================
elif menu == "📝 3. Jadwal Tambahan":
    st.header("Bikin Jadwal Khusus / Dadakan 📝")
    if not st.session_state.anggota: st.warning("⚠️ Jangan lupa isi 'Kenalan Dulu' ya!")
    else:
        kategori = st.selectbox("Pilih Kategori", ["Tugas/Kewajiban", "Ibadah & Spiritual", "Waktu Luang", "Agenda Mendatang", "Kesehatan / Medis"])
        if kategori == "Tugas/Kewajiban": keg_options = ["Bekerja", "Belajar di rumah", "Memasak", "Mencuci piring", "Mencuci pakaian", "Menyapu rumah", "Beres kamar tidur"]
        elif kategori == "Ibadah & Spiritual": keg_options = ["Tahfidz / Hafalan Quran", "Doa Harian", "Ibadah Lainnya"]
        elif kategori == "Waktu Luang": keg_options = ["Bermain", "Menonton TV", "Istirahat santai", "Olahraga"]
        elif kategori == "Agenda Mendatang": keg_options = ["Liburan Keluarga", "Silaturahmi", "Belanja Bulanan", "Kerja Bakti"]
        elif kategori == "Kesehatan / Medis": keg_options = ["Minum Obat", "Kontrol ke Dokter", "Terapi / Perawatan"]
            
        kegiatan = st.selectbox("Kegiatannya Ngapain?", keg_options)
        
        with st.form("form_jadwal", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                tanggal = st.date_input("Kapan Dilaksanakannya?")
                jam_mulai = st.time_input("Jam Mulai")
            with col2:
                jam_selesai = st.time_input("Jam Selesainya Kapan?")
                
            nama_obat = aturan_minum = lokasi_dokter = menu_masak = gizi = mata_pelajaran = surat_ayat = detail_ibadah = ""
            
            if kategori == "Kesehatan / Medis":
                if kegiatan == "Minum Obat":
                    nama_obat = st.text_input("Nama Obatnya apa?")
                    aturan_minum = st.text_input("Aturan minumnya? (Cth: 3x sehari)")
                elif kegiatan == "Kontrol ke Dokter": lokasi_dokter = st.text_input("Lokasinya di mana?")
            elif kegiatan == "Memasak":
                menu_masak = st.text_input("Mau masak apa aja?")
                gizi = st.text_input("Catatan gizi (opsional)")
            elif kegiatan == "Belajar di rumah": mata_pelajaran = st.text_input("Belajar mata pelajaran apa?")
            elif kegiatan == "Tahfidz / Hafalan Quran": 
                surat_quran = {
                    "1. Al-Fatihah": 7, "2. Al-Baqarah": 286, "3. Ali 'Imran": 200, "112. Al-Ikhlas": 4, "113. Al-Falaq": 5, "114. An-Nas": 6
                }
                pilih_surat = st.selectbox("Hafalan Surat Apa?", list(surat_quran.keys()))
                jumlah_ayat_maks = surat_quran[pilih_surat]
                col_ay1, col_ay2 = st.columns(2)
                with col_ay1: ayat_mulai = st.number_input("Mulai Ayat:", min_value=1, max_value=jumlah_ayat_maks, step=1, value=1)
                with col_ay2: ayat_sampai = st.number_input("Sampai Ayat:", min_value=1, max_value=jumlah_ayat_maks, step=1, value=min(5, jumlah_ayat_maks))
                surat_ayat = f"{pilih_surat} (Ayat {ayat_mulai} - {ayat_sampai})"
            elif kegiatan in ["Ibadah Lainnya"]: detail_ibadah = st.text_input("Detail ibadahnya")

            pic = st.multiselect("Siapa nih yang ngerjain?", [x["Nama"] for x in st.session_state.anggota])
            
            if st.form_submit_button("Simpan Jadwal Tambahan"):
                if not pic: st.error("Pilih minimal 1 orang ya!")
                else:
                    catatan = ""
                    if nama_obat: catatan = f" - (Obat: {nama_obat}, Aturan: {aturan_minum})"
                    elif lokasi_dokter: catatan = f" - (Lokasi: {lokasi_dokter})"
                    elif menu_masak: catatan = f" - (Menu: {menu_masak} | Gizi: {gizi})"
                    elif mata_pelajaran: catatan = f" - (Materi: {mata_pelajaran})"
                    elif surat_ayat: catatan = f" - (Target: {surat_ayat})"
                    elif detail_ibadah: catatan = f" - ({detail_ibadah})"
                            
                    st.session_state.jadwal.append({"Tanggal": tanggal.strftime("%d-%m-%Y"), "Waktu": f"{jam_mulai.strftime('%H:%M')} - {jam_selesai.strftime('%H:%M')}", "Kategori": kategori, "Kegiatan": f"{kegiatan}{catatan}", "Penanggung Jawab": ", ".join(pic), "Selesai": False})
                    save_to_db() # SINKRON KE LOKAL
                    st.success("Sip! Jadwal tersimpan ke database.")

# ==========================================
# HALAMAN 4: AUTO-JADWAL IBADAH
# ==========================================
elif menu == "🕌 4. Jadwal Ibadah":
    st.header("Bikin Jadwal Ibadah Otomatis 🕌")
    if not st.session_state.anggota: st.warning("⚠️ Yuk isi 'Kenalan Dulu' sebelum bikin jadwal.")
    else:
        agama = st.selectbox("Agama / Kepercayaannya?", ["Islam", "Kristen", "Katolik", "Hindu", "Buddha", "Lainnya"])
        nama_anggota = [x["Nama"] for x in st.session_state.anggota]
        pic_ibadah = st.multiselect("Siapa aja yang mau ikut jadwal ibadah ini?", nama_anggota, default=nama_anggota)
        pj_str = ", ".join(pic_ibadah)
        tgl_hari_ini = datetime.today().strftime("%d-%m-%Y")
        hari_ini = datetime.today().weekday() 

        if agama == "Islam":
            kota = st.text_input("Tulis nama kotanya", value="Jakarta")
            if st.button("🚀 Ambil Jadwal Sholat Otomatis", type="primary"):
                with st.spinner('Menghubungi server...'):
                    try:
                        res = requests.get(f"https://api.aladhan.com/v1/timingsByCity?city={kota}&country=Indonesia&method=20")
                        count = 0
                        if res.json()['code'] == 200:
                            t = res.json()['data']['timings']
                            waktu = {"Sholat Subuh": t["Fajr"], "Sholat Dzuhur": t["Dhuhr"], "Sholat Ashar": t["Asr"], "Sholat Maghrib": t["Maghrib"], "Sholat Isya": t["Isha"]}
                            for s, j in waktu.items():
                                if not any(x["Tanggal"] == tgl_hari_ini and x["Kegiatan"] == s and x["Penanggung Jawab"] == pj_str for x in st.session_state.jadwal):
                                    st.session_state.jadwal.append({"Tanggal": tgl_hari_ini, "Waktu": f"{j} - Selesai", "Kategori": "Ibadah & Spiritual", "Kegiatan": s, "Penanggung Jawab": pj_str, "Selesai": False})
                                    count += 1
                            if count > 0: 
                                save_to_db()
                                st.success(f"Alhamdulillah! {count} jadwal sholat udah di-sync ke Database Lokal.")
                            else: st.info("Jadwal ibadah hari ini udah komplet.")
                    except Exception as e: st.error("Gagal ngambil data internet.")

# ==========================================
# HALAMAN 5: MENU MASAKAN MINGGUAN
# ==========================================
elif menu == "🍳 5. Menu Masakan Mingguan":
    st.header("Menu Masakan Mingguan 🍳")
    st.markdown("Ide menu biar nggak bingung mau masak apa hari ini. Bisa diedit juga lho!")
    
    edited_masakan = st.data_editor(pd.DataFrame(st.session_state.master_masakan), num_rows="dynamic", width='stretch', key="editor_masakan")
    
    if st.button("💾 Simpan Perubahan Menu", type="primary"):
        st.session_state.master_masakan = edited_masakan.to_dict('records')
        save_to_db()
        st.success("Perubahan menu masakan berhasil disimpan!")

    st.markdown("---")
    if not st.session_state.anggota: 
        st.warning("⚠️ Isi dulu data 'Kenalan Dulu' buat nentuin siapa yang masak ya.")
    else:
        hari_ini_indonesia = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
        hari_ini_str = hari_ini_indonesia[datetime.today().weekday()]
        
        if st.button(f"🚀 Jadikan Menu Hari {hari_ini_str} ke Jadwal Hari Ini", type="primary"):
            menu_hari_ini = next((m for m in st.session_state.master_masakan if m["Hari"] == hari_ini_str), None)
            
            if menu_hari_ini:
                tgl_hari_ini = datetime.today().strftime("%d-%m-%Y")
                kegiatan_str = f"Memasak - (Menu: {menu_hari_ini['Menu Utama']} | Gizi: {menu_hari_ini['Kandungan Gizi']})"
                pic_default = st.session_state.anggota[0]["Nama"] 
                
                if not any(j["Tanggal"] == tgl_hari_ini and j["Kegiatan"] == kegiatan_str for j in st.session_state.jadwal):
                    st.session_state.jadwal.append({"Tanggal": tgl_hari_ini, "Waktu": "05:00 - 06:30", "Kategori": "Tugas/Kewajiban", "Kegiatan": kegiatan_str, "Penanggung Jawab": pic_default, "Selesai": False})
                    save_to_db()
                    st.success(f"Mantap! Jadwal masak menu {hari_ini_str} udah ditarik ke Beranda.")
                    st.rerun()
                else: st.info("Menu masak hari ini udah ada di jadwal kok.")
            else: st.warning(f"Belum ada data menu untuk hari {hari_ini_str}.")

# ==========================================
# HALAMAN 6: JADWAL PELAJARAN SEKOLAH 
# ==========================================
elif menu == "🎒 6. Jadwal Sekolah":
    st.header("Jadwal Pelajaran Sekolah 🎒")
    murid = [x for x in st.session_state.anggota if x["Status"] in ["Pelajar Mahasiswa", "SMA", "SMP", "SD"]]
    
    if not st.session_state.anggota: st.warning("⚠️ Yuk isi 'Kenalan Dulu' sebelum lanjut.")
    elif not murid: st.info("💡 Nggak ada anggota keluarga berstatus pelajar nih.")
    else:
        with st.form("form_jadwal_sekolah", clear_on_submit=True):
            nama_murid = st.selectbox("Jadwalnya siapa?", [m["Nama"] for m in murid])
            hari_pilihan = st.selectbox("Hari apa?", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"])
            
            # MEMPERBAIKI NEWLINE (\n) PADA STRING LITERAL 
            jadwal_teks = st.text_area("Jadwal (Format: 07:00 - 08:30 | Matematika):", value="07:00 - 08:30 | Matematika\n08:30 - 10:00 | Bahasa Indonesia", height=120)
            
            if st.form_submit_button("Simpan Jadwal Sekolah"):
                if not jadwal_teks.strip(): st.error("Jadwal jangan kosong!")
                else:
                    lines = jadwal_teks.strip().split('\n')
                    count = 0
                    for line in lines:
                        if "|" in line:
                            w, m = line.split("|", 1)
                            w_bersih, m_bersih = w.strip(), m.strip()
                            if not any(x["Pelajar"] == nama_murid and x["Hari"] == hari_pilihan and x["Waktu"] == w_bersih and x["Pelajaran"] == m_bersih for x in st.session_state.master_sekolah):
                                st.session_state.master_sekolah.append({"Pelajar": nama_murid, "Hari": hari_pilihan, "Waktu": w_bersih, "Pelajaran": m_bersih})
                                count += 1
                    if count > 0: 
                        save_to_db()
                        st.success(f"Beres! Data pelajaran disimpen ke Database Lokal.")
                        st.rerun()

        if st.session_state.master_sekolah:
            st.markdown("---")
            edited_sekolah = st.data_editor(pd.DataFrame(st.session_state.master_sekolah), num_rows="dynamic", width='stretch', key="editor_sekolah")
            if st.button("💾 Simpan Perubahan"):
                st.session_state.master_sekolah = edited_sekolah.to_dict('records')
                save_to_db()
                st.success("Tersimpan ke database!")
                st.rerun()
                
            st.markdown("---")
            hari_ini_str = {0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 4: "Jumat", 5: "Sabtu", 6: "Minggu"}[datetime.today().weekday()]
            if st.button(f"🚀 Masukin Pelajaran Hari {hari_ini_str} ke Beranda", type="primary"):
                jadwal_hari_ini = [x for x in st.session_state.master_sekolah if x["Hari"] == hari_ini_str]
                count = 0
                for js in jadwal_hari_ini:
                    keg_mapel = f"Sekolah - {js['Pelajaran']}"
                    if not any(x["Tanggal"] == datetime.today().strftime("%d-%m-%Y") and x["Kegiatan"] == keg_mapel and x["Penanggung Jawab"] == js['Pelajar'] for x in st.session_state.jadwal):
                        st.session_state.jadwal.append({"Tanggal": datetime.today().strftime("%d-%m-%Y"), "Waktu": js['Waktu'], "Kategori": "Pelajaran Sekolah", "Kegiatan": keg_mapel, "Penanggung Jawab": js['Pelajar'], "Selesai": False})
                        count += 1
                if count > 0: 
                    save_to_db()
                    st.success("Tugas sekolah hari ini siap dikerjakan di Beranda!")
                else: st.info("Semua pelajaran hari ini udah masuk kok.")

# ==========================================
# HALAMAN 7: MANAJEMEN JADWAL (EDIT & HAPUS)
# ==========================================
elif menu == "✏️ 7. Atur Ulang Jadwal":
    st.header("Atur Ulang / Hapus Jadwal ✏️")
    if not st.session_state.jadwal: st.warning("⚠️ Belum ada jadwal apa-apa nih.")
    else:
        edited_df = st.data_editor(pd.DataFrame(st.session_state.jadwal), num_rows="dynamic", width='stretch', key="editor_jadwal")
        if st.button("💾 Simpan Hasil Edit", type="primary"):
            st.session_state.jadwal = edited_df.to_dict('records')
            save_to_db() # SINKRON KE LOKAL
            st.success("Mantap, perubahan udah disimpen ke Database!")
            
        st.markdown("---")
        pilihan_hapus = [f"[{i}] {j['Tanggal']} | Jam {j['Waktu']} | {j['Penanggung Jawab']} - {j['Kegiatan']}" for i, j in enumerate(st.session_state.jadwal)]
        jadwal_terpilih = st.selectbox("Pilih jadwal yang mau dihapus:", pilihan_hapus)
        if st.button("❌ Hapus Jadwal Ini"):
            if jadwal_terpilih:
                idx = int(jadwal_terpilih.split("]")[0].replace("[", ""))
                st.session_state.jadwal.pop(idx)
                save_to_db() # SINKRON KE LOKAL
                st.success("Jadwal dihapus permanen dari sistem.")
                st.rerun() 

# ==========================================
# HALAMAN 8: CETAK/SIMPAN PDF (FILTER LENGKAP)
# ==========================================
elif menu == "🖨️ 8. Cetak Jadwal (PDF)":
    st.header("Cetak Jadwal ke File PDF 🖨️")
    st.markdown("Gunakan menu ini untuk memfilter dan mengekspor jadwal menjadi dokumen PDF siap cetak.")
    
    if not st.session_state.jadwal:
        st.warning("⚠️ Belum ada jadwal yang dimasukkan. Silakan tambahkan jadwal terlebih dahulu.")
    elif not st.session_state.anggota:
        st.warning("⚠️ Belum ada data anggota keluarga.")
    else:
        df_jadwal = pd.DataFrame(st.session_state.jadwal)
        df_jadwal['Tanggal_Date'] = pd.to_datetime(df_jadwal['Tanggal'], format='%d-%m-%Y').dt.date
        
        st.markdown("### 🗓️ 1. Filter Rentang Waktu")
        rentang_waktu = st.radio("Pilih rentang waktu jadwal yang ingin dicetak:", ["Harian", "Mingguan", "Bulanan"], horizontal=True)
        
        if rentang_waktu == "Harian":
            tgl_pilih = st.date_input("Pilih Tanggal", datetime.today().date())
            df_filter_waktu = df_jadwal[df_jadwal['Tanggal_Date'] == tgl_pilih]
            periode_str = f"Tanggal: {tgl_pilih.strftime('%d-%m-%Y')}"
            
        elif rentang_waktu == "Mingguan":
            col_tgl1, col_tgl2 = st.columns(2)
            today_date = datetime.today().date()
            start_of_week = today_date - timedelta(days=today_date.weekday())
            with col_tgl1: start_date = st.date_input("Mulai Tanggal", start_of_week)
            with col_tgl2: end_date = st.date_input("Sampai Tanggal", start_of_week + timedelta(days=6))
            df_filter_waktu = df_jadwal[(df_jadwal['Tanggal_Date'] >= start_date) & (df_jadwal['Tanggal_Date'] <= end_date)]
            periode_str = f"Periode: {start_date.strftime('%d-%m-%Y')} s/d {end_date.strftime('%d-%m-%Y')}"
            
        elif rentang_waktu == "Bulanan":
            col_bln1, col_bln2 = st.columns(2)
            with col_bln1: bln = st.selectbox("Pilih Bulan", range(1, 13), index=datetime.today().month - 1)
            with col_bln2: thn = st.selectbox("Pilih Tahun", range(2023, 2030), index=datetime.today().year - 2023)
            df_filter_waktu = df_jadwal[(pd.to_datetime(df_jadwal['Tanggal_Date']).dt.month == bln) & (pd.to_datetime(df_jadwal['Tanggal_Date']).dt.year == thn)]
            nama_bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
            periode_str = f"Bulan: {nama_bulan[bln-1]} {thn}"

        st.markdown("---")
        st.markdown("### 🎯 2. Filter Target Cetak")
        target_cetak = st.radio("Bagaimana Anda ingin jadwal ditampilkan di PDF?", [
            "Semua Jadwal (Gabung menjadi satu)", 
            "Per Anggota Keluarga (Dipisah per halaman)", 
            "Hanya Kegiatan Bersama (Penanggung jawab lebih dari 1 orang)"
        ])
        
        st.markdown("---")
        if df_filter_waktu.empty:
            st.info(f"Tidak ada jadwal yang ditemukan untuk {periode_str}.")
        else:
            st.write(f"Ditemukan **{len(df_filter_waktu)} jadwal** pada rentang waktu ini.")
            
            if st.button("📄 Generate File PDF", type="primary"):
                pdf = FPDF()
                
                def cetak_tabel(pdf_obj, df_cetak, judul_halaman):
                    pdf_obj.add_page()
                    pdf_obj.set_font("Arial", 'B', 14)
                    pdf_obj.cell(190, 8, judul_halaman, ln=True, align='C')
                    pdf_obj.set_font("Arial", '', 10)
                    pdf_obj.cell(190, 6, periode_str, ln=True, align='C')
                    pdf_obj.ln(5)
                    
                    pdf_obj.set_font("Arial", 'B', 9)
                    col_widths = [22, 23, 30, 75, 40]
                    headers = ["Tanggal", "Waktu", "Kategori", "Kegiatan", "PIC"]
                    for i in range(len(headers)): 
                        pdf_obj.cell(col_widths[i], 8, headers[i], border=1, align='C')
                    pdf_obj.ln()
                    
                    pdf_obj.set_font("Arial", '', 8)
                    df_cetak = df_cetak.sort_values(by=["Tanggal_Date", "Waktu"])
                    for index, row in df_cetak.iterrows():
                        pdf_obj.cell(col_widths[0], 8, str(row['Tanggal'])[:10], border=1, align='C')
                        pdf_obj.cell(col_widths[1], 8, str(row['Waktu'])[:15], border=1, align='C')
                        pdf_obj.cell(col_widths[2], 8, str(row['Kategori'])[:20], border=1)
                        pdf_obj.cell(col_widths[3], 8, str(row['Kegiatan'])[:50], border=1)
                        pdf_obj.cell(col_widths[4], 8, str(row['Penanggung Jawab'])[:22], border=1)
                        pdf_obj.ln()

                if "Semua Jadwal" in target_cetak:
                    cetak_tabel(pdf, df_filter_waktu, "Master Jadwal Keseluruhan")
                elif "Per Anggota Keluarga" in target_cetak:
                    for anggota in st.session_state.anggota:
                        nama = anggota["Nama"]
                        df_member = df_filter_waktu[df_filter_waktu["Penanggung Jawab"].apply(lambda x: nama in str(x))]
                        if not df_member.empty:
                            cetak_tabel(pdf, df_member, f"Jadwal Aktivitas - {nama}")
                elif "Hanya Kegiatan Bersama" in target_cetak:
                    df_bersama = df_filter_waktu[df_filter_waktu["Penanggung Jawab"].apply(lambda x: "," in str(x))]
                    if not df_bersama.empty:
                        cetak_tabel(pdf, df_bersama, "Jadwal Kegiatan Bersama Keluarga")
                    else:
                        st.warning("⚠️ Tidak ada kegiatan bersama (Penanggung Jawab > 1) pada rentang waktu ini.")

                if pdf.page_no() > 0:
                    pdf_filename = "Laporan_Jadwal_Keluarga.pdf"
                    pdf.output(pdf_filename)
                    with open(pdf_filename, "rb") as pdf_file: PDFbyte = pdf_file.read()
                    st.success("File PDF berhasil dirender sesuai filter Anda!")
                    st.download_button(label="⬇️ Download PDF Sekarang", data=PDFbyte, file_name=pdf_filename, mime="application/octet-stream")

# ==========================================
# HALAMAN 9: DASHBOARD UTAMA & ALARM
# ==========================================
elif menu == "🏠 Beranda Keluarga":
    st.header("Pantau Jadwal Hari Ini Yuk! 🏠")
    
    st.markdown("### 🔔 Monitor Alarm")
    aktifkan_alarm = st.toggle("Aktifkan Alarm untuk jadwal 'Bangun Tidur' & 'Sholat'")
    
    if aktifkan_alarm:
        if not st.session_state.jadwal:
            st.warning("Belum ada jadwal hari ini. Alarm tidak dapat diaktifkan.")
        else:
            waktu_alarm = []
            for j in st.session_state.jadwal:
                keg = j["Kegiatan"].lower()
                if "sholat" in keg or "bangun tidur" in keg:
                    jam_mulai = j["Waktu"].split(" - ")[0].strip()
                    waktu_alarm.append(jam_mulai)
            
            waktu_alarm = list(set(waktu_alarm))
            
            if waktu_alarm:
                js_code = f'''
                <div style="background-color: #ffebee; padding: 20px; border-radius: 8px; text-align: center; border: 2px solid #f44336;">
                    <p id="alarm-status" style="font-family: sans-serif; font-size: 16px; color: #b71c1c; margin-bottom:15px;">
                        ⚠️ <b>Penting:</b> Browser memblokir suara otomatis. Anda wajib mengklik tombol di bawah ini agar alarm bisa berbunyi!
                    </p>
                    <button id="enable-audio-btn" style="padding: 12px 24px; font-size: 16px; font-weight: bold; cursor: pointer; background-color: #f44336; color: white; border: none; border-radius: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        🔊 IZINKAN SUARA ALARM
                    </button>
                    <!-- Menggunakan MP3 publik dari Mixkit -->
                    <audio id="audio-player" src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" preload="auto"></audio>
                </div>
                
                <script>
                    const alarmTimes = {{json.dumps(waktu_alarm)}};
                    let lastPlayed = "";
                    let isAudioEnabled = false;
                    
                    const audio = document.getElementById("audio-player");
                    const btn = document.getElementById("enable-audio-btn");
                    const statusText = document.getElementById("alarm-status");
                    
                    btn.addEventListener("click", () => {{
                        audio.play().then(() => {{
                            audio.pause();
                            audio.currentTime = 0;
                            isAudioEnabled = true;
                            
                            btn.style.display = "none";
                            statusText.innerHTML = "✅ <b>Monitor aktif!</b> Alarm siap berbunyi pada jam: " + alarmTimes.join(", ");
                            statusText.style.color = "#2e7d32";
                            statusText.parentElement.style.backgroundColor = "#e8f5e9";
                            statusText.parentElement.style.borderColor = "#4caf50";
                        }}).catch(err => {{
                            statusText.innerHTML = "❌ Gagal memutar suara: " + err.message;
                        }});
                    }});
                    
                    setInterval(() => {{
                        if (!isAudioEnabled) return;
                        const now = new Date();
                        const hh = now.getHours().toString().padStart(2, '0');
                        const mm = now.getMinutes().toString().padStart(2, '0');
                        const currentTime = hh + ":" + mm;
                        
                        if (alarmTimes.includes(currentTime) && lastPlayed !== currentTime) {{
                            audio.play();
                            statusText.innerHTML = "⏰ <b>ALARM BERBUNYI SEKARANG!</b> Waktunya: " + currentTime;
                            statusText.style.color = "#d32f2f";
                            lastPlayed = currentTime;
                        }}
                    }}, 1000);
                </script>
                '''
                components.html(js_code, height=150)
            else:
                st.warning("⚠️ Tidak ada jadwal 'Bangun Tidur' atau 'Sholat' yang terdeteksi di tabel hari ini.")

    st.markdown("---")
    
    if st.session_state.jadwal:
        df_jadwal = pd.DataFrame(st.session_state.jadwal).sort_values(by="Waktu")
        tgl_hari_ini = datetime.today().strftime('%d-%m-%Y')
        df_hari_ini = df_jadwal[df_jadwal['Tanggal'] == tgl_hari_ini]
        total_tugas = len(df_hari_ini)
        tugas_selesai = int(df_hari_ini["Selesai"].sum()) if not df_hari_ini.empty else 0
        progress_val = tugas_selesai / total_tugas if total_tugas > 0 else 0.0
        
        st.markdown(f"### 🗓️ Jadwal Buat Hari Ini ({tgl_hari_ini})")
        st.progress(progress_val, text=f"Progress: {tugas_selesai} dari {total_tugas} tugas udah selesai")
        
        if not df_hari_ini.empty:
            edited_df = st.data_editor(df_hari_ini, column_config={"Selesai": st.column_config.CheckboxColumn("✅ Udah Beres?", help="Centang kalau tugasnya udah kelar", default=False)}, disabled=["Tanggal", "Waktu", "Kategori", "Kegiatan", "Penanggung Jawab"], hide_index=True, width='stretch', key="dashboard_checklist")
            
            # Mendeteksi apakah ada tugas yang dicentang, lalu menyimpannya ke JSON
            updated_records = edited_df.to_dict('records')
            needs_save = False
            for rec in updated_records:
                for j in st.session_state.jadwal:
                    if j['Tanggal'] == rec['Tanggal'] and j['Waktu'] == rec['Waktu'] and j['Kegiatan'] == rec['Kegiatan'] and j['Penanggung Jawab'] == rec['Penanggung Jawab']:
                        if j['Selesai'] != rec['Selesai']:
                            j['Selesai'] = rec['Selesai']
                            needs_save = True
            
            if needs_save:
                save_to_db() # SINKRON KE LOKAL
                st.toast("✅ Perubahan status tugas berhasil disimpan ke sistem!")
        else: st.info("Eh, hari ini jadwalnya kosong nih. Yuk isi manual atau tarik dari Master Rutinitas!")
    else: st.info("Wah, masih kosong nih. Data belum tersedia.")
