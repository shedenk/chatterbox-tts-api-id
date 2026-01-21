# Chatterbox TTS API

Chatterbox TTS API adalah REST API berperforma tinggi untuk Text-to-Speech (TTS) yang mendukung kloning suara, multibahasa (23 bahasa), dan streaming real-time. API ini dirancang agar kompatibel dengan standar OpenAI, memudahkan integrasi dengan berbagai aplikasi, dan memiliki optimasi khusus untuk Bahasa Indonesia.

## Fitur Utama

- **OpenAI Compatible**: Mendukung endpoint `/v1/audio/speech`.
- **Indonesian Optimized**: Menggunakan model khusus yang dioptimasi untuk ucapan Bahasa Indonesia yang natural.
- **Voice Cloning**: Kloning suara instan hanya dengan sampel audio singkat.
- **Multilingual**: Mendukung 23 bahasa dengan kemampuan model multibahasa.
- **Streaming & SSE**: Dukungan streaming audio secara real-time (WAV) atau melalui Server-Side Events (SSE).
- **Long Text Processing**: Memproses teks sangat panjang (hingga 100.000 karakter) di background dengan sistem antrean job.
- **Voice Library**: Kelola koleksi suara kustom Anda secara persisten.
- **Diagnostic Logging**: Dilengkapi dengan logs detail (breadcrumb) untuk memudahkan debugging konektivitas.

## Instalasi (Docker)

Pastikan Anda sudah menginstal Docker dan Docker Compose.

1.  Clone repository ini.
2.  Salin `.env.example` ke `.env` dan sesuaikan konfigurasinya:
    ```bash
    cp .env.example .env
    ```
3.  Jalankan aplikasi:
    ```bash
    docker-compose up --build
    ```

API akan tersedia di `http://localhost:4123`. Dokumentasi interaktif (Swagger UI) dapat diakses di `http://localhost:4123/docs`.

## API Usage Samples

### 1. Basic Text-to-Speech (WAV)

#### cURL
```bash
curl -X POST http://localhost:4123/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Halo, selamat datang di layanan Chatterbox TTS API.",
    "voice": "alloy",
    "model": "chatterbox-multilingual"
  }' \
  --output speech.wav
```

### 2. Streaming Audio (Real-time)

#### cURL (WAV Stream)
```bash
curl -X POST http://localhost:4123/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Streaming audio memungkinkan Anda mendengar suara saat sedang diproses.",
    "voice": "nova",
    "stream": true
  }' --no-buffer > stream.wav
```

#### SSE Streaming (Server-Sent Events)
Untuk mendapatkan audio chunk-by-chunk melalui SSE:
```bash
curl -X POST http://localhost:4123/v1/audio/speech/upload \
  -F "input=Halo dari streaming SSE" \
  -F "stream_format=sse"
```

### 3. Long Text TTS (> 3000 Karakter)

Untuk teks yang sangat panjang, gunakan sistem job background:

#### Create Job
```bash
curl -X POST http://localhost:4123/v1/tts/long-text \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Masukkan teks yang sangat panjang (> 3000 karakter) di sini...",
    "voice": "onyx"
  }'
```

#### Check Status
Gunakan `job_id` dari response di atas:
```bash
curl http://localhost:4123/v1/tts/long-text/status/{job_id}
```

### 4. Health Check & Connectivity

#### Root Health (Basic Connectivity)
```bash
curl http://localhost:4123/
```

#### Detailed Health (Model Status)
```bash
curl http://localhost:4123/v1/health
```

## Konfigurasi Port

Secara default, API berjalan di port **4123**. Anda dapat mengubahnya melalui environment variable `PORT` di file `.env`.

---
© 2026 Adsmedia.ai Development
 
