import time
from flask import Flask, render_template, request
from summarizer import youtubeSummarizer
import translators.server as tss
from gtts import gTTS
import os

app = Flask(__name__)
app.secret_key = "123"

summary = ''''''
ytlink = ''
to_translate = ''
VOICE_PATH = './static/voice.mp3'

@app.route('/', methods=['GET', 'POST'])
def Home() :
    global summary, ytlink
    # Reading all packet files from data folder
    if request.method == "POST" :
        try :
            ytlink = str(request.form['ytlink']).strip()
            summary = youtubeSummarizer(ytlink)
            myobj = gTTS(text = summary, lang = 'en')
            if os.path.isfile(VOICE_PATH) :
                os.remove(VOICE_PATH)
            myobj.save(VOICE_PATH)
            time.sleep(10)
            return render_template('index.html', ytlink = ytlink, summary = summary, audio = True)
        except Exception as e :
            print(e)
            return render_template('index.html')
    return render_template('index.html')

@app.route('/translate', methods=['GET', 'POST'])
def translator() -> 'Translated Summary' :
    global summary, ytlink, to_translate
    if request.method == "POST" :
        try :
            to_translate = str(request.form['to_translate']).strip()
            if to_translate == 'hi' :
                translated_summary = tss.google(summary, to_language = 'hi')
            elif to_translate == 'gu' :
                translated_summary = tss.google(summary, to_language = 'gu')
            elif to_translate == 'bn' :
                translated_summary = tss.google(summary, to_language = 'bn')
            elif to_translate == 'fr' :
                translated_summary = tss.google(summary, to_language = 'fr')
            elif to_translate == 'de' : # german
                translated_summary = tss.google(summary, to_language = 'de')

            if os.path.isfile(VOICE_PATH) :
                os.remove(VOICE_PATH)

            myobj = gTTS(text = translated_summary, lang = to_translate)
            myobj.save(VOICE_PATH)
            time.sleep(10)
            return render_template('index.html', ytlink = ytlink, summary = translated_summary, translated_audio = True)
        except Exception as e :
            return render_template('index.html')

if __name__ == '__main__' :
    app.run(debug = True, port = 5000)
