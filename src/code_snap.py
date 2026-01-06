# ball.py - Ball.__init__() (Baris 42-101)
class Ball:
    def __init__(self,canvas: tk.Canvas,x_pixels: float,  y_pixels: float, 
                 radius_pixels: float, color: str,mass: float,velocity_x: float, 
                 velocity_y: float,pixels_to_meters: float):
      
        self.canvas = canvas
        self.radius_pixels = radius_pixels
        self.radius_meters = radius_pixels * pixels_to_meters
        self.mass = float(mass)
        self.pixels_to_meters = pixels_to_meters
        self.color = color

        # Posisi dan kecepatan dalam satuan meter dan m/s
        self.position = np.array([x_pixels * pixels_to_meters,y_pixels * pixels_to_meters], dtype=float)
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