import gooeypie as gp


def enable_disable_switch(event):
    switch.disabled = not switch.disabled
    switch_status_lbl.text = f"Switch disabled: {switch.disabled}"

def on_off_switch(event):
    # Styled Switch
    s2 = gp.Switch(text="Styled Switch", value=True)
    s2.style.on_bg_color = "red"
    s2.style.button_color = "blue"
    # switch.value = not switch.value
    switch.toggle()
    switch_status_lbl.text = f"Switch value: {switch.value}"

def switch_changed(event):
    switch_status_lbl.text = f"Change event triggered, switch value: {switch.value}"

def change_text(event):
    switch.text = "New Text"

def get_text(event):
    switch_status_lbl.text = f"Switch text: {switch.text}"

app = gp.GooeyPieApp("Switch Test")
app.width = 800

switch_lbl = gp.Label("Switch")
switch_enable_btn = gp.Button("Enable/disable", enable_disable_switch)
switch_enable_btn.width = 20
switch_on_off_btn = gp.Button("On/Off", on_off_switch)
switch_on_off_btn.width = 20
switch = gp.Switch(text="Switch")
switch_text_set_btn = gp.Button("Change Text", change_text)
switch_text_set_btn.width = 0
switch_text_get_btn = gp.Button("Get Text", get_text)
switch_text_get_btn.width = 0

switch_status_lbl = gp.Label("Status: ")

switch.on_change(switch_changed)

switch_frame = gp.Frame()
switch_frame.add(switch_lbl, 1, 1)
switch_frame.add(switch_enable_btn, 2, 1)
switch_frame.add(switch_on_off_btn, 3, 1)
switch_frame.add(switch, 4, 1)
switch_frame.add(switch_text_set_btn, 5, 1)
switch_frame.add(switch_text_get_btn, 6, 1)
switch_frame.add(switch_status_lbl, 7, 1)


app.add(switch_frame, 1, 1, expand_horizontal=True)

app.set_column_weight(1, 1)
app.run()
