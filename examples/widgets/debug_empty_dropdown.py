import gooeypie as gp
import sys

def test_empty_dropdown():
    app = gp.GooeyPieApp("Empty Dropdown Test")

    # Test 1: Dropdown with empty list
    print("Creating Dropdown with empty list...")
    try:
        dd_empty = gp.Dropdown([])
        app.add(dd_empty, 1, 1)
        if dd_empty.selected == "" or dd_empty.selected is None:
             print("PASS: Dropdown([]) created successfully and is blank")
        else:
             print(f"FAIL: Dropdown([]) created but has value: '{dd_empty.selected}'")
    except Exception as e:
        print(f"FAIL: Dropdown([]) raised: {e}")

    # Test 2: Dropdown() without args
    print("\nCreating Dropdown without args...")
    try:
        dd_no_args = gp.Dropdown()
        app.add(dd_no_args, 2, 1)
        if dd_no_args.selected == "" or dd_no_args.selected is None:
            print("PASS: Dropdown() created successfully and is blank")
        else:
            print(f"FAIL: Dropdown() created but has value: '{dd_no_args.selected}'")
    except TypeError as e:
        print(f"FAIL: Dropdown() raised TypeError: {e}")
    except Exception as e:
        print(f"FAIL: Dropdown() raised unexpected: {e}")

    app.run()

if __name__ == "__main__":
    test_empty_dropdown()
