from pydub import AudioSegment

name = 'Russian_Postman'

given_audio = AudioSegment.from_ogg("Russian_Postman.ogg", format="ogg")                                                

given_audio.export("Russian_Postman.mp3", format="mp3")
