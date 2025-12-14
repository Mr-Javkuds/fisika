# Proyek Pembelajaran Python - Fisika

Proyek pembelajaran Python dengan fokus pada simulasi fisika dan dokumentasi interaktif.

## 📁 Struktur Proyek

```
fisika/
├── src/                    # Source code Python
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
python -m http.server 8000
```
Kemudian buka `http://localhost:8000`

### 📱 Alternatif: Gunakan Live Server
- Install VS Code extension: "Live Server"
- Right-click `docs/index.html` → "Open with Live Server"

### Menjalankan Simulasi Fisika
```bash
python src/momentum_2d.py
```

## 📚 Fitur

- **Simulasi Momentum 2D**: Aplikasi interaktif dengan visualisasi real-time
- **Dokumentasi Lengkap**: Tutorial Python dari basic hingga advanced
- **Clean Code Examples**: Contoh-contoh best practices

## 🛠️ Teknologi

- Python 3.x
- Tkinter (GUI)
- NumPy (Komputasi)
- HTML/CSS/JavaScript (Dokumentasi)

## 📝 License

Educational project - free to use for learning purposes.
