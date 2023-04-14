from flask import Flask, request, send_file
from gtts import gTTS
import io

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def tts():
    try:
        data = request.get_json()
        text = data['text']
        lang = data['lang']
        slow = data.get('slow', False)

        output = io.BytesIO()
        gTTS(text=text, lang=lang, slow=slow).write_to_fp(output)
        output.seek(0)
        
        return send_file(output, mimetype='audio/mpeg', as_attachment=True, attachment_filename='output.mp3')
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
