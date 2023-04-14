from gtts import gTTS
import os

myText = "wie geht si, meine stimmer bitte"
language = 'nl'

output = gTTS(text=myText, lang=language, slow=False)

print(output)
output.save(f"{myText}.mp3")
os.system(" start output.mp3")