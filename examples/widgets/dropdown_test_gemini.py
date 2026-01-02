import sys
import os

# Add the project root to sys.path to ensure we import the local gooeypie
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import gooeypie as gp

def test_dropdown():
    app = gp.GooeyPieApp("Dropdown Test")
    
    # Test 1: Constructor Validation (String instead of list)
    try:
        gp.Dropdown(values="Invalid String")
        print("FAIL: Constructor accepted string for values")
    except ValueError as e:
        print(f"PASS: Constructor raised ValueError for string values: {e}")
    except Exception as e:
        print(f"FAIL: Constructor raised unexpected exception for string values: {e}")

    # Test 2: Valid Construction
    try:
        dd = gp.Dropdown(values=["Option 1", "Option 2", "Option 3"], selected_value="Option 2")
        app.add(dd, 1, 1)
        print("PASS: Valid Dropdown created")
    except Exception as e:
        print(f"FAIL: Valid Dropdown creation failed: {e}")
        return

    # Test 3: Selected Property Helper
    if dd.selected == "Option 2":
        print("PASS: Initial selected value correct")
    else:
        print(f"FAIL: Initial selected value incorrect. Got {dd.selected}, expected 'Option 2'")

    # Test 4: Set selected (Valid)
    try:
        dd.selected = "Option 3"
        if dd.selected == "Option 3":
            print("PASS: Set selected to valid value successful")
        else:
            print(f"FAIL: Set selected value failed. Got {dd.selected}, expected 'Option 3'")
    except Exception as e:
        print(f"FAIL: Set selected raised exception: {e}")

    # Test 5: Set selected (Invalid)
    try:
        dd.selected = "Invalid Option"
        print("FAIL: Set selected accepted invalid value")
    except ValueError as e:
        print(f"PASS: Set selected raised ValueError for invalid value: {e}")
    except Exception as e:
        print(f"FAIL: Set selected raised unexpected exception: {e}")

    # Test 6: Change Event
    def on_change(event):
        print(f"PASS: Change event fired! Widget: {event.widget}, Selected: {event.widget.selected}")

    dd.add_event_listener('change', on_change)
    print("info: manually change selection in UI to verify 'change' event logs.")

    # Test 7: Update Values
    try:
        dd.values = ["New A", "New B"]
        if dd.values == ["New A", "New B"]:
            print("PASS: values update successful")
            # Select new value
            dd.selected = "New A"
            print("PASS: Selected new value from updated list")
        else:
             print(f"FAIL: values update failed. Got {dd.values}")
    except Exception as e:
        print(f"FAIL: Updating values raised exception: {e}")

    app.run()

if __name__ == "__main__":
    test_dropdown()
