import numbers
import gooeypie as gp

app = gp.GooeyPieApp('Margins Test')

# Make a number widget with 2 buttons and an entry
down_btn = gp.Button('-', None)
number_ent = gp.Entry()
number_ent.text = '1'
up_btn = gp.Button('+', None)

number_ent.width = 40
number_ent.style.justify = 'center'
down_btn.style.font_weight = up_btn.style.font_weight = 'bold'
down_btn.width = up_btn.width = 30

# down_btn.margin_right = 0
# up_btn.margin_left = 0
# number_ent.margin_left = number_ent.margin_right = 0

counter_frame = gp.Frame()
counter_frame.add(down_btn, 1, 1, margin_right=0)
counter_frame.add(number_ent, 2, 1, margin_horizontal=0)
counter_frame.add(up_btn, 3, 1, margin_left=0)

app.add(counter_frame, 1, 1)


name_lbl = gp.Label('Name')
name_lbl.margin_bottom = 0
name_ent = gp.Entry()

email_lbl = gp.Label('Email Address')
email_lbl.margin_bottom = 0
email_ent = gp.Entry()

message_lbl = gp.Label('Message')
message_lbl.margin_bottom = 0
message_txt = gp.Textbox()

submit_btn = gp.Button('Send feedback', None)


form_frame = gp.Frame()
form_frame.margin_top = 100
form_frame.add(name_lbl, 1, 1)
form_frame.add(name_ent, 1, 2)
form_frame.add(email_lbl, 1, 3)
form_frame.add(email_ent, 1, 4)
form_frame.add(message_lbl, 1, 5)
form_frame.add(message_txt, 1, 6)
form_frame.add(submit_btn, 1, 7)

app.add(form_frame, 1, 2, margin=100)



app.run()