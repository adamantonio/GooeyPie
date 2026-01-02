import gooeypie as gp

app = gp.GooeyPieApp("SVG Test")

try:
    # Try to load SVG directly in ImageButton
    btn = gp.ImageButton("../images/test.svg", lambda e: print("Clicked"))
    app.add(btn, 1, 1)
except Exception as e:
    print(f"Failed to load SVG: {e}")
    lbl = gp.Label(f"SVG Failed: {e}")
    app.add(lbl, 1, 1)

app.run()
