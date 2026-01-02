import gooeypie as gp

def test_methods(event):
    print("Testing methods...")
    
    # Test focus
    print("Setting focus to Entry 2")
    e2.focus()
    
    # Test clear
    print("Clearing Entry 1")
    e1.clear()
    if e1.text == "":
        print("Entry 1 cleared successfully")
    else:
        print(f"Entry 1 clear failed. Text: '{e1.text}'")

    # Test select
    print("Selecting text in Entry 3")
    e3.focus()
    e3.select()
    print("Entry 3 selected (check visually)")

app = gp.GooeyPieApp("Entry Methods Test")

e1 = gp.Entry("Clear Me")
e2 = gp.Entry("Focus Me")
# e3 = gp.Entry("Select Me")

btn = gp.Button("Run Tests", test_methods)

app.add(e1, 1, 1)
app.add(e2, 2, 1)
# app.add(e3, 3, 1)
app.add(btn, 4, 1)

# Check logic also without button press for initial state
# e2.focus() # Should start with focus

app.run()
