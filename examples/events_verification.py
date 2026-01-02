import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gooeypie as gp

def test_events():
    print("Initializing App...")
    app = gp.GooeyPieApp("Event Test")

    print("Creating Checkbox...")
    def on_change(event):
        print(f"Checkbox change: {event.name}")

    cb = gp.Checkbox("Verify Me")
    cb.add_event_listener('change', on_change)
    app.add(cb, 1, 1)

    print("Creating Button...")
    def on_press(event):
        print(f"Button press: {event.name}")

    def on_hover(event):
        print(f"Hover: {event.name}")

    btn = gp.Button("Hover/Press Me")
    btn.add_event_listener('press', on_press)
    btn.add_event_listener('mouse_over', on_hover)
    app.add(btn, 2, 1)
    
    print("Verifying command property logic...")
    def new_change(event):
        print("New change listener!")
    
    # Verify initial listener count
    if len(cb._event_listeners['change']) != 1:
        print("FAILED: Expected 1 change listener")
    else:
        print("PASS: Initial listener count")
        
    # Update command property
    cb.command = new_change
    
    # Verify listener replaced
    if len(cb._event_listeners['change']) != 1:
         print("FAILED: Expected 1 change listener after setter")
    elif cb._event_listeners['change'][0] != new_change:
         print("FAILED: Listener not updated correctly")
    else:
         print("PASS: Command property update")

    print("Verification Setup Complete. No errors.")
    return app

if __name__ == "__main__":
    app = test_events()
