"""
MAIN ENTRY POINT
================
Entry point untuk menjalankan aplikasi simulasi tumbukan.
"""

import tkinter as tk
from app import CollisionSimulatorApp


def main():
    """Fungsi utama untuk menjalankan aplikasi."""
    root = tk.Tk()
    app = CollisionSimulatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
