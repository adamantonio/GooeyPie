import gooeypie as gp
import customtkinter as ctk

def test_readonly_appearance():
    app = gp.GooeyPieApp("Read-only Appearance Test")

    # Normal Dropdown (currently editable by default)
    dd_normal = gp.Dropdown(["Option 1", "Option 2"])
    dd_normal.selected = "Option 1"
    
    # We want to test what happens if we set it to readonly manually first (using underlying ctk object if needed to test)
    # But I will modify the class. 
    # For this test, I will manually configure the inner object to see the visual difference.
    
    label_norm = gp.Label("Normal (Editable)")
    app.add(label_norm, 1, 1)
    app.add(dd_normal, 1, 2)
    
    dd_readonly = gp.Dropdown(["Option A", "Option B"])
    dd_readonly.selected = "Option A"
    
    # Manually hack to test "readonly" on the CTk object
    # We need to wait for it to be created? No, gp widgets create immediately inside App context usually?
    # Wait, GooeyPie widgets create lazily or immediately? 
    # Looking at code: `_create_widget` is called when?
    # In `grid` (via `add` -> `grid`) or `pack`.
    
    label_ro = gp.Label("Read-only (Mock)")
    app.add(label_ro, 2, 1)
    app.add(dd_readonly, 2, 2)
    
    # We can't access _ctk_object until after run? Or checking internal keys.
    # Actually, let's just use this script to VERIFY after I make the change.
    
    print("Please verify: Can you type in the Second dropdown? Does it look different?")
    
    # I will modify the class code directly, then run this.
    
    app.run()

if __name__ == "__main__":
    test_readonly_appearance()
