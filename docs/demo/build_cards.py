"""Generate title + outro PNG cards for the demo video."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1387, 868
BG = (28, 25, 23)        # stone-900
AMBER = (251, 191, 36)   # amber-400
WHITE = (250, 250, 249)  # stone-50
GREY = (120, 113, 108)   # stone-500
INDIGO = (129, 140, 248) # indigo-400
EMERALD = (52, 211, 153) # emerald-400

SFNS = "/System/Library/Fonts/SFNS.ttf"
MONO = "/System/Library/Fonts/SFNSMono.ttf"


def make_title(path: str) -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # Subtle border
    d.rectangle([0, H - 6, W, H], fill=AMBER)
    # W mark
    w_x, w_y = W // 2 - 40, 220
    d.rectangle([w_x, w_y, w_x + 80, w_y + 80], fill=AMBER)
    f_w = ImageFont.truetype(SFNS, 60)
    bbox = d.textbbox((0, 0), "W", font=f_w)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    d.text((w_x + 40 - text_w / 2 - bbox[0], w_y + 40 - text_h / 2 - bbox[1]),
           "W", fill=BG, font=f_w)
    # Title
    f_title = ImageFont.truetype(SFNS, 84)
    title = "KAJOTA WITNESS"
    bbox = d.textbbox((0, 0), title, font=f_title)
    d.text(((W - (bbox[2] - bbox[0])) / 2 - bbox[0], 360),
           title, fill=AMBER, font=f_title)
    # Tagline
    f_sub = ImageFont.truetype(SFNS, 32)
    sub = "encrypted seller memory + AI jury on 0G Galileo"
    bbox = d.textbbox((0, 0), sub, font=f_sub)
    d.text(((W - (bbox[2] - bbox[0])) / 2 - bbox[0], 480),
           sub, fill=WHITE, font=f_sub)
    # Event
    f_evt = ImageFont.truetype(SFNS, 24)
    evt = "0G Zero Cup 2026  ·  Round 1"
    bbox = d.textbbox((0, 0), evt, font=f_evt)
    d.text(((W - (bbox[2] - bbox[0])) / 2 - bbox[0], 540),
           evt, fill=GREY, font=f_evt)
    img.save(path)


def make_outro(path: str) -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 6], fill=AMBER)
    # Heading
    f_h = ImageFont.truetype(SFNS, 56)
    heading = "Three real 0G surfaces"
    bbox = d.textbbox((0, 0), heading, font=f_h)
    d.text(((W - (bbox[2] - bbox[0])) / 2 - bbox[0], 130),
           heading, fill=AMBER, font=f_h)
    # Subhead
    f_sh = ImageFont.truetype(SFNS, 28)
    sh = "each doing work the app cannot run without"
    bbox = d.textbbox((0, 0), sh, font=f_sh)
    d.text(((W - (bbox[2] - bbox[0])) / 2 - bbox[0], 215),
           sh, fill=GREY, font=f_sh)

    # Three pillars
    pillars = [
        ("0G Storage", "encrypted chat + verdict blobs", EMERALD),
        ("0G Chain (txs)", "settles every upload, issues every CID", AMBER),
        ("WitnessAnchor", "public commitment - matchesStorageCid", INDIGO),
    ]
    col_w = W // 3
    pill_y = 320
    f_pt = ImageFont.truetype(SFNS, 34)
    f_pd = ImageFont.truetype(SFNS, 20)
    for i, (title, desc, color) in enumerate(pillars):
        cx = col_w * i + col_w // 2
        # vertical color bar
        d.rectangle([cx - 80, pill_y, cx - 76, pill_y + 100], fill=color)
        # title
        bbox = d.textbbox((0, 0), title, font=f_pt)
        d.text((cx - 60, pill_y + 10), title, fill=color, font=f_pt)
        # desc (split into 2 lines if needed)
        words = desc.split()
        line1, line2 = "", ""
        for w in words:
            if d.textbbox((0, 0), line1 + " " + w if line1 else w, font=f_pd)[2] < 320:
                line1 = (line1 + " " + w).strip()
            else:
                line2 = (line2 + " " + w).strip()
        d.text((cx - 60, pill_y + 55), line1, fill=WHITE, font=f_pd)
        if line2:
            d.text((cx - 60, pill_y + 80), line2, fill=WHITE, font=f_pd)

    # Footer URLs (monospace for credibility)
    f_url = ImageFont.truetype(MONO, 22)
    f_label = ImageFont.truetype(SFNS, 18)
    footer_y = 600
    urls = [
        ("Repo:", "github.com/KaJota-inc/kajota-witness"),
        ("Live:", "kajota-witness.onrender.com"),
        ("Anchor:", "0x2f1D3a881cfbeA01Cf55f3cAd125aA32Bf8cEC94"),
    ]
    for label, url in urls:
        bbox_l = d.textbbox((0, 0), label, font=f_label)
        bbox_u = d.textbbox((0, 0), url, font=f_url)
        total = (bbox_l[2] - bbox_l[0]) + 12 + (bbox_u[2] - bbox_u[0])
        x = (W - total) // 2
        d.text((x, footer_y), label, fill=GREY, font=f_label)
        d.text((x + bbox_l[2] - bbox_l[0] + 12, footer_y - 2),
               url, fill=AMBER, font=f_url)
        footer_y += 38
    img.save(path)


def make_step_divider(path: str, step_num: int, step_total: int,
                      title: str, sub: str, color) -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 6], fill=color)
    # Step counter at top
    f_count = ImageFont.truetype(SFNS, 22)
    counter = f"STEP {step_num} / {step_total}"
    d.text((48, 36), counter, fill=GREY, font=f_count)
    # Big step number on the left
    f_num = ImageFont.truetype(SFNS, 280)
    num_str = str(step_num)
    bbox = d.textbbox((0, 0), num_str, font=f_num)
    num_w = bbox[2] - bbox[0]
    d.text((180, 280), num_str, fill=color, font=f_num)
    # Title to the right of the number
    f_t = ImageFont.truetype(SFNS, 64)
    title_x = 180 + num_w + 60
    d.text((title_x, 340), title, fill=WHITE, font=f_t)
    # Subtitle below title
    f_s = ImageFont.truetype(SFNS, 28)
    d.text((title_x + 4, 440), sub, fill=GREY, font=f_s)
    img.save(path)


if __name__ == "__main__":
    import sys
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    make_title(f"{out_dir}/00-title.png")
    make_outro(f"{out_dir}/99-outro.png")
    make_step_divider(f"{out_dir}/10-step1.png", 1, 3,
                      "Seed a new conversation",
                      "encrypt client-side, upload to 0G Storage (~20s)",
                      color=EMERALD)
    make_step_divider(f"{out_dir}/20-step2.png", 2, 3,
                      "File a dispute",
                      "3-LLM jury (Groq) + judge + 0G Chain anchor (~25s)",
                      color=AMBER)
    make_step_divider(f"{out_dir}/30-step3.png", 3, 3,
                      "Verify trustlessly",
                      "0G Storage / local / chain / decrypted = 4 cross-checks",
                      color=INDIGO)
    print(f"wrote all cards to {out_dir}")
