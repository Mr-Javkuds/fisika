# HTML Content Generator for Python Learning Documentation
# This script helps build comprehensive sections programmatically

sections_content = """
<!-- Continuing from intro section... -->

    <!-- 1. TIPE DATA (DATA TYPES) SECTION -->
    <section id="data-types" class="py-20 px-6 bg-white dark:bg-gray-800">
        <div class="container mx-auto max-w-6xl">
            <div class="text-center mb-16">
                <span class="badge badge-purple mb-4">Python Fundamentals #1</span>
                <h2 class="text-4xl md:text-5xl font-bold mb-4 gradient-text">
                    <i class="fas fa-database mr-3"></i>Tipe Data Python
                </h2>
                <p class="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
                    Dari basic types hingga advanced collections - dengan contoh real dari momentum_2d.py
                </p>
            </div>

            <!-- Numeric Types -->
            <div class="mb-12">
                <h3 class="text-3xl font-bold mb-6 text-gray-900 dark:text-white">
                    <span class="text-4xl mr-3">🔢</span> Numeric Types
                </h3>
                
                <div class="grid md:grid-cols-3 gap-6">
                    <div class="bg-purple-50 dark:bg-purple-900/20 p-6 rounded-xl border-2 border-purple-200 dark:border-purple-700">
                        <h4 class="text-xl font-bold text-purple-600 dark:text-purple-300 mb-3">int - Integer</h4>
                        <p class="text-sm mb-4 text-gray-700 dark:text-gray-300">Bilangan bulat</p>
                        <div class="code-block">
                            <button class="copy-btn bg-purple-500 text-white px-3 py-1 rounded text-sm" onclick="copyCode(this)">
                                <i class="fas fa-copy mr-1"></i>Copy
                            </button>
                            <pre class="rounded-lg"><code class="language-python"># Line 222
BALL_RADIUS_PIXELS = 20

# Conversion
delay_ms = int(0.02 * 1000)  # 20</code></pre>
                        </div>
                    </div>

                    <div class="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-xl border-2 border-blue-200 dark:border-blue-700">
                        <h4 class="text-xl font-bold text-blue-600 dark:text-blue-300 mb-3">float - Desimal</h4>
                        <p class="text-sm mb-4 text-gray-700 dark:text-gray-300">Bilangan dengan koma</p>
                        <div class="code-block">
                            <button class="copy-btn bg-blue-500 text-white px-3 py-1 rounded text-sm" onclick="copyCode(this)">
                                <i class="fas fa-copy mr-1"></i>Copy
                            </button>
                            <pre class="rounded-lg"><code class="language-python"># Line 218-219
PIXELS_TO_METERS = 0.01
TIME_STEP = 0.02

mass = float("2.5")  # String to float</code></pre>
                        </div>
                    </div>

                    <div class="bg-green-50 dark:bg-green-900/20 p-6 rounded-xl border-2 border-green-200 dark:border-green-700">
                        <h4 class="text-xl font-bold text-green-600 dark:text-green-300 mb-3">Type Safety</h4>
                        <p class="text-sm mb-4 text-gray-700 dark:text-gray-300">Explicit conversion</p>
                        <div class="code-block">
                            <button class="copy-btn bg-green-500 text-white px-3 py-1 rounded text-sm" onclick="copyCode(this)">
                                <i class="fas fa-copy mr-1"></i>Copy
                            </button>
                            <pre class="rounded-lg"><code class="language-python"># Line 103
self.mass = float(mass)  # Ensure type

# Line 858
e = float(self.restitution_coefficient.get())</code></pre>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Strings -->
            <div class="mb-12">
                <h3 class="text-3xl font-bold mb-6 text-gray-900 dark:text-white">
                    <span class="text-4xl mr-3">📝</span> Strings (str)
                </h3>
                
                <div class="grid md:grid-cols-2 gap-6">
                    <div class="bg-white dark:bg-gray-700 p-6 rounded-xl shadow-lg">
                        <h4 class="text-xl font-bold mb-4">F-Strings (Modern)</h4>
                        <div class="code-block">
                            <button class="copy-btn bg-blue-500 text-white px-3 py-1 rounded text-sm" onclick="copyCode(this)">
                                <i class="fas fa-copy"></i>
                            </button>
                            <pre class="rounded-lg"><code class="language-python"># Line 909-912 - F-string formatting
txt = (
    f"t: {self.simulation_time:.2f}s | "
    f"P_tot: {self.momentum_log[-1]:.2f} kg·m/s"
)
# :.2f = 2 decimal places</code></pre>
                        </div>
                    </div>

                    <div class="bg-white dark:bg-gray-700 p-6 rounded-xl shadow-lg">
                        <h4 class="text-xl font-bold mb-4">String Literals</h4>
                        <div class="code-block">
                            <button class="copy-btn bg-blue-500 text-white px-3 py-1 rounded text-sm" onclick="copyCode(this)">
                                <i class="fas fa-copy"></i>
                            </button>
                            <pre class="rounded-lg"><code class="language-python"># Line 223-225
BALL_1_COLOR = "#e63946"  # Hex colors
BALL_2_COLOR = "#457b9d"

# Line 313 - Unicode emoji
text="⚙️ Parameter Fisika"</code></pre>
                        </div>
                    </div>
                </div>

                <div class="callout tip mt-6">
                    <h4 class="font-bold mb-2"><i class="fas fa-star text-yellow-500 mr-2"></i>Best Practice: Use F-Strings</h4>
                    <p class="text-sm">F-strings (Python 3.6+) are the best way to format strings. More readable than % or .format().</p>
                </div>
            </div>

            <!-- Boolean -->
            <div class="mb-12">
                <h3 class="text-3xl font-bold mb-6 text-gray-900 dark:text-white">
                    <span class="text-4xl mr-3">✓✗</span> Boolean (bool)
                </h3>
                
                <div class="bg-gradient-to-r from-green-50 to-teal-50 dark:from-green-900/20 dark:to-teal-900/20 p-8 rounded-2xl">
                    <div class="code-block">
                        <button class="copy-btn bg-green-500 text-white px-3 py-1 rounded text-sm" onclick="copyCode(this)">
                            <i class="fas fa-copy"></i>
                        </button>
                        <pre class="rounded-lg"><code class="language-python"># Line 247-249 - State flags
self.is_running = False
self.is_paused = False

# Line 263 - Dictionary with bool values
self.contact_tracker = {
    "in_contact": False,
    "impulse_accumulated": 0.0
}

# Usage in conditionals
if not self.is_running:  # Line 786
    return

# Boolean naming: use is_, has_, can_
is_valid = True
has_collision = False</code></pre>
                    </div>
                </div>
            </div>

            <!-- Collections -->
            <div class="mb-12">
                <h3 class="text-3xl font-bold mb-8 text-center text-gray-900 dark:text-white">
                    Python Collections
                </h3>

                <!-- Lists -->
                <div class="mb-8">
                    <h4 class="text-2xl font-bold mb-4 text-gray-900 dark:text-white flex items-center">
                        <span class="text-4xl mr-3">📋</span> Lists
                    </h4>
                    <div class="grid md:grid-cols-2 gap-6">
                        <div class="bg-white dark:bg-gray-700 p-6 rounded-xl shadow-lg">
                            <h5 class="font-bold text-lg mb-3 text-purple-600 dark:text-purple-400">Operations</h5>
                            <div class="code-block">
                                <button class="copy-btn bg-purple-500 text-white px-3 py-1 rounded text-sm" onclick="copyCode(this)">
                                    <i class="fas fa-copy"></i>
                                </button>
                                <pre class="rounded-lg"><code class="language-python"># Line 256-259 - Initialize
self.time_log = []
self.force_log = []

# Line 901 - Append
self.time_log.append(self.simulation_time)

# Line 909 - Access (negative index)
last_value = self.momentum_log[-1]

# Line 690 - Clear
self.time_log.clear()</code></pre>
                            </div>
                        </div>

                        <div class="bg-white dark:bg-gray-700 p-6 rounded-xl shadow-lg">
                            <h5 class="font-bold text-lg mb-3 text-purple-600 dark:text-purple-400">Iteration</h5>
                            <div class="code-block">
                                <button class="copy-btn bg-purple-500 text-white px-3 py-1 rounded text-sm" onclick="copyCode(this)">
                                    <i class="fas fa-copy"></i>
                                </button>
                                <pre class="rounded-lg"><code class="language-python"># Line 802 - Iterate over objects
for b in (self.ball_1, self.ball_2):
    # Process each ball

# Line 954 - Iterate with index
for i in range(len(self.time_log)):
    value = self.time_log[i]

# Line 385 - List literal
values = ["1D", "2D (semi)"]</code></pre>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Dictionaries -->
                <div class="mb-8">
                    <h4 class="text-2xl font-bold mb-4 text-gray-900 dark:text-white flex items-center">
                        <span class="text-4xl mr-3">📚</span> Dictionaries
                    </h4>
                    <div class="bg-white dark:bg-gray-700 p-6 rounded-xl shadow-lg">
                        <div class="code-block">
                            <button class="copy-btn bg-blue-500 text-white px-3 py-1 rounded text-sm" onclick="copyCode(this)">
                                <i class="fas fa-copy"></i>
                            </button>
                            <pre class="rounded-lg"><code class="language-python"># Line 262-266 - Dict for state tracking
self.contact_tracker = {
    "in_contact": False,
    "impulse_accumulated": 0.0,
    "force_samples": []
}

# Access values
ct = self.contact_tracker
if ct["in_contact"]:  # Line 873
    ct["impulse_accumulated"] += j

# Clear list in dict
ct["force_samples"].clear()  # Line 888</code></pre>
                        </div>
                        <div class="callout info mt-4">
                            <p class="text-sm"><strong>Dict Pattern:</strong> Gunakan dict untuk group related state variables dengan named keys (lebih readable dari tuple).</p>
                        </div>
                    </div>
                </div>

                <!-- Deque -->
                <div class="mb-8">
                   <h4 class="text-2xl font-bold mb-4 text-gray-900 dark:text-white flex items-center">
                        <span class="text-4xl mr-3">🔄</span> Deque (collections.deque)
                    </h4>
                    <div class="bg-white dark:bg-gray-700 p-6 rounded-xl shadow-lg">
                        <div class="code-block">
                            <button class="copy-btn bg-green-500 text-white px-3 py-1 rounded text-sm" onclick="copyCode(this)">
                                <i class="fas fa-copy"></i>
                            </button>
                            <pre class="rounded-lg"><code class="language-python"># Line 20 - Import
from collections import deque

# Line 113 - Create with max length
self.trail_points = deque(maxlen=30)

# Line 181 - Auto-evict oldest when full
self.trail_points.append((px, py))
# When length > 30, oldest is removed automatically

# Line 135 - Iterate
for index, (trail_x, trail_y) in enumerate(self.trail_points):
    # Draw trail point</code></pre>
                        </div>
                        <div class="highlight-box mt-4">
                            <h5 class="font-bold mb-2"><i class="fas fa-bolt text-yellow-500 mr-2"></i>Why Deque?</h5>
                            <p class="text-sm">Deque dengan <code>maxlen</code> is PERFECT for fixed-size buffers (trails, moving averages). Auto-eviction = no manual size management!</p>
                        </div>
                    </div>
                </div>

                <!-- NumPy Arrays -->
                <div class="mb-8">
                    <h4 class="text-2xl font-bold mb-4 text-gray-900 dark:text-white flex items-center">
                        <span class="text-4xl mr-3">🔢</span> NumPy Arrays
                    </h4>
                    <div class="bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20 p-6 rounded-xl border-2 border-indigo-300 dark:border-indigo-700">
                        <div class="code-block mb-4">
                            <button class="copy-btn bg-indigo-500 text-white px-3 py-1 rounded text-sm" onclick="copyCode(this)">
                                <i class="fas fa-copy"></i>
                            </button>
                            <pre class="rounded-lg"><code class="language-python"># Line 108-110 - Create array
self.position = np.array(
    [x_pixels * pixels_to_meters, y_pixels * pixels_to_meters],
    dtype=float
)
self.velocity = np.array([velocity_x, velocity_y], dtype=float)

# Line 174 - Vector arithmetic (MAGIC!)
self.position += self.velocity * time_step
# Applies to EACH element: pos[0] += vel[0]*dt, pos[1] += vel[1]*dt

# Line 838 - Vector operations
dist = np.linalg.norm(pos_diff)  # Euclidean distance
v_norm = np.dot(v_rel, n)  # Dot product

# Line 896 - Magnitude squared (efficient)
speed_squared = np.dot(velocity, velocity)</code></pre>
                        </div>

                        <div class="grid md:grid-cols-2 gap-4">
                            <div class="comparison-box bad">
                                <p class="font-bold text-red-600 mb-2">❌ Without NumPy (Slow)</p>
                                <code class="text-xs">pos_x += vel_x * dt<br>pos_y += vel_y * dt<br>dist = sqrt(dx**2 + dy**2)</code>
                            </div>
                            <div class="comparison-box good">
                                <p class="font-bold text-green-600 mb-2">✅ With NumPy (Fast)</p>
                                <code class="text-xs">pos += vel * dt<br>dist = np.linalg.norm(diff)</code>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

"""

# Save this content for building complete HTML
print("Section content template ready for integration")
print(f"Content length: {len(sections_content)} characters")
