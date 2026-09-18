import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def draw_scavenger_hunt_pdf(filename="swfl-holiday-scavenger-hunt.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    page_w, page_h = letter # 612 x 792

    # Background border
    margin = 28
    c.setStrokeColor(colors.HexColor('#0f766e')) # Deep teal/evergreen
    c.setLineWidth(3)
    c.roundRect(margin, margin, page_w - 2 * margin, page_h - 2 * margin, 12, stroke=1, fill=0)

    # Inner decorative thin border
    c.setStrokeColor(colors.HexColor('#f59e0b')) # Holiday gold
    c.setLineWidth(1)
    c.roundRect(margin + 4, margin + 4, page_w - 2 * (margin + 4), page_h - 2 * (margin + 4), 10, stroke=1, fill=0)

    # HEADER BANNER
    header_y = page_h - margin - 68
    c.setFillColor(colors.HexColor('#064e3b')) # Dark holiday green
    c.roundRect(margin + 8, header_y, page_w - 2 * (margin + 8), 58, 8, stroke=0, fill=1)

    # Header Accent Line
    c.setFillColor(colors.HexColor('#dc2626')) # Holiday red
    c.rect(margin + 8, header_y, page_w - 2 * (margin + 8), 4, stroke=0, fill=1)

    # Title text
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(page_w / 2, header_y + 36, "SOUTHWEST FLORIDA HOLIDAY LIGHT TOUR")
    
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#fef08a')) # Warm soft gold
    c.drawCentredString(page_w / 2, header_y + 20, "KIDS' BACKSEAT SCAVENGER HUNT & BINGO")

    c.setFont("Helvetica", 8.5)
    c.setFillColor(colors.HexColor('#a7f3d0')) # Mint white
    c.drawCentredString(page_w / 2, header_y + 8, "Punta Gorda  *  Port Charlotte  *  North Port  *  Venice  *  Sarasota  *  Bradenton")

    # NAME / DATE ROW
    info_y = header_y - 24
    c.setFillColor(colors.HexColor('#1e293b'))
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(margin + 12, info_y, "Family / Explorer Name: ___________________________")
    c.drawString(margin + 265, info_y, "Date: ____________")
    c.drawString(margin + 370, info_y, "City / Trail: __________________")

    # INSTRUCTIONS BOX
    inst_y = info_y - 20
    c.setFillColor(colors.HexColor('#f0fdf4')) # Soft mint tint
    c.setStrokeColor(colors.HexColor('#86efac'))
    c.setLineWidth(0.8)
    c.roundRect(margin + 10, inst_y - 4, page_w - 2 * (margin + 10), 18, 4, stroke=1, fill=1)

    c.setFillColor(colors.HexColor('#14532d'))
    c.setFont("Helvetica-Bold", 8)
    instructions = "INSTRUCTIONS: Spot each holiday surprise out your car window! Mark the box with an X. Get 4 in a row or find all 16!"
    c.drawCentredString(page_w / 2, inst_y + 2, instructions)

    # 4x4 GRID ITEMS
    items = [
        ("Car Radio Sync", "Tuned to FM station playing holiday songs", "#1"),
        ("Florida Flamingo", "Pink flamingo wearing a Santa hat or scarf", "#2"),
        ("Giant Inflatable", "Blow-up character taller than mom or dad!", "#3"),
        ("Real Snow Machine", "Faux flurry bubbles blowing across yard", "#4"),
        ("Animated Pixel Tree", "Light tree with dancing computer patterns", "#5"),
        ("Rooftop Reindeer", "Prancing reindeer glowing atop shingles", "#6"),
        ("Candy Cane Lane", "Row of glowing candy canes lining driveway", "#7"),
        ("Lighted Boat / Anchor", "Nautical or boat display with twinkle lights", "#8"),
        ("Singing Characters", "Animated trees or bulbs with moving mouths", "#9"),
        ("Nativity Manger", "Glowing manger scene or holy family display", "#10"),
        ("Sneaky Grinch", "Green holiday grinch sneaking with a gift", "#11"),
        ("Walk-Through Arch", "Lighted tunnel or walk-under glowing arch", "#12"),
        ("Holiday Train Express", "Illuminated train engine puffing lights", "#13"),
        ("Nutcracker Guard", "Tall wooden soldier guarding the front walkway", "#14"),
        ("Laser Snowflake Stars", "Twinkling lasers dancing on home wall", "#15"),
        ("Santa & Sleigh", "Saint Nick with glowing reindeer in yard", "#16")
    ]

    grid_top = inst_y - 12
    cols = 4
    rows = 4
    gap_x = 8
    gap_y = 7
    total_grid_w = page_w - 2 * (margin + 10)
    card_w = (total_grid_w - (cols - 1) * gap_x) / cols
    card_h = 92

    for index, (title, hint, num) in enumerate(items):
        r = index // cols
        col = index % cols

        x = margin + 10 + col * (card_w + gap_x)
        y = grid_top - (r + 1) * card_h - r * gap_y

        # Card Background
        # Alternating subtle festive colors
        card_colors = ['#f8fafc', '#fef2f2', '#f0fdf4', '#eff6ff']
        bg_color = card_colors[(r + col) % 4]
        c.setFillColor(colors.HexColor(bg_color))
        c.setStrokeColor(colors.HexColor('#cbd5e1'))
        c.setLineWidth(1)
        c.roundRect(x, y, card_w, card_h, 6, stroke=1, fill=1)

        # Card Header Tab
        c.setFillColor(colors.HexColor('#0f766e') if (r % 2 == 0) else colors.HexColor('#b91c1c'))
        c.roundRect(x + 4, y + card_h - 18, 22, 14, 3, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(x + 15, y + card_h - 14, num)

        # Checkbox in top right
        box_size = 14
        box_x = x + card_w - box_size - 6
        box_y = y + card_h - box_size - 4
        c.setStrokeColor(colors.HexColor('#059669'))
        c.setLineWidth(1.5)
        c.setFillColor(colors.white)
        c.roundRect(box_x, box_y, box_size, box_size, 3, stroke=1, fill=1)

        # Item Title
        c.setFillColor(colors.HexColor('#0f172a'))
        c.setFont("Helvetica-Bold", 8.8)
        c.drawString(x + 6, y + card_h - 32, title)

        # Subtle decorative separator line
        c.setStrokeColor(colors.HexColor('#e2e8f0'))
        c.setLineWidth(0.6)
        c.line(x + 6, y + card_h - 36, x + card_w - 6, y + card_h - 36)

        # Hint / Description text (wrapped manually)
        c.setFillColor(colors.HexColor('#475569'))
        c.setFont("Helvetica", 7.5)
        
        # Word wrap hint into 2 lines
        words = hint.split(' ')
        line1 = []
        line2 = []
        curr = line1
        for w in words:
            if len(' '.join(curr + [w])) < 24 and curr is line1:
                curr.append(w)
            else:
                curr = line2
                curr.append(w)

        c.drawString(x + 6, y + card_h - 48, ' '.join(line1))
        if line2:
            c.drawString(x + 6, y + card_h - 59, ' '.join(line2))

        # Bottom "Points / Star" note
        c.setFillColor(colors.HexColor('#94a3b8'))
        c.setFont("Helvetica-Bold", 6.8)
        c.drawString(x + 6, y + 8, "[  ] FOUND IT!")

    # BOTTOM SECTION: BONUS CHALLENGES & CERTIFICATE
    bottom_y = margin + 10
    bottom_h = 82
    bottom_w = page_w - 2 * (margin + 10)
    
    c.setFillColor(colors.HexColor('#f8fafc'))
    c.setStrokeColor(colors.HexColor('#cbd5e1'))
    c.setLineWidth(1)
    c.roundRect(margin + 10, bottom_y, bottom_w, bottom_h, 8, stroke=1, fill=1)

    # Left: Bonus questions
    c.setFillColor(colors.HexColor('#b91c1c'))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin + 20, bottom_y + bottom_h - 16, "* BONUS BACKSEAT CHALLENGES:")

    c.setFillColor(colors.HexColor('#1e293b'))
    c.setFont("Helvetica", 8)
    c.drawString(margin + 20, bottom_y + bottom_h - 32, "1. Most inflatables spotted in one yard:  [ _______ ]  (Which house was it?)")
    c.drawString(margin + 20, bottom_y + bottom_h - 48, "2. Best holiday song heard in the car:  _________________________________________")
    c.drawString(margin + 20, bottom_y + bottom_h - 64, "3. Favorite light display of the night:  __________________________________________")

    # Right: Official Seal / Badge
    seal_x = page_w - margin - 140
    c.setFillColor(colors.HexColor('#fef3c7'))
    c.setStrokeColor(colors.HexColor('#f59e0b'))
    c.setLineWidth(1.5)
    c.roundRect(seal_x, bottom_y + 8, 125, bottom_h - 16, 6, stroke=1, fill=1)

    c.setFillColor(colors.HexColor('#92400e'))
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(seal_x + 62.5, bottom_y + bottom_h - 22, "OFFICIAL CERTIFICATE")

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor('#065f46'))
    c.drawCentredString(seal_x + 62.5, bottom_y + bottom_h - 36, "LIGHT TOUR PRO")

    c.setFont("Helvetica", 6.8)
    c.setFillColor(colors.HexColor('#78350f'))
    c.drawCentredString(seal_x + 62.5, bottom_y + bottom_h - 48, "SWFL Holiday Season 2026")

    c.setStrokeColor(colors.HexColor('#d97706'))
    c.setLineWidth(0.5)
    c.line(seal_x + 10, bottom_y + 20, seal_x + 115, bottom_y + 20)
    c.setFont("Helvetica", 6)
    c.drawCentredString(seal_x + 62.5, bottom_y + 12, "Navigator / Parent Signature")

    # Footer attribution (safe margin for home inkjets)
    c.setFillColor(colors.HexColor('#64748b'))
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(page_w / 2, 16, "Free Printable from Southwest Florida Holiday & Festivities Planner  *  Print & Share with Friends!")

    c.showPage()
    c.save()
    print(f"Generated {filename} successfully ({os.path.getsize(filename)} bytes)")

if __name__ == "__main__":
    draw_scavenger_hunt_pdf()
