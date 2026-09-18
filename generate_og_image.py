import os
from PIL import Image, ImageDraw, ImageFont

def create_og_image(output_path="og-preview.png"):
    width, height = 1200, 630
    img = Image.new("RGBA", (width, height), (10, 22, 40, 255)) # Deep navy/twilight
    draw = ImageDraw.Draw(img)

    # Vertical rich gradient from deep twilight to dark emerald
    for y in range(height):
        ratio = y / height
        r = int(12 * (1 - ratio) + 6 * ratio)
        g = int(24 * (1 - ratio) + 68 * ratio)
        b = int(48 * (1 - ratio) + 52 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # Soft ambient glow lights along edges/corners only (not behind text)
    bokeh_lights = [
        (90, 90, 70, (245, 158, 11, 28)),
        (1110, 90, 80, (16, 185, 129, 25)),
        (1120, 530, 90, (239, 68, 68, 25)),
        (80, 540, 85, (56, 189, 248, 25)),
        (70, 315, 60, (254, 240, 138, 25)),
        (1130, 315, 65, (254, 240, 138, 25)),
    ]
    for bx, by, br, bcol in bokeh_lights:
        draw.ellipse([bx - br, by - br, bx + br, by + br], fill=bcol)

    # Outer decorative gold & emerald frames
    margin = 24
    draw.rounded_rectangle(
        [margin, margin, width - margin, height - margin],
        radius=20,
        outline=(245, 158, 11, 220), # Holiday Gold
        width=3
    )
    draw.rounded_rectangle(
        [margin + 6, margin + 6, width - margin - 6, height - margin - 6],
        radius=16,
        outline=(16, 185, 129, 140), # Emerald
        width=1
    )

    # Load Windows standard fonts
    font_bold_path = "C:\\Windows\\Fonts\\segoeuib.ttf"
    font_reg_path = "C:\\Windows\\Fonts\\segoeui.ttf"
    if not os.path.exists(font_bold_path):
        font_bold_path = "C:\\Windows\\Fonts\\arialbd.ttf"
        font_reg_path = "C:\\Windows\\Fonts\\arial.ttf"

    font_badge = ImageFont.truetype(font_bold_path, 18)
    font_title = ImageFont.truetype(font_bold_path, 52)
    font_sub = ImageFont.truetype(font_bold_path, 24)
    font_pill = ImageFont.truetype(font_bold_path, 20)
    font_footer = ImageFont.truetype(font_reg_path, 19)

    # 1. Top Badge Pill
    badge_text = "2026 OFFICIAL SOUTHWEST FLORIDA HOLIDAY DIRECTORY"
    badge_bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
    badge_w = badge_bbox[2] - badge_bbox[0]
    badge_x = (width - badge_w) // 2
    badge_y = 60

    draw.rounded_rectangle(
        [badge_x - 22, badge_y - 7, badge_x + badge_w + 22, badge_y + 30],
        radius=14,
        fill=(6, 78, 59, 140),
        outline=(52, 211, 153, 220),
        width=2
    )
    draw.text((badge_x, badge_y), badge_text, fill=(167, 243, 208, 255), font=font_badge)

    # 2. Main Title Lines
    title1 = "SWFL Holiday Lights &"
    title2 = "Festivities Guide"
    
    t1_bbox = draw.textbbox((0, 0), title1, font=font_title)
    t1_w = t1_bbox[2] - t1_bbox[0]
    draw.text(((width - t1_w) // 2, 120), title1, fill=(255, 255, 255, 255), font=font_title)

    t2_bbox = draw.textbbox((0, 0), title2, font=font_title)
    t2_w = t2_bbox[2] - t2_bbox[0]
    draw.text(((width - t2_w) // 2, 188), title2, fill=(254, 240, 138, 255), font=font_title)

    # 3. Subtitle / Covered Towns
    sub_text = "Punta Gorda  |  Port Charlotte  |  North Port  |  Venice  |  Sarasota  |  Bradenton"
    s_bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
    s_w = s_bbox[2] - s_bbox[0]
    draw.text(((width - s_w) // 2, 268), sub_text, fill=(148, 163, 184, 255), font=font_sub)

    # 4. Gold Divider Line
    div_w = 420
    div_x = (width - div_w) // 2
    div_y = 318
    draw.line([(div_x, div_y), (div_x + div_w, div_y)], fill=(245, 158, 11, 220), width=2)

    # 5. Feature Highlights (4 Clean Grid Cards)
    pills = [
        ("40+ Verified Displays & Festivals", (6, 78, 59, 180), (16, 185, 129, 220), (110, 231, 183, 255)),
        ("1-Click Multi-Stop Google Maps Route", (30, 58, 138, 180), (56, 189, 248, 220), (186, 230, 253, 255)),
        ("FM-Radio Musical Light Shows", (136, 19, 55, 180), (251, 113, 133, 220), (254, 205, 211, 255)),
        ("Kids' Backseat Scavenger Hunt (PDF)", (120, 53, 15, 180), (251, 191, 36, 220), (254, 240, 138, 255))
    ]

    pill_y1 = 345
    pill_y2 = 420
    card_w = 510
    card_h = 56
    col1_x = 75
    col2_x = 615

    coords = [
        (col1_x, pill_y1),
        (col2_x, pill_y1),
        (col1_x, pill_y2),
        (col2_x, pill_y2)
    ]

    for (p_text, p_bg, p_border, p_color), (px, py) in zip(pills, coords):
        draw.rounded_rectangle(
            [px, py, px + card_w, py + card_h],
            radius=12,
            fill=p_bg,
            outline=p_border,
            width=2
        )
        pb = draw.textbbox((0, 0), p_text, font=font_pill)
        pw = pb[2] - pb[0]
        draw.text((px + (card_w - pw) // 2, py + 15), p_text, fill=p_color, font=font_pill)

    # 6. Bottom Tagline Bar
    footer_text = "Interactive GPS Maps  •  Real-Time Distance Radar  •  Free Community Planner"
    fb = draw.textbbox((0, 0), footer_text, font=font_footer)
    fw = fb[2] - fb[0]
    draw.text(((width - fw) // 2, 530), footer_text, fill=(148, 163, 184, 240), font=font_footer)

    # Save as PNG
    img.save(output_path, "PNG")
    print(f"Updated {output_path} successfully ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    create_og_image()
