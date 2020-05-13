import codecs
import os
import re
import folium
from app.gen_map import gen_map as gen_map
from datetime import datetime as dt
from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

def transmit_msg(phone, sms):
    stamp = dt.now().strftime('%s')
    out_filename = "/home/pi/smsmessages/in/message-" + str(stamp)
    with open(out_filename, 'w') as out_file:
        aprs_packet = "KI7ADJ>APRS,WIDE2-1::SMSGTE  :@" + phone + " " + sms
        out_file.write(aprs_packet)
    return

@app.route('/')
def index():
    gen_map()
    return render_template('index.html', title='Map')

@app.route('/send', methods=['GET', 'POST'])
def send():
    form = LoginForm()
    if form.validate_on_submit():
        transmit_msg(form.phone_num.data, form.sms_text.data)
        flash('Message Sent to {}, Message={}'.format(
            form.phone_num.data, form.sms_text.data))
        return redirect('/messages')
    return render_template('send.html', title='Send TEXT over Radio', form=form)

@app.route('/messages', methods=['GET'])
def messages():
    for root, dirs, files in os.walk("/home/pi/smsmessages/out"):
        for filename in files:
            with codecs.open(root + '/' + filename, 'r', encoding='utf-8', errors='ignore') as line:
                line = line.readline()
                match = re.search('::(KI7ADJ\s+:@\d+\s.*){M\d+', str(line))
                if match:
                    msg_date = dt.strptime(filename, '%Y%m%d-%H%M%S-%f')
                    flash('{} - {}'.format(msg_date, match.groups(1)))
    return render_template('messages.html', title='Messages')
