import gooeypie as gp

def main():
    app = gp.GooeyPieApp("Justify Test")
    
    # Entry Test
    e1 = gp.Entry("Left (Default)")
    
    e2 = gp.Entry("Center")
    e2.style.justify = 'center'
    
    e3 = gp.Entry("Right")
    e3.style.justify = 'right'
    
    # Label Test (need width to see alignment)
    l1 = gp.Label("Left Label")
    l1.width = 200
    l1.style.justify = 'left'
    l1.style.bg_color = 'lightgray' # To see the width
    
    l2 = gp.Label("Center Label")
    l2.width = 200
    l2.style.justify = 'center'
    l2.style.bg_color = 'lightgray'
    
    l3 = gp.Label("Right Label")
    l3.width = 200
    l3.style.justify = 'right'
    l3.style.bg_color = 'lightgray'
    
    app.add(e1, 1, 1)
    app.add(e2, 2, 1)
    app.add(e3, 3, 1)
    
    app.add(l1, 1, 2)
    app.add(l2, 2, 2)
    app.add(l3, 3, 2)
    
    print(f"Entry Right Justify: {e3.style.justify}")
    print(f"Label Right Justify: {l3.style.justify}")

    app.run()

if __name__ == "__main__":
    main()
