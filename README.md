# Proyek Pembelajaran python - Fisika

Proyek pembelajaran python dengan fokus pada simulasi fisika dan dokumentasi interaktif.

## 📁 Struktur Proyek

```
fisika/
├── src/                    # Source code py
│   └── momentum_2d.py     # Aplikasi simulasi fisika
├── build/                  # Build scripts
│   ├── build_sections.py
│   └── generate_complete.py
├── docs/                   # Website documentation
│   ├── index.html
│   ├── assets/
│   │   ├── css/
│   │   └── js/
│   ├── sections/
│   └── downloads/
├── dist/                   # Generated files
└── docs_source/           # Learning materials
```

## 🚀 Quick Start

> **⚠️ IMPORTANT**: Dokumentasi menggunakan dynamic loading dan **HARUS dibuka dengan web server**, tidak bisa dengan double-click!

### 🌐 Cara 1: Gunakan Launcher (MUDAH!)
```bash
# Double-click file ini:
start-server.bat
```
Kemudian buka browser ke: `http://localhost:8000`

### 🌐 Cara 2: Manual Web Server
```bash
cd docs
py -m http.server 8000
```
Kemudian buka `http://localhost:8000`

### 📱 Alternatif: Gunakan Live Server
- Install VS Code extension: "Live Server"
- Right-click `docs/index.html` → "Open with Live Server"

### Menjalankan Simulasi Fisika
```bash
py src/momentum_2d.py
```

### 📖 Membuka Dokumentasi

**⚠️ PENTING**: Dokumentasi **HARUS** dibuka dengan web server (tidak bisa double-click HTML)!

#### **Opsi 1: One-Click Launcher** ⭐ TERMUDAH!
1. **Double-click** file `start-server.bat`
2. Browser otomatis ke: `http://localhost:8000`
3. Dokumentasi langsung terbuka dengan semua fitur!

#### **Opsi 2: Manual dengan py**
```bash
cd docs
py -m http.server 8000
```
Lalu buka browser ke: `http://localhost:8000`

#### **Opsi 3: VS Code Live Server**
1. Install extension "Live Server" di VS Code
2. Right-click `docs/index.html`
3. Pilih "Open with Live Server"

#### **Troubleshooting**
- Sections tidak muncul? → Pastikan buka dengan web server (bukan file://)
- Port 8000 sudah dipakai? → Ganti ke port lain: `py -m http.server 8080`
- Lihat `docs/CORS-FIX.md` untuk detail troubleshooting

## 📚 Fitur

- **Simulasi Momentum 2D**: Aplikasi interaktif dengan visualisasi real-time
- **Dokumentasi Lengkap**: Tutorial py dari basic hingga advanced
- **Clean Code Examples**: Contoh-contoh best practices

## 🛠️ Teknologi

- py 3.x
- Tkinter (GUI)
- NumPy (Komputasi)
- HTML/CSS/JavaScript (Dokumentasi)

## 📝 License

Educational project - free to use for learning purposes.
