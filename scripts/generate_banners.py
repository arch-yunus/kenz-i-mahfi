"""
Kenz-i Mahfî Banner Generator
Generates 3 cinematic, ultra-high-resolution 1920x1080 banners with sacred geometry,
cosmic nebulae, quantum wave patterns, and illuminated manuscript styling.
"""

import math
import random
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 1920, 1080

def create_noise_nebula(w, h, base_color, glow_color, scale=120, seed=42):
    np.random.seed(seed)
    # Generate low-res random field
    rw, rh = w // scale, h // scale
    grid = np.random.rand(rh, rw)
    img_noise = Image.fromarray((grid * 255).astype(np.uint8), mode='L')
    img_noise = img_noise.resize((w, h), Image.Resampling.BICUBIC)
    img_noise = img_noise.filter(ImageFilter.GaussianBlur(radius=scale//1.5))
    
    noise_arr = np.array(img_noise).astype(np.float32) / 255.0
    
    # 2nd octave
    rw2, rh2 = w // (scale // 2), h // (scale // 2)
    grid2 = np.random.rand(rh2, rw2)
    img_noise2 = Image.fromarray((grid2 * 255).astype(np.uint8), mode='L')
    img_noise2 = img_noise2.resize((w, h), Image.Resampling.BICUBIC)
    img_noise2 = img_noise2.filter(ImageFilter.GaussianBlur(radius=scale//3))
    noise_arr2 = np.array(img_noise2).astype(np.float32) / 255.0
    
    combined = (noise_arr * 0.6 + noise_arr2 * 0.4)
    combined = np.clip((combined - 0.3) * 1.8, 0, 1)
    
    # Colorize
    img_rgb = np.zeros((h, w, 3), dtype=np.uint8)
    for c in range(3):
        col_c = base_color[c] * (1 - combined) + glow_color[c] * combined
        img_rgb[:, :, c] = np.clip(col_c, 0, 255).astype(np.uint8)
        
    return Image.fromarray(img_rgb)

def add_stars(draw, w, h, count=300, seed=100):
    rng = random.Random(seed)
    for _ in range(count):
        x = rng.randint(0, w)
        y = rng.randint(0, h)
        brightness = rng.random()
        if brightness > 0.96:
            r = rng.randint(2, 4)
            draw.ellipse((x-r, y-r, x+r, y+r), fill=(255, 245, 220, 240))
            # Diffraction spikes
            spike_len = rng.randint(6, 16)
            draw.line((x-spike_len, y, x+spike_len, y), fill=(255, 240, 200, 160), width=1)
            draw.line((x, y-spike_len, x, y+spike_len), fill=(255, 240, 200, 160), width=1)
        elif brightness > 0.8:
            r = 1
            draw.ellipse((x-r, y-r, x+r, y+r), fill=(220, 230, 255, 180))
        else:
            draw.point((x, y), fill=(180, 200, 240, 120))

def draw_seljuk_star(draw, cx, cy, r_outer, r_inner, outline_color, fill_color=None, width=2):
    """Draws an 8-pointed Islamic/Seljuk star."""
    points = []
    for i in range(16):
        angle = i * math.pi / 8.0 - math.pi / 2.0
        r = r_outer if i % 2 == 0 else r_inner
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        points.append((px, py))
    if fill_color:
        draw.polygon(points, fill=fill_color)
    draw.polygon(points, outline=outline_color, width=width)

def draw_sacred_circles(draw, cx, cy, radii, color, width=1):
    for r in radii:
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=width)

def draw_golden_spiral(draw, cx, cy, a=4, b=0.18, max_t=5*math.pi, color=(212, 175, 55, 120), width=2):
    points = []
    for step in range(600):
        t = (step / 600) * max_t
        r = a * math.exp(b * t)
        x = cx + r * math.cos(t)
        y = cy + r * math.sin(t)
        points.append((x, y))
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=color, width=width)

def draw_quantum_grid(draw, cx, cy, size=400, color=(100, 200, 255, 40)):
    # Perspective wave mesh
    for y_idx in range(-15, 16):
        y_pos = cy + y_idx * 16
        pts = []
        for x_idx in range(-30, 31):
            x_pos = cx + x_idx * 24
            dist = math.hypot(x_pos - cx, y_pos - cy)
            wave = 20 * math.sin(dist * 0.035) * math.exp(-dist * 0.003)
            pts.append((x_pos, y_pos + wave))
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=color, width=1)

def draw_ornate_border(draw, w, h, gold_color=(212, 175, 55, 200), margin=36):
    # Double rectangle
    draw.rectangle((margin, margin, w - margin, h - margin), outline=gold_color, width=2)
    draw.rectangle((margin + 12, margin + 12, w - margin - 12, h - margin - 12), outline=(gold_color[0], gold_color[1], gold_color[2], 100), width=1)
    
    # Corner ornaments
    corner_size = 40
    corners = [
        (margin, margin),
        (w - margin, margin),
        (margin, h - margin),
        (w - margin, h - margin)
    ]
    for cx, cy in corners:
        draw_seljuk_star(draw, cx, cy, 18, 9, gold_color, fill_color=(20, 15, 30, 240), width=1)

def apply_vignette(img, strength=0.7):
    w, h = img.size
    cx, cy = w / 2, h / 2
    max_dist = math.hypot(cx, cy)
    
    x = np.linspace(-cx, cx, w)
    y = np.linspace(-cy, cy, h)
    xx, yy = np.meshgrid(x, y)
    dist = np.sqrt(xx**2 + yy**2) / max_dist
    
    vignette = 1.0 - strength * (dist ** 2)
    vignette = np.clip(vignette, 0, 1)
    
    arr = np.array(img).astype(np.float32)
    for c in range(3):
        arr[:, :, c] *= vignette
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

def render_banner_text(draw, cx, cy_title, title, subtitle, category_badge, tag_arabic=""):
    try:
        font_badge = ImageFont.truetype("C:/Windows/Fonts/cambriab.ttf", 20)
        font_title = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 46)
        font_sub = ImageFont.truetype("C:/Windows/Fonts/palabi.ttf", 26)
        font_arabic = ImageFont.truetype("C:/Windows/Fonts/times.ttf", 34)
    except Exception:
        font_badge = font_title = font_sub = font_arabic = ImageFont.load_default()

    # Draw badge background
    badge_w, badge_h = 440, 36
    draw.rectangle(
        (cx - badge_w // 2, cy_title - 95, cx + badge_w // 2, cy_title - 60),
        fill=(15, 23, 42, 210),
        outline=(212, 175, 55, 180),
        width=1
    )
    # Badge text
    draw.text((cx, cy_title - 78), category_badge.upper(), font=font_badge, fill=(245, 208, 115), anchor="mm")

    # Arabic calligraphic subtitle if present
    if tag_arabic:
        draw.text((cx, cy_title - 25), tag_arabic, font=font_arabic, fill=(230, 210, 160, 230), anchor="mm")

    # Main title with subtle shadow
    draw.text((cx + 2, cy_title + 32), title, font=font_title, fill=(10, 10, 20, 220), anchor="mm")
    draw.text((cx, cy_title + 30), title, font=font_title, fill=(255, 245, 220), anchor="mm")

    # Subtitle
    draw.text((cx, cy_title + 80), subtitle, font=font_sub, fill=(200, 215, 235), anchor="mm")

    # Decorative bottom separator
    line_w = 260
    draw.line((cx - line_w, cy_title + 115, cx + line_w, cy_title + 115), fill=(212, 175, 55, 160), width=1)
    draw_seljuk_star(draw, cx, cy_title + 115, 8, 4, (245, 208, 115, 240), fill_color=(20, 15, 30, 255), width=1)


# ==========================================
# 1. BANNER: KUANTUM KOZMOLOJİSİ & KENZ-İ MAHFÎ
# ==========================================
def generate_quantum_cosmology_banner():
    print("Generating Banner 1: Quantum Cosmology & Kenz-i Mahfî...")
    base_color = np.array([4, 8, 24])       # Deep Midnight Quantum Navy
    glow_color = np.array([28, 72, 150])    # Electric Sapphire & Cyan glow
    
    bg = create_noise_nebula(W, H, base_color, glow_color, scale=150, seed=777)
    
    # Overlay draw in RGBA
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    
    add_stars(d, W, H, count=450, seed=888)
    
    # Center-left Quantum Vacuum / Cosmic Singularity
    q_cx, q_cy = W // 2, H // 2 - 40
    
    # Quantum grid ripples
    draw_quantum_grid(d, q_cx, q_cy, size=500, color=(56, 189, 248, 60))
    
    # Sacred Geometric Concentric Orbits
    draw_sacred_circles(d, q_cx, q_cy, [80, 140, 210, 290, 380, 480], color=(212, 175, 55, 60), width=1)
    draw_sacred_circles(d, q_cx, q_cy, [110, 250, 340, 430], color=(56, 189, 248, 45), width=1)
    
    # Golden logarithmic spiral of cosmic inflation
    draw_golden_spiral(d, q_cx, q_cy, a=3, b=0.15, max_t=4.5*math.pi, color=(245, 208, 115, 130), width=2)
    draw_golden_spiral(d, q_cx, q_cy, a=-3, b=0.15, max_t=4.5*math.pi, color=(56, 189, 248, 110), width=2)
    
    # Central Quantum Vacuum Spark / Ahadiyyet Singularity
    draw_seljuk_star(d, q_cx, q_cy, 64, 32, (255, 245, 200, 240), fill_color=(15, 23, 42, 220), width=2)
    draw_seljuk_star(d, q_cx, q_cy, 36, 18, (56, 189, 248, 255), fill_color=(245, 208, 115, 200), width=1)
    
    # Radiant glow at center
    for rad in range(12, 1, -2):
        d.ellipse((q_cx - rad, q_cy - rad, q_cx + rad, q_cy + rad), fill=(255, 255, 255, 240))
        
    # Borders
    draw_ornate_border(d, W, H, gold_color=(212, 175, 55, 180), margin=32)
    
    # Text Plate / Title Badge
    render_banner_text(
        d,
        cx=W // 2,
        cy_title=H - 210,
        title="Modern Bilim, Kuantum Kozmolojisi ve Varlık Fiziği",
        subtitle="Kuantum Vakumu • Sıfır Noktası Alanı • Holografik Evren & Nefes-i Rahmânî",
        category_badge="Kenz-i Mahfî & Çağdaş Fizik Paralellikleri",
        tag_arabic="كُنْتُ كَنْزاً مَخْفِيّاً ── فِيزْيَاءُ الْوُجُودِ وَالْكَوْنِ"
    )
    
    # Merge and apply vignette
    final_img = Image.alpha_composite(bg.convert("RGBA"), overlay)
    final_img = apply_vignette(final_img.convert("RGB"), strength=0.65)
    
    out_path = os.path.join(OUTPUT_DIR, "06_kuantum_kozmoloji_banner.jpg")
    final_img.save(out_path, quality=95)
    print(f"Saved: {out_path}")


# ==========================================
# 2. BANNER: İNSÂN-I KÂMİL & KOZMİK AYNA
# ==========================================
def generate_insan_kamil_banner():
    print("Generating Banner 2: İnsân-ı Kâmil & Kozmik Ayna...")
    base_color = np.array([8, 22, 18])       # Mystical Emerald Forest / Celâli Obsidian
    glow_color = np.array([20, 95, 75])      # Luminous Emerald & Gold
    
    bg = create_noise_nebula(W, H, base_color, glow_color, scale=160, seed=1234)
    
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    
    add_stars(d, W, H, count=400, seed=555)
    
    cx, cy = W // 2, H // 2 - 45
    
    # Cosmic Mirror Mandala Rays
    ray_count = 32
    for i in range(ray_count):
        angle = i * (2 * math.pi / ray_count)
        r_start = 130
        r_end = 460 + 60 * (i % 2)
        x1 = cx + r_start * math.cos(angle)
        y1 = cy + r_start * math.sin(angle)
        x2 = cx + r_end * math.cos(angle)
        y2 = cy + r_end * math.sin(angle)
        d.line((x1, y1, x2, y2), fill=(212, 175, 55, 60 if i % 2 == 0 else 30), width=1)
        
    # Concentric circles of 5 Divine Presences (Hazarât-ı Hams)
    presences_radii = [90, 160, 240, 330, 420]
    draw_sacred_circles(d, cx, cy, presences_radii, color=(212, 175, 55, 80), width=2)
    
    # 12-point and 8-point Seljuk Stars for Micro-Cosmos Mirror
    draw_seljuk_star(d, cx, cy, 140, 70, (245, 208, 115, 220), fill_color=(10, 30, 24, 200), width=2)
    draw_seljuk_star(d, cx, cy, 95, 50, (52, 211, 153, 220), fill_color=(4, 20, 15, 240), width=2)
    draw_seljuk_star(d, cx, cy, 50, 25, (255, 245, 200, 255), fill_color=(212, 175, 55, 230), width=1)
    
    # Center Mirror Spark
    for r in range(16, 2, -2):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 230))
        
    # Flanking dual celestial arches (Kâbe Kavseyn - Two Bows' Length)
    arch_r = 300
    d.arc((cx - arch_r - 80, cy - arch_r, cx + arch_r - 80, cy + arch_r), start=280, end=440, fill=(245, 208, 115, 140), width=2)
    d.arc((cx - arch_r + 80, cy - arch_r, cx + arch_r + 80, cy + arch_r), start=100, end=260, fill=(245, 208, 115, 140), width=2)
    
    draw_ornate_border(d, W, H, gold_color=(212, 175, 55, 190), margin=32)
    
    render_banner_text(
        d,
        cx=W // 2,
        cy_title=H - 210,
        title="İnsân-ı Kâmil, Âlem Aynası ve Merâtib-i Vücûd",
        subtitle="Hazarât-ı Hams • Hilâfet-i İlâhiyye • Kâbe Kavseyn & Ev Ednâ Makamı",
        category_badge="Mertebe-i Câmia & Kozmik Tezahür",
        tag_arabic="الْإِنْسَانُ الْكَامِلُ مِرْآةُ الْحَضَرَاتِ الْإِلَهِيَّةِ"
    )
    
    final_img = Image.alpha_composite(bg.convert("RGBA"), overlay)
    final_img = apply_vignette(final_img.convert("RGB"), strength=0.65)
    
    out_path = os.path.join(OUTPUT_DIR, "07_insan_kamil_banner.jpg")
    final_img.save(out_path, quality=95)
    print(f"Saved: {out_path}")


# ==========================================
# 3. BANNER: KÜLLİYAT DİZİNİ & METİNLER KÜTÜPHANESİ
# ==========================================
def generate_kulliyat_dizin_banner():
    print("Generating Banner 3: Külliyat Dizin & Tematik Kütüphane...")
    base_color = np.array([24, 10, 6])       # Imperial Ottoman Burgundy & Amber
    glow_color = np.array([120, 50, 20])     # Warm Antique Gold & Cinnabar glow
    
    bg = create_noise_nebula(W, H, base_color, glow_color, scale=140, seed=9999)
    
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    
    add_stars(d, W, H, count=380, seed=333)
    
    cx, cy = W // 2, H // 2 - 45
    
    # Geometric Knowledge Lattice / Multi-node Constellation
    node_coords = []
    num_nodes = 8
    radius_node = 260
    for i in range(num_nodes):
        angle = i * (2 * math.pi / num_nodes) - math.pi / 2
        nx = cx + radius_node * math.cos(angle)
        ny = cy + radius_node * math.sin(angle)
        node_coords.append((nx, ny))
        
    # Connect all nodes (complete knowledge graph)
    for i in range(len(node_coords)):
        for j in range(i + 1, len(node_coords)):
            d.line([node_coords[i], node_coords[j]], fill=(212, 175, 55, 45), width=1)
            
    # Draw node stars
    for nx, ny in node_coords:
        draw_seljuk_star(d, nx, ny, 24, 12, (245, 208, 115, 220), fill_color=(35, 15, 10, 240), width=1)
        d.ellipse((nx - 4, ny - 4, nx + 4, ny + 4), fill=(255, 240, 200, 255))
        
    # Central Grand Rosette / Sun of Wisdom (Şems-i Ma'rifet)
    draw_sacred_circles(d, cx, cy, [60, 110, 170, 360, 460], color=(212, 175, 55, 75), width=1)
    draw_seljuk_star(d, cx, cy, 125, 62, (245, 208, 115, 230), fill_color=(45, 18, 12, 220), width=2)
    draw_seljuk_star(d, cx, cy, 70, 35, (234, 179, 8, 255), fill_color=(212, 175, 55, 210), width=1)
    
    for r in range(14, 2, -2):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 240))
        
    draw_ornate_border(d, W, H, gold_color=(212, 175, 55, 190), margin=32)
    
    render_banner_text(
        d,
        cx=W // 2,
        cy_title=H - 210,
        title="Kenz-i Mahfî Külliyatı: Tematik Dizin ve Kütüphane",
        subtitle="33 Akademik Monografi • 4 Ana İlim Dalı • Birincil Metinler ve Mukayeseli Şerhler",
        category_badge="Akademik Külliyat Dizin Haritası",
        tag_arabic="فِهْرِسُ الْكُلِّيَّةِ وَمَفَاتِيحُ الْحِكْمَةِ الْعِرْفَانِيَّةِ"
    )
    
    final_img = Image.alpha_composite(bg.convert("RGBA"), overlay)
    final_img = apply_vignette(final_img.convert("RGB"), strength=0.65)
    
    out_path = os.path.join(OUTPUT_DIR, "08_kulliyat_dizin_banner.jpg")
    final_img.save(out_path, quality=95)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    generate_quantum_cosmology_banner()
    generate_insan_kamil_banner()
    generate_kulliyat_dizin_banner()
    print("All 3 banners successfully generated!")
