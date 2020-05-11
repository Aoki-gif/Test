import os 

outtext = "呼び出し中です。少々お待ちください。"

language = "ja"

myobj = gTTS(text=outtext, lang=language, slow=false)

myobj.save("OutAnaunce.mp3")

os.system("mpg321 OutAnaunce.mp3")
