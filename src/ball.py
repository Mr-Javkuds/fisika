"""
KELAS BOLA (Ball Object)
========================
Representasi objek bola dalam simulasi fisika.
"""

import tkinter as tk
import numpy as np
from collections import deque
from constants import (
    TRAIL_MAX_LENGTH, 
    TRAIL_POINT_MIN_SIZE, 
    TRAIL_POINT_MAX_SIZE,
    BALL_BORDER_WIDTH
)


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
        x_pixels : float
            Posisi awal sumbu X dalam piksel
        y_pixels : float
            Posisi awal sumbu Y dalam piksel
        radius_pixels : float
            Jari-jari bola dalam piksel
        color : str
            Warna bola (kode hex)
        mass : float
            Massa bola dalam kg
        velocity_x : float
            Kecepatan awal sumbu X dalam m/s
        velocity_y : float
            Kecepatan awal sumbu Y dalam m/s
        pixels_to_meters : float
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
        self.trail_points = deque(maxlen=TRAIL_MAX_LENGTH)
        self.trail_ids = []

        # Gambar bola di canvas
        self.canvas_id = canvas.create_oval(
            x_pixels - radius_pixels, 
            y_pixels - radius_pixels, 
            x_pixels + radius_pixels, 
            y_pixels + radius_pixels,
            fill=color, 
            outline="black", 
            width=BALL_BORDER_WIDTH
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
            size = TRAIL_POINT_MIN_SIZE + \
                   (index / TRAIL_MAX_LENGTH) * TRAIL_POINT_MAX_SIZE
            
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
