import gooeypie as gp

def verify_readonly_state():
    app = gp.GooeyPieApp("Read-only State Verification")

    dd = gp.Dropdown(["Option 1", "Option 2"])
    app.add(dd, 1, 1)

    # Test 1: Initial state should be readonly
    print(f"Initial state: {dd._ctk_object.cget('state')}")
    if dd._ctk_object.cget('state') == 'readonly':
        print("PASS: Initial state is readonly")
    else:
        print(f"FAIL: Initial state is {dd._ctk_object.cget('state')}")

    # Test 2: Disable widget
    dd.disabled = True
    print(f"Disabled state: {dd._ctk_object.cget('state')}")
    if dd._ctk_object.cget('state') == 'disabled':
        print("PASS: Widget correctly disabled")
    else:
        print(f"FAIL: Widget disabled state is {dd._ctk_object.cget('state')}")

    # Test 3: Re-enable widget (should return to readonly)
    dd.disabled = False
    print(f"Restored state: {dd._ctk_object.cget('state')}")
    if dd._ctk_object.cget('state') == 'readonly':
        print("PASS: Widget correctly restored to readonly")
    else:
        print(f"FAIL: Widget restored state is {dd._ctk_object.cget('state')}")

    app.after(100, app.quit)
    app.run()

if __name__ == "__main__":
    verify_readonly_state()
