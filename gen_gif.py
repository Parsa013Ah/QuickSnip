from PIL import Image, ImageDraw, ImageFont
import os

W, H = 640, 360
frames = []
font = ImageFont.truetype("consola.ttf", 13) if os.path.exists("consola.ttf") else ImageFont.load_default()

lines = [
    ("$ snip add docker-clean -d \"Remove all containers\" -l bash -t \"docker\" -c \"docker rm -f $(docker ps -aq)\"", "#7aa2f7"),
    ("✓ Snippet 'docker-clean' added successfully!", "#9ece6a"),
    ("", None),
    ("$ snip search docker", "#7aa2f7"),
    ("Search Results (1 found)", "#565f89"),
    ("  docker-clean  bash  docker  Remove all containers", "#a9b1d6"),
    ("", None),
    ("$ snip copy docker-clean", "#7aa2f7"),
    ("✓ Copied 'docker-clean' to clipboard!", "#9ece6a"),
    ("", None),
    ("$ snip stats", "#7aa2f7"),
    ("Total Snippets: 1 | Languages: 1 | Tags: 1", "#a9b1d6"),
]

for i in range(len(lines) + 10):
    img = Image.new("RGB", (W, H), "#1a1b26")
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 28], fill="#24283b")
    for j, (text, color) in enumerate(lines[: min(i, len(lines))]):
        if text:
            draw.text((20, 40 + j * 22), text, fill=color or "#c0caf5", font=font)
    if i < len(lines):
        draw.text((20, 40 + min(i, len(lines)) * 22), "$ ", fill="#7aa2f7", font=font)
    frames.append(img)

frames[0].save("demo.gif", save_all=True, append_images=frames[1:], duration=120, loop=0)
print("done")
