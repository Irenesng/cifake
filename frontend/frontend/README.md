# Frontend Demo - Deteksi Citra Sintetis AI (Streamlit)

Aplikasi web interaktif berbasis **Streamlit** untuk mendemonstrasikan klasifikasi citra CIFAKE secara real-time dan menampilkan visualisasi interpretabilitas **Grad-CAM++**.

---

## 1. Menjalankan Lokal

1. Masuk ke direktori frontend:
   ```bash
   cd production/frontend
   ```
2. Pasang dependensi:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi Streamlit:
   ```bash
   streamlit run app.py
   ```
4. Buka peramban di [http://localhost:8501](http://localhost:8501).
5. Pada sidebar kiri, atur URL backend jika menggunakan Railway (atau default `http://127.0.0.1:8000` jika backend berjalan lokal).

---

## 2. Deploy ke Streamlit Community Cloud

1. **Unggah ke GitHub**:
   Pastikan folder `frontend` diunggah ke repository GitHub Anda (misal dalam satu repo atau repo terpisah).
2. **Deploy**:
   - Masuk ke [share.streamlit.io](https://share.streamlit.io).
   - Klik **New app**.
   - Pilih repository GitHub Anda, branch `main`, dan tentukan file path `production/frontend/app.py`.
3. **Konfigurasi Environment Variable (Secrets)**:
   - Pada menu **Advanced settings** di Streamlit Cloud, tambahkan secret URL backend Railway:
     ```toml
     BACKEND_API_URL = "https://url-backend-railway-anda.up.railway.app"
     ```
   - Klik **Deploy!**.
