# Chatterbox TTS API

Chatterbox TTS API adalah REST API berperforma tinggi untuk Text-to-Speech (TTS) yang mendukung kloning suara, multibahasa (23 bahasa), dan streaming real-time. API ini dirancang agar kompatibel dengan standar OpenAI, memudahkan integrasi dengan berbagai aplikasi.

## Fitur Utama

- **OpenAI Compatible**: Mendukung endpoint `/v1/audio/speech`.
- **Voice Cloning**: Kloning suara instan hanya dengan sampel audio singkat.
- **Multilingual**: Mendukung 23 bahasa termasuk Indonesia.
- **Streaming**: Dukungan streaming audio secara real-time (WAV atau SSE).
- **Long Text Processing**: Memproses teks yang sangat panjang secara efisien di background.
- **Voice Library**: Kelola koleksi suara Anda sendiri.

## Instalasi (Docker)

Pastikan Anda sudah menginstal Docker dan Docker Compose.

1.  Clone repository ini (jika belum).
2.  Sesuaikan konfigurasi di file `.env`.
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

#### Python
```python
import requests

response = requests.post(
    "http://localhost:4123/v1/audio/speech",
    json={
        "input": "Halo, ini adalah contoh suara dari Python.",
        "voice": "alloy",
        "model": "chatterbox-multilingual"
    }
)

if response.status_code == 200:
    with open("speech.wav", "wb") as f:
        f.write(response.content)
    print("Berhasil menyimpan audio ke speech.wav")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
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

### 3. Long Text TTS (Background Processing)

Untuk teks yang sangat panjang (hingga 100.000 karakter), gunakan endpoint `long-text`.

#### cURL
```bash
curl -X POST http://localhost:4123/v1/tts/long-text \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Masukkan teks yang sangat panjang di sini...",
    "voice": "onyx"
  }'
```

Response akan memberikan `job_id` yang bisa digunakan untuk mengecek status:
```bash
curl http://localhost:4123/v1/tts/long-text/status/{job_id}
```

### 4. Health Check

```bash
curl http://localhost:4123/v1/health
```

## Konfigurasi Port

Secara default, API berjalan di port **4123**. Jika Anda menggunakan Docker atau Coolify, pastikan port ini sudah di-expose atau disesuaikan melalui environment variable `PORT`.

---
© 2026 Adsmedia.ai Development 
