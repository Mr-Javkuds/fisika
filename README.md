# 🎓 Python Learning - Physics Simulation Project

> **Proyek pembelajaran Python interaktif dengan simulasi momentum 2D dan dokumentasi lengkap 972 baris kode real!**

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-Clean%20Code-brightgreen.svg)](docs/index.html#clean-code)

---

## 📖 Tentang Proyek

Project ini adalah **pembelajaran Python hands-on** yang menggabungkan:
- 🎯 **Aplikasi nyata**: Simulasi fisika momentum 2D dengan GUI interaktif
- 📚 **Dokumentasi lengkap**: Tutorial Python dari basic hingga advanced (972 baris)
- ✨ **Best practices**: Clean code, modular architecture, DRY principles
- 🏗️ **Modern structure**: Modular web architecture dengan dynamic loading

**Perfect untuk:**
- Belajar Python dari dasar hingga mahir
- Memahami physics simulation programming
- Studi kasus clean code & best practices
- Referensi project structure yang baik

---

## ✨ Fitur Utama

### 🎮 Simulasi Fisika Interaktif
- **Momentum 2D Collision Simulator** dengan visualisasi real-time
- Mode 1D dan 2D (semi-realistic)
- Physics parameters yang bisa disesuaikan (mass, velocity, restitution)
- Real-time plotting dengan Matplotlib
- Data export ke CSV
- Trail effects untuk visualisasi trajectory

### 📚 Dokumentasi Komprehensif
- **8 Section** pembelajaran Python lengkap
- Contoh kode dari aplikasi nyata (bukan toy examples!)
- Interactive features: dark mode, code copy, smooth navigation
- Syntax highlighting dengan Prism.js
- Responsive design (mobile-friendly)

### 🏗️ Modern Architecture
- Modular project structure (src/, build/, docs/)
- Dynamic section loading (true modularity!)
- Clean separation of concerns
- Professional file organization

---

## 📁 Struktur Proyek

```
fisika/
├── 📦 src/                      # Source Code Python
│   └── momentum_2d.py          # Main application (972 lines)
│
├── 🔨 build/                    # Build Scripts
│   ├── html_helpers.py         # HTML generation utilities
│   ├── build_sections.py       # Section builder
│   └── generate_complete.py    # Complete HTML generator
│
├── 📚 docs/                     # Documentation Website
│   ├── index.html              # Main page (116 lines - modular!)
│   ├── assets/
│   │   ├── css/
│   │   │   └── styles.css      # Custom styling
│   │   └── js/
│   │       ├── main.js         # Interactive features
│   │       └── section-loader.js  # Dynamic loader
│   ├── sections/               # Content modules (8 sections)
│   │   ├── data_types.html
│   │   ├── functions.html
│   │   ├── loops.html
│   │   ├── oop.html
│   │   ├── physics.html
│   │   ├── structure.html
│   │   ├── clean_code.html
│   │   └── best_practices.html
│   └── downloads/
│       └── momentum_2d.py      # Downloadable source
│
├── 📊 dist/                     # Generated Files
│   └── python_learning_complete.html  # Built version
│
├── 🧪 tests/                    # Unit Tests (future)
│
├── 📖 docs_source/              # Learning Materials
│   └── examples/
│
├── start-server.bat            # One-click documentation server
├── README.md                   # This file
└── .gitignore                  # Git ignore rules
```

---

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.x** (3.6 atau lebih baru)
- **pip** (Python package manager)
- **Web browser** (Chrome, Firefox, Edge, etc.)

### 📦 Installation

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd fisika
   ```

2. **Install dependencies** (untuk aplikasi simulasi)
   ```bash
   pip install numpy matplotlib tkinter
   ```

3. **Selesai!** Tidak perlu instalasi tambahan untuk dokumentasi.

---

## 🎮 Cara Menggunakan

### 1️⃣ Menjalankan Simulasi Fisika

```bash
# Langsung jalankan aplikasi
py src/momentum_2d.py
```

**Features:**
- 🎚️ Atur parameter: mass, velocity (x, y), restitution coefficient
- 🎭 Pilih mode: 1D atau 2D (semi-realistic)
- ▶️ Start/Pause/Reset simulation
- 📊 Real-time graphs (Force, Momentum, Kinetic Energy)
- 💾 Export data ke CSV
- 🎨 Visual trail effects

---

### 2️⃣ Membuka Dokumentasi

**⚠️ PENTING**: Dokumentasi menggunakan **dynamic loading** dan HARUS dibuka dengan web server!

#### **Opsi A: One-Click Launcher** ⭐ **RECOMMENDED**

1. **Double-click** file `start-server.bat`
2. Server otomatis start di port 8000
3. Browser otomatis terbuka ke `http://localhost:8000`
4. **Done!** ✅

#### **Opsi B: Manual - Command Line**

```bash
# Masuk ke folder docs
cd docs

# Start web server (pilih salah satu)
py -m http.server 8000
# ATAU
python -m http.server 8000
# ATAU
python3 -m http.server 8000
```

Lalu buka browser ke: **`http://localhost:8000`**

#### **Opsi C: VS Code Live Server**

1. Install extension **"Live Server"** di VS Code
2. Right-click `docs/index.html`
3. Select **"Open with Live Server"**
4. Otomatis terbuka di browser dengan live reload!

---

### 3️⃣ Generate Complete HTML (Optional)

Untuk membuat single-file HTML (tanpa dynamic loading):

```bash
py build/generate_complete.py
```

Output: `dist/python_learning_complete.html` (dapat dibuka tanpa server)

---

## 📚 Konten Dokumentasi

### 🎯 Section 1: Data Types
- Numeric types (int, float)
- Strings & f-strings
- Booleans
- Collections (list, dict, deque)
- Type conversion best practices

### ⚙️ Section 2: Functions & Methods
- Function anatomy
- Type hints
- Docstrings
- Instance & private methods
- Callback functions
- Nested functions

### 🔄 Section 3: Loops & Control Flow
- For loops & while loops
- Enumerate & range
- List comprehensions
- Break, continue, pass
- Try-except error handling

### 🏛️ Section 4: Object-Oriented Programming (OOP)
- Classes & objects
- Constructors (`__init__`)
- Instance vs class attributes
- Methods
- Encapsulation principles

### 🎯 Section 5: Physics Implementation
- Vector operations dengan NumPy
- Collision detection
- Impulse-momentum calculations
- Physics state management

### 🏗️ Section 6: Code Structure
- Project organization
- Module imports
- Constants & configuration
- Separation of concerns

### ✨ Section 7: Clean Code Principles
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple)
- SRP (Single Responsibility)
- Naming conventions
- Guard clauses

### 🌟 Section 8: Best Practices
- Context managers (`with`)
- NumPy vectorization
- Defensive programming
- Data structure selection
- Python idioms

---

## 🛠️ Development

### 📝 Edit Documentation

Karena menggunakan modular architecture, edit sections sangat mudah:

```bash
# Edit individual section
code docs/sections/data_types.html

# Changes langsung terlihat saat refresh browser!
# Tidak perlu rebuild selama development
```

### 🎨 Customize Styling

```bash
# Edit CSS
code docs/assets/css/styles.css

# Edit JavaScript behavior
code docs/assets/js/main.js
```

### 🔨 Build Tools

Jika ingin modify build process:

```bash
# Edit section builder
code build/build_sections.py

# Edit HTML generator
code build/generate_complete.py

# Edit HTML helpers (jika sudah dibuat)
code build/html_helpers.py
```

---

## 🐛 Troubleshooting

### ❌ Sections tidak muncul / "Failed to load section" errors

**Penyebab**: File dibuka dengan `file://` protocol (double-click)

**Solusi**: 
- ✅ Gunakan web server (lihat cara di atas)
- ✅ Atau gunakan `dist/python_learning_complete.html`

**Detail**: Lihat `docs/CORS-FIX.md`

### ❌ Port 8000 sudah dipakai

```bash
# Ganti ke port lain
py -m http.server 8080  # Port 8080
py -m http.server 3000  # Port 3000
```

### ❌ Python command tidak ditemukan

- Windows: gunakan `py` instead of `python`
- Linux/Mac: gunakan `python3`
- Atau install Python dari [python.org](https://python.org)

### ❌ Module tidak ditemukan (simulasi)

```bash
# Install dependencies
pip install numpy matplotlib

# Atau dengan py
py -m pip install numpy matplotlib
```

---

## 🧪 Testing

```bash
# Run aplikasi simulasi (manual test)
py src/momentum_2d.py

# Open documentation (manual test)
start-server.bat

# Unit tests (future implementation)
# pytest tests/
```

---

## 🛤️ Roadmap

- [ ] Add unit tests untuk physics calculations
- [ ] Add more simulation modes (3D collision)
- [ ] Interactive playground di documentation
- [ ] Code challenges & exercises
- [ ] English translation
- [ ] Video tutorials

---

## 🤝 Contributing

Contributions welcome! Untuk contribute:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

Educational project - **free to use for learning purposes**.

Dibuat dengan ❤️ untuk pembelajaran Python

---

## 🔗 Resources

### Technologies Used
- **Python 3.x** - Main programming language
- **Tkinter** - GUI framework
- **NumPy** - Scientific computing
- **Matplotlib** - Plotting & visualization
- **Tailwind CSS** - Utility-first CSS (via CDN)
- **Prism.js** - Syntax highlighting
- **Font Awesome** - Icons

### Learning Resources
- [Python Official Docs](https://docs.python.org/3/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Clean Code Book](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Python Best Practices](https://docs.python-guide.org/)

---

## � Project Stats

- **Total Lines**: 972 (Python application)
- **Documentation Sections**: 8
- **Code Examples**: 50+
- **File Size Reduction**: 97% (3098 → 116 lines in index.html)
- **Architecture**: Modular & scalable

---

## 💬 Questions?

Jika ada pertanyaan atau menemukan bug:
1. Lihat **Troubleshooting** section di atas
2. Check `docs/CORS-FIX.md` untuk documentation issues
3. Review code comments di `src/momentum_2d.py`
4. Open an issue di repository

---

**Happy Learning! 🚀**
