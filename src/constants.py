"""
KONSTANTA SIMULASI
==================
Konstanta fisika dan visual untuk simulasi tumbukan.
"""

# ===== KONSTANTA FISIKA =====
PIXELS_TO_METERS = 0.01  # 1 px = 0.01 m
TIME_STEP = 0.02  # 20 ms per frame
COLLISION_DURATION = 0.05  # Asumsi durasi tumbukan (s)

# ===== KONSTANTA VISUAL BOLA =====
BALL_RADIUS_PIXELS = 20
BALL_1_COLOR = "#e63946"  # Merah
BALL_2_COLOR = "#457b9d"  # Biru
CENTER_OF_MASS_COLOR = "#2a9d8f"  # Hijau tosca

# ===== KONSTANTA CANVAS =====
CANVAS_BG_COLOR = "#f5f5f5"
GRID_COLOR = "#e0e0e0"
GRID_STEP_PIXELS = 50

# ===== KONSTANTA TRAIL (JEJAK BOLA) =====
TRAIL_MAX_LENGTH = 30
TRAIL_POINT_MIN_SIZE = 2
TRAIL_POINT_MAX_SIZE = 5
BALL_BORDER_WIDTH = 2
