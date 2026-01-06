"""
APLIKASI SIMULATOR UTAMA
========================
Aplikasi utama simulasi tumbukan interaktif.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from typing import Optional

from constants import (
    PIXELS_TO_METERS, TIME_STEP, COLLISION_DURATION,
    BALL_RADIUS_PIXELS, BALL_1_COLOR, BALL_2_COLOR,
    CANVAS_BG_COLOR, GRID_COLOR, GRID_STEP_PIXELS,
    CENTER_OF_MASS_COLOR
)
from ball import Ball
from physics import (
    calculate_collision, handle_wall_bounce,
    calculate_center_of_mass, calculate_physics_data
)
from ui_components import (
    create_mode_selector, create_restitution_selector,
    create_ball_input_row, create_position_sliders,
    create_control_buttons, create_info_panel
)


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
            bg=CANVAS_BG_COLOR, 
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
        self.info_label = create_info_panel(right_panel)
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
        self.mode_variable = tk.StringVar(value="1D")
        self.combo_mode = create_mode_selector(
            control_box, self.mode_variable, self._on_mode_changed
        )
        
        # Radio koefisien restitusi
        self.restitution_coefficient = tk.StringVar(value="1.0")
        create_restitution_selector(control_box, self.restitution_coefficient)
        
        # Input parameter bola
        ttk.Separator(control_box, orient='horizontal').pack(fill=tk.X, pady=5)
        create_ball_input_row(
            control_box, self,
            "🔴 Benda 1 (Merah)", 
            "entry_mass_1", "2.0", 
            "entry_velocity_1_x", "3.0", 
            "entry_velocity_1_y", "0.0"
        )
        create_ball_input_row(
            control_box, self,
            "🔵 Benda 2 (Biru)", 
            "entry_mass_2", "1.5", 
            "entry_velocity_2_x", "-1.5", 
            "entry_velocity_2_y", "0.0"
        )
        
        # Slider posisi Y (untuk mode 2D)
        slider_result = create_position_sliders(control_box, self._on_slider_moved)
        self.slider_container = slider_result["container"]
        self.position_y_slider_1 = slider_result["slider_1"]
        self.position_y_slider_2 = slider_result["slider_2"]
        
        # Tombol kontrol
        create_control_buttons(
            control_box,
            self.start_simulation,
            self.toggle_pause_simulation,
            self.reset_simulation
        )

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
            self.ball_1.position[1] = (center_y + offset_1) * PIXELS_TO_METERS
            self.ball_2.position[1] = (center_y + offset_2) * PIXELS_TO_METERS
            
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
        for x in range(0, canvas_width, GRID_STEP_PIXELS):
            self.canvas.create_line(
                x, 0, x, canvas_height, 
                fill=GRID_COLOR, 
                tags="grid"
            )
        
        # Garis horizontal
        for y in range(0, canvas_height, GRID_STEP_PIXELS):
            self.canvas.create_line(
                0, y, canvas_width, y, 
                fill=GRID_COLOR, 
                tags="grid"
            )
        
        self.canvas.tag_lower("grid")

    def _update_center_of_mass_marker(self) -> None:
        """Update posisi marker center of mass (pusat massa sistem)."""
        try:
            com_x, com_y = calculate_center_of_mass(self.ball_1, self.ball_2)
            
            # Konversi ke piksel
            com_x_px = com_x / PIXELS_TO_METERS
            com_y_px = com_y / PIXELS_TO_METERS
            
            if self.center_of_mass_id is None:
                self.center_of_mass_id = self.canvas.create_text(
                    com_x_px, com_y_px, 
                    text="✖", 
                    fill=CENTER_OF_MASS_COLOR, 
                    font=("Arial", 14, "bold")
                )
            else:
                self.canvas.coords(self.center_of_mass_id, com_x_px, com_y_px)
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
            BALL_RADIUS_PIXELS, 
            BALL_1_COLOR, 
            mass_1, 
            velocity_1_x, velocity_1_y, 
            PIXELS_TO_METERS
        )
        
        self.ball_2 = Ball(
            self.canvas, 
            canvas_width - 50, center_y, 
            BALL_RADIUS_PIXELS, 
            BALL_2_COLOR, 
            mass_2, 
            velocity_2_x, velocity_2_y, 
            PIXELS_TO_METERS
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
            # Reset log waktu & data sementara
            self.time_log.clear()
            self.force_log.clear()
            self.momentum_log.clear()
            self.kinetic_energy_log.clear()
            self.simulation_time = 0.0
            # Mulai loop
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
            # Tetap schedule check singkat saat pause
            self.animation_callback_id = self.root.after(50, self._run_loop)
            return

        # Move balls
        self.ball_1.move(TIME_STEP)
        self.ball_2.move(TIME_STEP)

        # Bounce off walls
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        handle_wall_bounce(self.ball_1, cw, ch, PIXELS_TO_METERS)
        handle_wall_bounce(self.ball_2, cw, ch, PIXELS_TO_METERS)

        # Handle collision antara dua bola
        restitution = float(self.restitution_coefficient.get())
        force, finished_impulse = calculate_collision(
            self.ball_1, self.ball_2, restitution, self.contact_tracker
        )
        self.last_collision_force = force
        
        # Plot impuls saat tumbukan selesai
        if finished_impulse > 0:
            self._plot_impulse(finished_impulse)

        # Logging dan update UI
        self._log_simulation_data()
        self._update_info_display()
        self._update_center_of_mass_marker()

        self.simulation_time += TIME_STEP
        # Schedule next frame
        self.animation_callback_id = self.root.after(int(TIME_STEP * 1000), self._run_loop)

    def _log_simulation_data(self) -> None:
        """Rekam data fisika tiap frame: waktu, gaya, momentum, energi kinetik."""
        p_tot, ke = calculate_physics_data(self.ball_1, self.ball_2)

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
            # Belum ada data log
            pass

    def _plot_impulse(self, impulse_val: float) -> None:
        """Gambar grafik pendek bentuk pulsa gaya berdasarkan nilai impuls total."""
        if impulse_val <= 0:
            return
        T = COLLISION_DURATION
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
