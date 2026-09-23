import io
import os
import base64
import requests
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Deteksi Citra AI",
    page_icon="🔍",
    layout="wide"
)

with st.sidebar:
    st.header("Pengaturan")
    default_api_url = "http://127.0.0.1:8000"
    if "BACKEND_API_URL" in st.secrets:
        default_api_url = st.secrets["BACKEND_API_URL"]
    elif os.getenv("BACKEND_API_URL"):
        default_api_url = os.getenv("BACKEND_API_URL")
    api_url = st.text_input(
        "URL Backend API",
        value=default_api_url,
        help="Alamat endpoint server backend FastAPI"
    ).rstrip("/")

    enable_xai = st.toggle("Aktifkan Grad-CAM++", value=True)

    try:
        health_resp = requests.get(f"{api_url}/health", timeout=3)
        if health_resp.status_code == 200:
            health_data = health_resp.json()
            is_ready = health_data.get("model_status") == "ready"
            status_text = "Model Siap" if is_ready else "Mode Simulasi"
            st.success(f"Backend Terhubung ({status_text})")
        else:
            st.warning("Backend merespons dengan status selain 200.")
    except Exception:
        st.error("Gagal terhubung ke backend. Pastikan server sudah berjalan.")

st.title("Sistem Deteksi Keaslian Citra")
st.write("Klasifikasi citra autentik (nyata) versus citra sintetis hasil generasi AI berbasis arsitektur EfficientNetB0-SE dan Explainable AI (Grad-CAM++).")

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("Unggah Gambar")
    uploaded_file = st.file_uploader(
        "Pilih file citra",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption=f"Citra uji: {uploaded_file.name}", use_container_width=True)
        btn_analyze = st.button("Analisis Citra", type="primary", use_container_width=True)
    else:
        st.info("Pilih berkas citra berformat JPG atau PNG untuk dianalisis.")
        btn_analyze = False

with col_right:
    st.subheader("Hasil Analisis")

    if uploaded_file is not None and btn_analyze:
        with st.spinner("Memproses citra..."):
            try:
                uploaded_file.seek(0)
                file_bytes = uploaded_file.read()
                files = {"file": (uploaded_file.name, file_bytes, uploaded_file.type)}

                endpoint = f"{api_url}/explain" if enable_xai else f"{api_url}/predict"
                response = requests.post(endpoint, files=files, timeout=30)

                if response.status_code == 200:
                    data = response.json()
                    pred = data.get("prediction", data)

                    label = pred["label"]
                    confidence = pred["confidence"] * 100
                    latency = pred.get("inference_time_ms", 0)
                    raw_score = pred.get("raw_score", 0)
                    is_real = label == "REAL"

                    if is_real:
                        st.success(f"Hasil: Citra Asli (REAL)")
                    else:
                        st.error(f"Hasil: Citra AI (FAKE)")

                    m1, m2 = st.columns(2)
                    m1.metric("Tingkat Keyakinan", f"{confidence:.2f}%")
                    m2.metric("Waktu Inferensi", f"{latency} ms")

                    st.caption(f"Skor Sigmoid Model: {raw_score:.4f}")

                    if enable_xai and "gradcam_overlay_base64" in data:
                        st.divider()
                        st.subheader("Visualisasi Grad-CAM++")
                        st.caption("Area panas (merah/kuning) menandakan area piksel yang paling dominan mempengaruhi keputusan model.")

                        overlay_data = base64.b64decode(data["gradcam_overlay_base64"])
                        overlay_image = Image.open(io.BytesIO(overlay_data))
                        st.image(overlay_image, caption="Peta Atensi Grad-CAM++", use_container_width=True)

                else:
                    try:
                        err_msg = response.json().get("detail", response.text)
                    except Exception:
                        err_msg = response.text
                    st.error(f"Error dari server ({response.status_code}): {err_msg}")

            except requests.exceptions.ConnectionError:
                st.error("Gagal terhubung ke backend FastAPI. Pastikan server sudah aktif.")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {str(e)}")

    elif uploaded_file is None:
        st.info("Silakan unggah citra terlebih dahulu di panel sebelah kiri.")
