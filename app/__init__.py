from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import io
from phonemizer import phonemize
import phonemizer
import subprocess
subprocess.run(['sudo', 'apt-get', 'update'])
subprocess.run(['sudo', 'apt-get', 'install', 'espeak'])

app = Flask(__name__)

@app.route("/")
def home():
    return "home"

@app.route('/phonemes', methods=['POST'])
def phonemize_text():
    try:
        data = request.json
        text = data.get('text', '')
        language = data.get('language', 'de')
        phonemes = phonemize(text, language=language)
        return jsonify({'phonemes': phonemes})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/tts', methods=['POST'])
async def tts():
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data received'})

        text = data.get('text')
        lang = data.get('lang')
        if not text or not lang:
            return jsonify({'success': False, 'error': 'Missing required parameters'})

        slow = data.get('slow', False)

        output = io.BytesIO()
        gTTS(text=text, lang=lang, slow=slow).write_to_fp(output)
        output.seek(0)

        return send_file(output, mimetype='audio/mpeg', download_name=f"{text}.mp3", as_attachment=True)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run()