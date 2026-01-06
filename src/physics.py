"""
LOGIKA FISIKA TUMBUKAN
======================
Fungsi-fungsi untuk menghitung tumbukan dan fisika simulasi.
File ini menangani logika inti fisika termasuk deteksi tumbukan,
resolusi posisi, dan konservasi momentum.
"""

import numpy as np
from typing import Tuple, Dict, Any
from ball import Ball
from constants import TIME_STEP


def calculate_collision(ball_1: Ball, 
                        ball_2: Ball, 
                        restitution: float,
                        contact_tracker: Dict[str, Any]) -> Tuple[float, float]:
    """
    Deteksi dan tangani tumbukan antara dua bola.
    Menggunakan Hukum Kekekalan Momentum dan Koefisien Restitusi.
    """
    
    # 1. Menghitung jarak antara dua pusat massa (Euclidean Distance)
    # Rumus: dist = ||pos_1 - pos_2|| = sqrt((x1-x2)^2 + (y1-y2)^2)
    pos_diff = ball_1.position - ball_2.position
    dist = np.linalg.norm(pos_diff)
    
    # Jarak minimal agar bersentuhan: r1 + r2
    min_dist = ball_1.radius_meters + ball_2.radius_meters
    f_sample = 0.0
    finished_impulse = 0.0 

    if dist <= min_dist:
        # 2. Menentukan Normal Vektor (Unit Vector)
        # Vektor satuan yang menunjuk dari benda 2 ke benda 1
        # Rumus: n = (pos_1 - pos_2) / dist
        n = pos_diff / (dist + 1e-9)
        
        # 3. Menghitung Kecepatan Relatif
        # Kecepatan benda 1 dilihat dari benda 2
        # Rumus: v_rel = v_1 - v_2
        v_rel = ball_1.velocity - ball_2.velocity
        
        # 4. Proyeksi Kecepatan Relatif ke Normal Vektor (Dot Product)
        # Kita hanya peduli pada kecepatan sepanjang Garis Dampak (Line of Impact)
        # Rumus: v_norm = v_rel • n
        v_norm = np.dot(v_rel, n)

        # 5. Resolusi Overlap (Positional Correction)
        # Mencegah bola "tenggelam" satu sama lain (Interpenetration)
        # Rumus Overlap: delta = min_dist - dist
        overlap = max(0.0, min_dist - dist)
        if overlap > 0:
            total_m = ball_1.mass + ball_2.mass
            # Pergeseran posisi proposional terhadap massa (Inverse Mass weighting)
            # pos_1 += (overlap * (m2 / m_total)) * n
            # pos_2 -= (overlap * (m1 / m_total)) * n
            ball_1.position += (overlap * (ball_2.mass / total_m)) * n
            ball_2.position -= (overlap * (ball_1.mass / total_m)) * n

        # 6. Kalkulasi Impuls (Hanya jika benda saling mendekat: v_norm < 0)
        if v_norm < 0:
            # Menghitung Impuls Skalar (j)
            # Rumus turunan dari Kekekalan Momentum & Restitusi:
            # j = [-(1 + e) * v_norm] / [(1/m1) + (1/m2)]
            j = -(1 + restitution) * v_norm
            j /= (1.0 / ball_1.mass + 1.0 / ball_2.mass)
            
            # Mengubah Impuls Skalar menjadi Vektor sepanjang normal
            # Rumus Impuls Vektor (J): J = j * n
            impulse_vec = j * n

            # 7. Update Kecepatan Akhir (v')
            # Menerapkan perubahan momentum: delta_p = J
            # v_new = v_old ± (J / m)
            ball_1.velocity += impulse_vec / ball_1.mass
            ball_2.velocity -= impulse_vec / ball_2.mass

            # 8. Approximasi Gaya Rata-rata (Impulsive Force)
            # Gaya adalah laju perubahan momentum per satuan waktu
            # Rumus: F = Δp / Δt = |j| / TIME_STEP
            f_sample = abs(j) / max(TIME_STEP, 1e-9)

            # Update contact tracker untuk analisis grafik Gaya-Waktu
            if not contact_tracker["in_contact"]:
                contact_tracker["in_contact"] = True
                contact_tracker["impulse_accumulated"] = 0.0
            contact_tracker["impulse_accumulated"] += j
            contact_tracker["force_samples"].append(f_sample)
    else:
        # Finalisasi Impuls saat kontak berakhir (Luas di bawah kurva F-t)
        if contact_tracker["in_contact"]:
            finished_impulse = abs(contact_tracker["impulse_accumulated"])
            # Reset tracker
            contact_tracker["in_contact"] = False
            contact_tracker["impulse_accumulated"] = 0.0
            contact_tracker["force_samples"].clear()

    return f_sample, finished_impulse


def handle_wall_bounce(ball: Ball, 
                       canvas_width: int, 
                       canvas_height: int,
                       pixels_to_meters: float) -> None:
    """
    Tangani pantulan bola dengan dinding (Elastic Reflection).
    Membalikkan komponen kecepatan saat bola menyentuh batas layar.
    """
    # Konversi posisi piksel ke meter untuk pengecekan fisik
    px = ball.position[0] / pixels_to_meters
    py = ball.position[1] / pixels_to_meters
    
    # 1. Cek Dinding Kiri/Kanan (Sumbu X)
    # Jika posisi < radius (kiri) ATAU posisi > lebar - radius (kanan)
    if px - ball.radius_pixels < 0:
        # Clamping posisi agar tidak keluar layar
        ball.position[0] = ball.radius_pixels * pixels_to_meters
        # Refleksi Kecepatan X: v_x' = -v_x
        ball.velocity[0] *= -1
    elif px + ball.radius_pixels > canvas_width:
        ball.position[0] = (canvas_width - ball.radius_pixels) * pixels_to_meters
        ball.velocity[0] *= -1
    
    # 2. Cek Dinding Atas/Bawah (Sumbu Y)
    # Jika posisi < radius (atas) ATAU posisi > tinggi - radius (bawah)
    if py - ball.radius_pixels < 0:
        ball.position[1] = ball.radius_pixels * pixels_to_meters
        # Refleksi Kecepatan Y: v_y' = -v_y
        ball.velocity[1] *= -1
    elif py + ball.radius_pixels > canvas_height:
        ball.position[1] = (canvas_height - ball.radius_pixels) * pixels_to_meters
        ball.velocity[1] *= -1


def calculate_center_of_mass(ball_1: Ball, 
                              ball_2: Ball) -> Tuple[float, float]:
    """
    Menghitung posisi pusat massa sistem dua bola.
    Digunakan untuk visualisasi titik pusat massa (COM).
    
    Rumus Pusat Massa (R_com):
    R_com = (m1 * r1 + m2 * r2) / (m1 + m2)
    dimana r adalah vektor posisi.
    """
    total_mass = ball_1.mass + ball_2.mass
    
    # Perhitungan vektor rata-rata tertimbang massa
    com_position = (
        ball_1.position * ball_1.mass + 
        ball_2.position * ball_2.mass
    ) / total_mass
    
    return com_position[0], com_position[1]


def calculate_physics_data(ball_1: Ball, 
                           ball_2: Ball) -> Tuple[float, float]:
    """
    Menghitung data fisika sistem untuk validasi hukum kekekalan.
    
    Returns:
    --------
    Tuple[float, float]
        (momentum_total, kinetic_energy_total)
    """
    # 1. Total Momentum Sistem (Besaran Vektor)
    # P_tot_vec = p1 + p2 = m1*v1 + m2*v2
    p_vec = ball_1.mass * ball_1.velocity + ball_2.mass * ball_2.velocity
    
    # Magnitudo Momentum (Skalar) untuk plotting grafik
    # P_scalar = ||P_tot_vec||
    p_tot = np.linalg.norm(p_vec)
    
    # 2. Energi Kinetik Total Sistem (Besaran Skalar)
    # Rumus: EK = 1/2 * m * v^2
    # v^2 dihitung sebagai Dot Product vektor kecepatan (v • v)
    ke = (0.5 * ball_1.mass * np.dot(ball_1.velocity, ball_1.velocity) + 
          0.5 * ball_2.mass * np.dot(ball_2.velocity, ball_2.velocity))
    
    return p_tot, ke