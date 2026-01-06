"""
KOMPONEN UI
===========
Helper functions untuk membuat komponen UI Tkinter.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Any


def create_mode_selector(parent: ttk.Frame, 
                         mode_variable: tk.StringVar,
                         on_change_callback: Callable) -> ttk.Combobox:
    """
    Buat dropdown pemilihan mode simulasi.
    
    Parameters:
    -----------
    parent : ttk.Frame
        Parent widget
    mode_variable : tk.StringVar
        Variable untuk menyimpan nilai mode
    on_change_callback : Callable
        Callback ketika mode berubah
        
    Returns:
    --------
    ttk.Combobox
        Widget combobox
    """
    frame_mode = ttk.Frame(parent)
    frame_mode.pack(fill=tk.X, pady=2)
    
    ttk.Label(frame_mode, text="Mode Simulasi:").pack(side=tk.LEFT)
    
    combo_mode = ttk.Combobox(
        frame_mode, 
        values=["1D", "2D (semi)"], 
        textvariable=mode_variable, 
        state="readonly", 
        width=12
    )
    combo_mode.pack(side=tk.LEFT, padx=5)
    combo_mode.bind("<<ComboboxSelected>>", on_change_callback)
    
    return combo_mode


def create_restitution_selector(parent: ttk.Frame,
                                 restitution_variable: tk.StringVar) -> ttk.Frame:
    """
    Buat radio button pemilihan koefisien restitusi.
    
    Parameters:
    -----------
    parent : ttk.Frame
        Parent widget
    restitution_variable : tk.StringVar
        Variable untuk menyimpan nilai restitusi
        
    Returns:
    --------
    ttk.Frame
        Frame berisi radio buttons
    """
    ttk.Label(
        parent, 
        text="Koefisien Restitusi (e) / Elastisitas:"
    ).pack(anchor="w", pady=(5, 0))
    
    frame_radio = ttk.Frame(parent)
    frame_radio.pack(fill=tk.X)
    
    ttk.Radiobutton(
        frame_radio, 
        text="1.0 (Elastis)", 
        value="1.0", 
        variable=restitution_variable
    ).pack(side=tk.LEFT)
    
    ttk.Radiobutton(
        frame_radio, 
        text="0.5 (Semi)", 
        value="0.5", 
        variable=restitution_variable
    ).pack(side=tk.LEFT, padx=10)
    
    ttk.Radiobutton(
        frame_radio, 
        text="0.0 (Inelastis)", 
        value="0.0", 
        variable=restitution_variable
    ).pack(side=tk.LEFT)
    
    return frame_radio


def create_ball_input_row(parent: ttk.Frame, 
                          owner: Any,
                          title: str, 
                          mass_attr: str, mass_default: str,
                          vx_attr: str, vx_default: str, 
                          vy_attr: str, vy_default: str) -> ttk.Frame:
    """
    Buat baris input untuk parameter satu bola.
    
    Parameters:
    -----------
    parent : ttk.Frame
        Parent widget
    owner : Any
        Object tempat menyimpan entry widgets
    title : str
        Label bola (misal: "Benda 1")
    mass_attr, vx_attr, vy_attr : str
        Nama atribut untuk entry widget
    mass_default, vx_default, vy_default : str
        Nilai default
        
    Returns:
    --------
    ttk.Frame
        Frame berisi input fields
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
        setattr(owner, attr_name, entry)
    
    create_entry("m (kg):", mass_default, mass_attr)
    create_entry("vx (m/s):", vx_default, vx_attr)
    create_entry("vy (m/s):", vy_default, vy_attr)
    
    return frame


def create_position_sliders(parent: ttk.Frame,
                            on_slider_moved: Callable) -> dict:
    """
    Buat slider untuk mengatur posisi Y bola (mode 2D).
    
    Parameters:
    -----------
    parent : ttk.Frame
        Parent widget
    on_slider_moved : Callable
        Callback ketika slider digerakkan
        
    Returns:
    --------
    dict
        Dictionary berisi container dan slider widgets
    """
    slider_container = ttk.Frame(parent)
    slider_container.pack(fill=tk.X, pady=5)
    
    ttk.Separator(slider_container, orient='horizontal').pack(fill=tk.X, pady=5)
    
    frame_label = ttk.Frame(slider_container)
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
    ttk.Label(slider_container, text="Bola 1:").pack(anchor="w")
    position_y_slider_1 = ttk.Scale(
        slider_container, 
        from_=-200, 
        to=200, 
        command=on_slider_moved
    )
    position_y_slider_1.set(0)
    position_y_slider_1.pack(fill=tk.X)
    
    # Slider bola 2
    ttk.Label(slider_container, text="Bola 2:").pack(anchor="w")
    position_y_slider_2 = ttk.Scale(
        slider_container, 
        from_=-200, 
        to=200, 
        command=on_slider_moved
    )
    position_y_slider_2.set(0)
    position_y_slider_2.pack(fill=tk.X)
    
    return {
        "container": slider_container,
        "slider_1": position_y_slider_1,
        "slider_2": position_y_slider_2
    }


def create_control_buttons(parent: ttk.Frame,
                           start_callback: Callable,
                           pause_callback: Callable,
                           reset_callback: Callable) -> ttk.Frame:
    """
    Buat tombol kontrol simulasi.
    
    Parameters:
    -----------
    parent : ttk.Frame
        Parent widget
    start_callback : Callable
        Callback tombol START
    pause_callback : Callable
        Callback tombol PAUSE
    reset_callback : Callable
        Callback tombol RESET
        
    Returns:
    --------
    ttk.Frame
        Frame berisi tombol-tombol
    """
    frame_buttons = ttk.Frame(parent)
    frame_buttons.pack(fill=tk.X, pady=10)
    
    ttk.Button(
        frame_buttons, 
        text="▶️ START", 
        command=start_callback
    ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
    
    ttk.Button(
        frame_buttons, 
        text="⏸️ PAUSE", 
        command=pause_callback
    ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
    
    ttk.Button(
        frame_buttons, 
        text="🔄 RESET", 
        command=reset_callback
    ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
    
    return frame_buttons


def create_info_panel(parent: ttk.Frame) -> ttk.Label:
    """
    Buat panel info real-time.
    
    Parameters:
    -----------
    parent : ttk.Frame
        Parent widget
        
    Returns:
    --------
    ttk.Label
        Label untuk menampilkan info
    """
    info_box = ttk.LabelFrame(parent, text="📊 Info Real-time", padding=5)
    info_box.pack(fill=tk.X, pady=(0, 10))
    
    info_label = ttk.Label(
        info_box, 
        text="Siap untuk simulasi...", 
        font=("Consolas", 9), 
        justify=tk.LEFT
    )
    info_label.pack(anchor="w", fill=tk.X)
    
    return info_label
