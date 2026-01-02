import sys
import os
import gooeypie as gp

# Manually verify internal state after update
def test_values_update():
    app = gp.GooeyPieApp("Values Update Test")
    
    # Create dropdown with initial values
    initial_values = ["A", "B", "C"]
    dd = gp.Dropdown(initial_values, "A")
    app.add(dd, 1, 1)
    
    # Check initial state
    print(f"Initial GooeyPie values: {dd.values}")
    print(f"Initial CTk values: {dd._ctk_object.cget('values')}")
    
    # Update values
    new_values = ["1", "2", "3"]
    print(f"Updating values to: {new_values}")
    dd.values = new_values
    
    # Check state after update
    print(f"Post-update GooeyPie values: {dd.values}")
    print(f"Post-update CTk values: {dd._ctk_object.cget('values')}")
    
    if dd.values == new_values and dd._ctk_object.cget('values') == new_values:
        print("PASS: Values updated correctly in object.")
    else:
        print("FAIL: Values did not match.")

    # Test with integers (to reproducing the ljust error potentially?)
    try:
        print("Updating values to integers [4, 5, 6]...")
        dd.values = [4, 5, 6]
        print("Updated to integers successfully (if no error above).")
        print(f"Values check: {dd.values}")
    except Exception as e:
        print(f"CAUGHT ERROR with integers: {e}")

    # We will close immediately after check
    app.after(100, app.quit)
    app.run()

if __name__ == "__main__":
    test_values_update()
