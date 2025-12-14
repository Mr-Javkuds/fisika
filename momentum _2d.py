"""
SIMULASI TUMBUKAN INTERAKTIF
=============================
Aplikasi simulasi fisika tumbukan 1D dan 2D dengan visualisasi real-time.

Author: Physics Education Team


KAMUS VARIABEL:
===============
Lihat dokumentasi lengkap di bagian docstring setiap class dan method.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from collections import deque
from typing import Tuple, Optional


# ==========================================
# KELAS BOLA (Ball Object)
# ==========================================
class Ball:
    """
    Representasi objek bola dalam simulasi fisika.
    
    ATRIBUT:
    --------
    canvas : tk.Canvas
        Canvas Tkinter untuk menggambar
    radius_pixels : float
        Jari-jari bola dalam piksel
    radius_meters : float
        Jari-jari bola dalam meter (untuk fisika)
    mass : float
        Massa bola (kg)
    position : np.array
        Posisi [x, y] dalam meter
    velocity : np.array
        Kecepatan [vx, vy] dalam m/s
    trail_points : deque
        Queue titik-titik jejak bola
    color : str
        Warna bola (hex)
    """
    
    # Konstanta Class
    TRAIL_MAX_LENGTH = 30
    TRAIL_POINT_MIN_SIZE = 2
    TRAIL_POINT_MAX_SIZE = 5
    BORDER_WIDTH = 2
    
    def __init__(self, 
                 canvas: tk.Canvas, 
                 x_pixels: float, 
                 y_pixels: float, 
                 radius_pixels: float, 
                 color: str, 
                 mass: float, 
                 velocity_x: float, 
                 velocity_y: float, 
                 pixels_to_meters: float):
        """
        Inisialisasi objek bola.

        Parameters
        ----------
        canvas : tk.Canvas
        Canvas untuk menggambar
        
        x_pxels : float
        Posisi awal sumbu X dalam piksel
        
        y_pxels : float
        Posisi awal sumbu Y dalam piksel
        
        radus_pixels : float
        Jari-jari bola dalam piksel
        
        colr : str
        Warna bola (kode hex)
        
        mas : float
        Massa bola dalam kg
        
        velcity_x : float
        Kecepatan awal sumbu X dalam m/s
        
        velcity_y : float
        Kecepatan awal sumbu Y dalam m/s
        
        pixls_to_meters : float
        Faktor konversi piksel ke meter
        
        """
        self.canvas = canvas
        self.radius_pixels = radius_pixels
        self.radius_meters = radius_pixels * pixels_to_meters
        self.mass = float(mass)
        self.pixels_to_meters = pixels_to_meters
        self.color = color

        # Posisi dan kecepatan dalam satuan meter dan m/s
        self.position = np.array([x_pixels * pixels_to_meters, 
                                  y_pixels * pixels_to_meters], dtype=float)
        self.velocity = np.array([velocity_x, velocity_y], dtype=float)

        # Trail (jejak bola)
        self.trail_points = deque(maxlen=self.TRAIL_MAX_LENGTH)
        self.trail_ids = []

        # Gambar bola di canvas
        self.canvas_id = canvas.create_oval(
            x_pixels - radius_pixels, 
            y_pixels - radius_pixels, 
            x_pixels + radius_pixels, 
            y_pixels + radius_pixels,
            fill=color, 
            outline="black", 
            width=self.BORDER_WIDTH
        )

    def draw_trail(self) -> None:
        """Menggambar jejak pergerakan bola."""
        # Hapus jejak lama
        for trail_id in self.trail_ids:
            self.canvas.delete(trail_id)
        self.trail_ids.clear()

        # Gambar jejak baru dengan efek fade
        for index, (trail_x, trail_y) in enumerate(self.trail_points):
            # Size bertambah seiring dengan index (efek fade)
            size = self.TRAIL_POINT_MIN_SIZE + \
                   (index / self.TRAIL_MAX_LENGTH) * self.TRAIL_POINT_MAX_SIZE
            
            fill_color = self.color if index % 2 == 0 else ""
            if fill_color:
                trail_id = self.canvas.create_oval(
                    trail_x - size, trail_y - size, 
                    trail_x + size, trail_y + size,
                    fill=self.color, 
                    outline="", 
                    stipple="gray50"
                )
                self.trail_ids.append(trail_id)

    def update_visual_position(self) -> None:
        """Update posisi visual bola di canvas."""
        pixels_x = self.position[0] / self.pixels_to_meters
        pixels_y = self.position[1] / self.pixels_to_meters

        self.canvas.coords(
            self.canvas_id,
            pixels_x - self.radius_pixels, 
            pixels_y - self.radius_pixels,
            pixels_x + self.radius_pixels, 
            pixels_y + self.radius_pixels
        )

    def move(self, time_step: float) -> None:
        """
        Gerakkan bola berdasarkan kecepatan dan waktu.
        
        Parameters:
        -----------
        time_step : float
            Delta waktu (detik)
        """
        # Update posisi: s = s₀ + v·Δt
        self.position += self.velocity * time_step
        
        # Konversi ke piksel untuk visual
        pixels_x = self.position[0] / self.pixels_to_meters
        pixels_y = self.position[1] / self.pixels_to_meters
        
        # Simpan posisi untuk jejak
        self.trail_points.append((pixels_x, pixels_y))
        
        # Update visual
        self.draw_trail()
        self.update_visual_position()


# ==========================================
# APLIKASI SIMULATOR UTAMA
# ==========================================
class CollisionSimulatorApp:
    """
    Aplikasi utama simulasi tumbukan interaktif.
    
    ATRIBUT UTAMA:
    --------------
    Physics Constants:
        PIXELS_TO_METERS : float (0.01)
        TIME_STEP : float (0.02 s)
        
    Simulation State:
        is_running : bool
        is_paused : bool
        simulation_time : float
        
    Data Logging:
        time_log : list (waktu dalam detik)
        force_log : list (gaya dalam Newton)
        momentum_log : list (momentum total)
        kinetic_energy_log : list (energi kinetik total)
        
    Ball Objects:
        ball_1 : Ball (bola merah)
        ball_2 : Ball (bola biru)
    """
    
    # ===== KONSTANTA FISIKA =====
    PIXELS_TO_METERS = 0.01  # 1 px = 0.01 m
    TIME_STEP = 0.02  # 20 ms per frame
    
    # ===== KONSTANTA VISUAL =====
    BALL_RADIUS_PIXELS = 20
    BALL_1_COLOR = "#e63946"  # Merah
    BALL_2_COLOR = "#457b9d"  # Biru
    CENTER_OF_MASS_COLOR = "#2a9d8f"  # Hijau tosca
    CANVAS_BG_COLOR = "#f5f5f5"
    GRID_COLOR = "#e0e0e0"
    GRID_STEP_PIXELS = 50
    
    # ===== KONSTANTA TUMBUKAN =====
    COLLISION_DURATION = 0.05  # Asumsi durasi tumbukan (s)
    
    def __init__(self, root: tk.Tk):
        """Inisialisasi aplikasi simulator."""
        self.root = root
        self.root.title("Simulasi Tumbukan Interaktif - Physics Engine v2.0")
        self.root.geometry("1100x750")
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        # Setup tema
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # State simulasi
        self.is_running = False
        self.is_paused = False
        self.animation_callback_id: Optional[int] = None
        
        # Parameter fisika
        self.simulation_time = 0.0
        self.last_collision_force = 0.0
        
        # Data logging
        self.time_log = []
        self.force_log = []
        self.momentum_log = []
        self.kinetic_energy_log = []
        
        # Tracking kontak tumbukan
        self.contact_tracker = {
            "in_contact": False,
            "impulse_accumulated": 0.0,
            "force_samples": []
        }
        
        # Marker center of mass
        self.center_of_mass_id: Optional[int] = None
        
        # Setup UI
        self._setup_user_interface()
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        
        # Setup awal
        self._toggle_slider_visibility()
        self.reset_simulation()

    def _on_window_close(self) -> None:
        """Handler untuk menutup aplikasi dengan aman."""
        self.is_running = False
        if self.animation_callback_id:
            try:
                self.root.after_cancel(self.animation_callback_id)
            except ValueError:
                pass
        self.root.destroy()

    # ==========================================
    # SETUP USER INTERFACE
    # ==========================================
    def _setup_user_interface(self) -> None:
        """Setup seluruh komponen UI."""
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Setup panel kiri dan kanan
        self._setup_left_panel(main_frame)
        self._setup_right_panel(main_frame)

    def _setup_left_panel(self, parent: ttk.Frame) -> None:
        """Setup panel kiri (canvas visualisasi)."""
        left_panel = ttk.Frame(parent)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ttk.Label(
            left_panel, 
            text="Visualisasi Area Tumbukan", 
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.canvas = tk.Canvas(
            left_panel, 
            bg=self.CANVAS_BG_COLOR, 
            highlightthickness=1, 
            highlightbackground="#aaa"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def _setup_right_panel(self, parent: ttk.Frame) -> None:
        """Setup panel kanan (kontrol dan info)."""
        right_panel = ttk.Frame(parent)
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.columnconfigure(0, weight=1)

        self._setup_control_panel(right_panel)
        self._setup_info_panel(right_panel)
        self._setup_graph_panel(right_panel)
        
        ttk.Button(
            right_panel, 
            text="📊 Export CSV", 
            command=self.export_data_to_csv
        ).pack(fill=tk.X, pady=(5, 0))

    def _setup_control_panel(self, parent: ttk.Frame) -> None:
        """Setup panel kontrol parameter fisika."""
        control_box = ttk.LabelFrame(parent, text="⚙️ Parameter Fisika", padding=10)
        control_box.pack(fill=tk.X, pady=(0, 10))

        # Mode dropdown
        self._setup_mode_selector(control_box)
        
        # Radio koefisien restitusi
        self._setup_restitution_selector(control_box)
        
        # Input parameter bola
        ttk.Separator(control_box, orient='horizontal').pack(fill=tk.X, pady=5)
        self._create_ball_input_row(
            control_box, 
            "🔴 Benda 1 (Merah)", 
            "entry_mass_1", "2.0", 
            "entry_velocity_1_x", "3.0", 
            "entry_velocity_1_y", "0.0"
        )
        self._create_ball_input_row(
            control_box, 
            "🔵 Benda 2 (Biru)", 
            "entry_mass_2", "1.5", 
            "entry_velocity_2_x", "-1.5", 
            "entry_velocity_2_y", "0.0"
        )
        
        # Slider posisi Y (untuk mode 2D)
        self._setup_position_sliders(control_box)
        
        # Tombol kontrol
        self._setup_control_buttons(control_box)

    def _setup_mode_selector(self, parent: ttk.Frame) -> None:
        """Setup dropdown pemilihan mode simulasi."""
        frame_mode = ttk.Frame(parent)
        frame_mode.pack(fill=tk.X, pady=2)
        
        ttk.Label(frame_mode, text="Mode Simulasi:").pack(side=tk.LEFT)
        
        self.mode_variable = tk.StringVar(value="1D")
        self.combo_mode = ttk.Combobox(
            frame_mode, 
            values=["1D", "2D (semi)"], 
            textvariable=self.mode_variable, 
            state="readonly", 
            width=12
        )
        self.combo_mode.pack(side=tk.LEFT, padx=5)
        self.combo_mode.bind("<<ComboboxSelected>>", self._on_mode_changed)

    def _setup_restitution_selector(self, parent: ttk.Frame) -> None:
        """Setup radio button pemilihan koefisien restitusi."""
        ttk.Label(
            parent, 
            text="Koefisien Restitusi (e) / Elastisitas:"
        ).pack(anchor="w", pady=(5, 0))
        
        self.restitution_coefficient = tk.StringVar(value="1.0")
        frame_radio = ttk.Frame(parent)
        frame_radio.pack(fill=tk.X)
        
        ttk.Radiobutton(
            frame_radio, 
            text="1.0 (Elastis)", 
            value="1.0", 
            variable=self.restitution_coefficient
        ).pack(side=tk.LEFT)
        
        ttk.Radiobutton(
            frame_radio, 
            text="0.5 (Semi)", 
            value="0.5", 
            variable=self.restitution_coefficient
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Radiobutton(
            frame_radio, 
            text="0.0 (Inelastis)", 
            value="0.0", 
            variable=self.restitution_coefficient
        ).pack(side=tk.LEFT)

    def _create_ball_input_row(self, parent: ttk.Frame, 
                               title: str, 
                               mass_attr: str, mass_default: str,
                               vx_attr: str, vx_default: str, 
                               vy_attr: str, vy_default: str) -> None:
        """
        Membuat baris input untuk parameter satu bola.
        
        Parameters:
        -----------
        parent : ttk.Frame
            Parent widget
        title : str
            Label bola (misal: "Benda 1")
        mass_attr, vx_attr, vy_attr : str
            Nama atribut untuk entry widget
        mass_default, vx_default, vy_default : str
            Nilai default
        """
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(frame, text=title, font=("", 8, "bold")).pack(anchor="w")
        
        frame_inputs = ttk.Frame(frame)
        frame_inputs.pack(fill=tk.X)
        
        # Helper function untuk membuat entry
        def create_entry(label: str, default: str, attr_name: str):
            ttk.Label(frame_inputs, text=label, font=("", 8)).pack(side=tk.LEFT)
            entry = ttk.Entry(frame_inputs, width=5, font=("", 8))
            entry.insert(0, default)
            entry.pack(side=tk.LEFT, padx=(0, 5))
            setattr(self, attr_name, entry)
        
        create_entry("m (kg):", mass_default, mass_attr)
        create_entry("vx (m/s):", vx_default, vx_attr)
        create_entry("vy (m/s):", vy_default, vy_attr)

    def _setup_position_sliders(self, parent: ttk.Frame) -> None:
        """Setup slider untuk mengatur posisi Y bola (mode 2D)."""
        self.slider_container = ttk.Frame(parent)
        self.slider_container.pack(fill=tk.X, pady=5)
        
        ttk.Separator(self.slider_container, orient='horizontal').pack(fill=tk.X, pady=5)
        
        frame_label = ttk.Frame(self.slider_container)
        frame_label.pack(fill=tk.X)
        ttk.Label(
            frame_label, 
            text="Posisi Y (Offset):", 
            font=("", 8, "bold")
        ).pack(side=tk.LEFT)
        ttk.Label(
            frame_label, 
            text="(0 = Tengah)", 
            font=("", 7, "italic"), 
            foreground="gray"
        ).pack(side=tk.RIGHT)
        
        # Slider bola 1
        ttk.Label(self.slider_container, text="Bola 1:").pack(anchor="w")
        self.position_y_slider_1 = ttk.Scale(
            self.slider_container, 
            from_=-200, 
            to=200, 
            command=self._on_slider_moved
        )
        self.position_y_slider_1.set(0)
        self.position_y_slider_1.pack(fill=tk.X)
        
        # Slider bola 2
        ttk.Label(self.slider_container, text="Bola 2:").pack(anchor="w")
        self.position_y_slider_2 = ttk.Scale(
            self.slider_container, 
            from_=-200, 
            to=200, 
            command=self._on_slider_moved
        )
        self.position_y_slider_2.set(0)
        self.position_y_slider_2.pack(fill=tk.X)

    def _setup_control_buttons(self, parent: ttk.Frame) -> None:
        """Setup tombol kontrol simulasi."""
        frame_buttons = ttk.Frame(parent)
        frame_buttons.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            frame_buttons, 
            text="▶️ START", 
            command=self.start_simulation
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        
        ttk.Button(
            frame_buttons, 
            text="⏸️ PAUSE", 
            command=self.toggle_pause_simulation
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        
        ttk.Button(
            frame_buttons, 
            text="🔄 RESET", 
            command=self.reset_simulation
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)

    def _setup_info_panel(self, parent: ttk.Frame) -> None:
        """Setup panel info real-time."""
        info_box = ttk.LabelFrame(parent, text="📊 Info Real-time", padding=5)
        info_box.pack(fill=tk.X, pady=(0, 10))
        
        self.info_label = ttk.Label(
            info_box, 
            text="Siap untuk simulasi...", 
            font=("Consolas", 9), 
            justify=tk.LEFT
        )
        self.info_label.pack(anchor="w", fill=tk.X)

    def _setup_graph_panel(self, parent: ttk.Frame) -> None:
        """Setup panel grafik impuls."""
        graph_frame = ttk.LabelFrame(parent, text="📈 Grafik Impuls", padding=15)
        graph_frame.pack(fill=tk.BOTH, expand=True)
        
        # Setup matplotlib figure
        self.figure, self.axes = plt.subplots(figsize=(4, 3), dpi=85)
        self.figure.patch.set_facecolor('#f0f0f0')
        self.axes.set_facecolor('white')
        self.axes.grid(True, linestyle='--', alpha=0.5)
        self.axes.set_xlabel("Waktu (s)", fontsize=8)
        self.axes.set_ylabel("Gaya (N)", fontsize=8)
        self.figure.tight_layout()
        
        self.chart_canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ==========================================
    # EVENT HANDLERS
    # ==========================================
    def _on_mode_changed(self, event=None) -> None:
        """Handler ketika mode simulasi berubah."""
        self._toggle_slider_visibility()
        self.reset_simulation()

    def _toggle_slider_visibility(self) -> None:
        """Toggle visibility slider posisi Y berdasarkan mode."""
        current_mode = self.mode_variable.get()
        if current_mode == "1D":
            self.slider_container.pack_forget()
        else:
            # Pack setelah elemen ke-3 di parent
            children = self.slider_container.master.winfo_children()
            if len(children) > 3:
                self.slider_container.pack(after=children[3], fill=tk.X, pady=5)

    def _on_slider_moved(self, event=None) -> None:
        """Handler ketika slider posisi Y digerakkan."""
        if not self.is_running:
            self._sync_balls_to_slider()

    def _sync_balls_to_slider(self) -> None:
        """Sinkronkan posisi bola dengan nilai slider."""
        try:
            canvas_height = self.canvas.winfo_height()
            if canvas_height < 10:
                canvas_height = 400
            
            center_y = canvas_height / 2
            
            # Ambil offset dari slider
            offset_1 = self.position_y_slider_1.get()
            offset_2 = self.position_y_slider_2.get()
            
            # Update posisi bola
            self.ball_1.position[1] = (center_y + offset_1) * self.PIXELS_TO_METERS
            self.ball_2.position[1] = (center_y + offset_2) * self.PIXELS_TO_METERS
            
            # Update visual
            self.ball_1.update_visual_position()
            self.ball_2.update_visual_position()
            self._update_center_of_mass_marker()
        except AttributeError:
            pass

    def _on_canvas_resize(self, event) -> None:
        """Handler ketika canvas diresize."""
        self._draw_grid()
        
        canvas_height = self.canvas.winfo_height()
        safe_limit = (canvas_height / 2) - 50
        if safe_limit < 10:
            safe_limit = 100
        
        if canvas_height > 100:
            self.position_y_slider_1.config(from_=-safe_limit, to=safe_limit)
            self.position_y_slider_2.config(from_=-safe_limit, to=safe_limit)
            
            if not self.is_running:
                self._sync_balls_to_slider()

    # ==========================================
    # VISUAL HELPERS
    # ==========================================
    def _draw_grid(self) -> None:
        """Menggambar grid di canvas."""
        self.canvas.delete("grid")
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Garis vertikal
        for x in range(0, canvas_width, self.GRID_STEP_PIXELS):
            self.canvas.create_line(
                x, 0, x, canvas_height, 
                fill=self.GRID_COLOR, 
                tags="grid"
            )
        
        # Garis horizontal
        for y in range(0, canvas_height, self.GRID_STEP_PIXELS):
            self.canvas.create_line(
                0, y, canvas_width, y, 
                fill=self.GRID_COLOR, 
                tags="grid"
            )
        
        self.canvas.tag_lower("grid")

    def _update_center_of_mass_marker(self) -> None:
        """Update posisi marker center of mass (pusat massa sistem)."""
        try:
            total_mass = self.ball_1.mass + self.ball_2.mass
            
            # Hitung posisi COM: r_com = (m1·r1 + m2·r2) / (m1 + m2)
            com_position = (
                self.ball_1.position * self.ball_1.mass + 
                self.ball_2.position * self.ball_2.mass
            ) / total_mass
            
            # Konversi ke piksel
            com_x = com_position[0] / self.PIXELS_TO_METERS
            com_y = com_position[1] / self.PIXELS_TO_METERS
            
            if self.center_of_mass_id is None:
                self.center_of_mass_id = self.canvas.create_text(
                    com_x, com_y, 
                    text="✖", 
                    fill=self.CENTER_OF_MASS_COLOR, 
                    font=("Arial", 14, "bold")
                )
            else:
                self.canvas.coords(self.center_of_mass_id, com_x, com_y)
                self.canvas.tag_raise(self.center_of_mass_id)
        except:
            pass

    # ==========================================
    # CORE SIMULATION LOGIC
    # ==========================================
    def reset_simulation(self) -> None:
        """Reset simulasi ke kondisi awal."""
        self.is_running = False
        self.is_paused = False
        
        # Clear data logs
        self.time_log.clear()
        self.force_log.clear()
        self.momentum_log.clear()
        self.kinetic_energy_log.clear()
        
        # Reset contact tracker
        self.contact_tracker = {
            "in_contact": False,
            "impulse_accumulated": 0.0,
            "force_samples": []
        }
        
        # Clear canvas
        self.canvas.delete("all")
        self._draw_grid()
        
        # Clear graph
        self.axes.clear()
        self.axes.grid(True, linestyle='--', alpha=0.5)
        self.chart_canvas.draw()
        
        self.center_of_mass_id = None
        
        # Baca parameter dari input
        try:
            mass_1 = float(self.entry_mass_1.get())
            velocity_1_x = float(self.entry_velocity_1_x.get())
            velocity_1_y = float(self.entry_velocity_1_y.get())
            
            mass_2 = float(self.entry_mass_2.get())
            velocity_2_x = float(self.entry_velocity_2_x.get())
            velocity_2_y = float(self.entry_velocity_2_y.get())
        except ValueError:
            messagebox.showerror("Error", "Input tidak valid! Gunakan angka.")
            return
        
        # Ukuran canvas
        canvas_width = self.canvas.winfo_width()
        canvas_width = 600 if canvas_width < 10 else canvas_width
        canvas_height = self.canvas.winfo_height()
        canvas_height = 400 if canvas_height < 10 else canvas_height
        center_y = canvas_height / 2
        
        # Reset slider
        self.position_y_slider_1.set(0)
        self.position_y_slider_2.set(0)
        
        # Buat bola baru
        self.ball_1 = Ball(
            self.canvas, 
            50, center_y, 
            self.BALL_RADIUS_PIXELS, 
            self.BALL_1_COLOR, 
            mass_1, 
            velocity_1_x, velocity_1_y, 
            self.PIXELS_TO_METERS
        )
        
        self.ball_2 = Ball(
            self.canvas, 
            canvas_width - 50, center_y, 
            self.BALL_RADIUS_PIXELS, 
            self.BALL_2_COLOR, 
            mass_2, 
            velocity_2_x, velocity_2_y, 
            self.PIXELS_TO_METERS
        )
        
        self.simulation_time = 0.0
        self._update_info_display()
        self._update_center_of_mass_marker()
        self._toggle_slider_visibility()

    def start_simulation(self) -> None:
        """Mulai simulasi."""
        if not self.is_running:
            # Sync posisi jika mode 2D
            if self.mode_variable.get() != "1D":
                self._sync_balls_to_slider()
            self.is_running = True
            # reset log waktu & data sementara
            self.time_log.clear()
            self.force_log.clear()
            self.momentum_log.clear()
            self.kinetic_energy_log.clear()
            self.simulation_time = 0.0
            # mulai loop
            self._run_loop()

    def toggle_pause_simulation(self) -> None:
        """Toggle pause / resume."""
        if self.is_running:
            self.is_paused = not self.is_paused

    def _run_loop(self) -> None:
        """Loop utama simulasi (dipanggil berulang menggunakan after)."""
        if not self.is_running:
            return

        if self.is_paused:
            # tetap schedule check singkat saat pause
            self.animation_callback_id = self.root.after(50, self._run_loop)
            return

        # Move balls
        self.ball_1.move(self.TIME_STEP)
        self.ball_2.move(self.TIME_STEP)

        # Bounce off walls (simple reflection)
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()

        for b in (self.ball_1, self.ball_2):
            px = b.position[0] / self.PIXELS_TO_METERS
            py = b.position[1] / self.PIXELS_TO_METERS
            # kiri / kanan
            if px - b.radius_pixels < 0:
                b.position[0] = b.radius_pixels * self.PIXELS_TO_METERS
                b.velocity[0] *= -1
            elif px + b.radius_pixels > cw:
                b.position[0] = (cw - b.radius_pixels) * self.PIXELS_TO_METERS
                b.velocity[0] *= -1
            # atas / bawah
            if py - b.radius_pixels < 0:
                b.position[1] = b.radius_pixels * self.PIXELS_TO_METERS
                b.velocity[1] *= -1
            elif py + b.radius_pixels > ch:
                b.position[1] = (ch - b.radius_pixels) * self.PIXELS_TO_METERS
                b.velocity[1] *= -1

        # Handle collision antara dua bola
        self._handle_collision()

        # Logging dan update UI
        self._log_simulation_data()
        self._update_info_display()
        self._update_center_of_mass_marker()

        self.simulation_time += self.TIME_STEP
        # schedule next frame
        self.animation_callback_id = self.root.after(int(self.TIME_STEP * 1000), self._run_loop)

    def _handle_collision(self) -> None:
        """Deteksi dan tangani tumbukan antara ball_1 dan ball_2."""
        b1 = self.ball_1
        b2 = self.ball_2

        pos_diff = b1.position - b2.position
        dist = np.linalg.norm(pos_diff)
        min_dist = b1.radius_meters + b2.radius_meters
        F_sample = 0.0

        if dist <= min_dist:
            # normal vector (dari b2 ke b1)
            n = pos_diff / (dist + 1e-9)
            v_rel = b1.velocity - b2.velocity
            v_norm = np.dot(v_rel, n)

            # Resolve overlap (positional correction)
            overlap = max(0.0, min_dist - dist)
            if overlap > 0:
                total_m = b1.mass + b2.mass
                # geser sesuai perbandingan massa (mempertahankan pusat massa)
                b1.position += (overlap * (b2.mass / total_m)) * n
                b2.position -= (overlap * (b1.mass / total_m)) * n

            # Jika relatif bergerak saling mendekat -> hitung impuls
            if v_norm < 0:
                e = float(self.restitution_coefficient.get())
                # impuls skalar j
                j = -(1 + e) * v_norm
                j /= (1.0 / b1.mass + 1.0 / b2.mass)
                impulse_vec = j * n

                # update velocity
                b1.velocity += impulse_vec / b1.mass
                b2.velocity -= impulse_vec / b2.mass

                # approximasi gaya rata-rata selama satu TIME_STEP
                F_sample = abs(j) / max(self.TIME_STEP, 1e-9)

                # update contact tracker
                ct = self.contact_tracker
                if not ct["in_contact"]:
                    ct["in_contact"] = True
                    ct["impulse_accumulated"] = 0.0
                ct["impulse_accumulated"] += j
                ct["force_samples"].append(F_sample)
        else:
            # jika sebelumnya dalam kontak dan sekarang terpisah, finalize impuls
            ct = self.contact_tracker
            if ct["in_contact"]:
                total_impulse = abs(ct["impulse_accumulated"])
                # plot hasil impuls saat tumbukan selesai
                self._plot_impulse(total_impulse)
                # reset tracker
                ct["in_contact"] = False
                ct["impulse_accumulated"] = 0.0
                ct["force_samples"].clear()

        self.last_collision_force = F_sample

    def _log_simulation_data(self) -> None:
        """Rekam data fisika tiap frame: waktu, gaya, momentum, energi kinetik."""
        # total momentum vektor
        p_vec = self.ball_1.mass * self.ball_1.velocity + self.ball_2.mass * self.ball_2.velocity
        p_tot = np.linalg.norm(p_vec)
        # energi kinetik total
        ke = 0.5 * self.ball_1.mass * np.dot(self.ball_1.velocity, self.ball_1.velocity) + \
             0.5 * self.ball_2.mass * np.dot(self.ball_2.velocity, self.ball_2.velocity)

        self.time_log.append(self.simulation_time)
        self.force_log.append(self.last_collision_force)
        self.momentum_log.append(p_tot)
        self.kinetic_energy_log.append(ke)

    def _update_info_display(self) -> None:
        """Perbarui label info realtime."""
        try:
            txt = (f"t: {self.simulation_time:.2f}s | P_tot: {self.momentum_log[-1]:.2f} kg·m/s | "
                   f"KE: {self.kinetic_energy_log[-1]:.2f} J\n"
                   f"V1: {np.linalg.norm(self.ball_1.velocity):.2f} m/s | "
                   f"V2: {np.linalg.norm(self.ball_2.velocity):.2f} m/s")
            self.info_label.config(text=txt)
        except IndexError:
            # belum ada data log
            pass

    def _plot_impulse(self, impulse_val: float) -> None:
        """Gambar grafik pendek bentuk pulsa gaya berdasarkan nilai impuls total."""
        if impulse_val <= 0:
            return
        T = self.COLLISION_DURATION
        t = np.linspace(0, T, 50)
        Fmax = (impulse_val * np.pi) / (2 * T)
        F = Fmax * np.sin(np.pi * t / T)

        self.axes.clear()
        self.axes.plot(t, F, lw=2)
        self.axes.fill_between(t, F, alpha=0.3)
        self.axes.text(T/2, Fmax * 0.55, f"Impuls = {impulse_val:.2f} Ns",
                       ha="center", fontsize=10, fontweight="bold",
                       bbox=dict(boxstyle="round", fc="white", alpha=0.8))
        self.axes.set_xlabel("Waktu (s)")
        self.axes.set_ylabel("Gaya (N)")
        self.axes.grid(True, linestyle=":", alpha=0.6)
        self.figure.tight_layout()
        self.chart_canvas.draw()

    def export_data_to_csv(self) -> None:
        """Export data log simulasi ke file CSV."""
        if not self.time_log:
            messagebox.showinfo("Info", "Belum ada data untuk diekspor.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not path:
            return

        try:
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["t (s)", "F (N)", "P_total (kg·m/s)", "KE_total (J)"])
                for i in range(len(self.time_log)):
                    writer.writerow([
                        f"{self.time_log[i]:.5f}",
                        f"{self.force_log[i]:.5f}",
                        f"{self.momentum_log[i]:.5f}",
                        f"{self.kinetic_energy_log[i]:.5f}"
                    ])
            messagebox.showinfo("Sukses", "Data berhasil diekspor ke CSV.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan file: {e}")

# --------------------------------
# MAIN
# --------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CollisionSimulatorApp(root)
    root.mainloop()
