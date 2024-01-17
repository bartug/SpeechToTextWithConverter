# coding=utf-8
import os
import sys
import speech_recognition as sr
import ffmpeg

def convert_to_wav(input_file, output_format):
    # Ses dosyasını WAV formatına dönüştür
    if output_format == '1' or output_format == '4':
        command = "ffmpeg -i {input_file} speech.wav"
        result = os.system(command)
        if result != 0:
            print(f"Hata . ffmpeg  kodu: {result}")
        return os.path.abspath("speech.wav")

    elif output_format == '2' or output_format == '3':
        temp_mp3 = "temp.mp3"
        command_to_mp3 = "ffmpeg -i {input_file} {temp_mp3}"
        result_to_mp3 = os.system(command_to_mp3)
        if result_to_mp3 != 0:
            print(f"Hata . ffmpeg  kodu: {result_to_mp3}")
            return None

        command_to_wav = "ffmpeg -i {temp_mp3} speech.wav"
        result_to_wav = os.system(command_to_wav)
        if result_to_wav != 0:
            print(f"Hata . ffmpeg  kodu: {result_to_wav}")
            return None

        # Geçici MP3 dosyasını temizle
        os.remove(temp_mp3)

        return os.path.abspath("speech.wav")
def convert_speech_to_text(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language="tr-TR")
        return text
    except sr.UnknownValueError:
        return "Ses algılanamadı."
    except sr.RequestError as e:
        return f"Ses hizmeti hatası: {e}"
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Kullanım: python script.py <input_file> <output_format>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_format = sys.argv[2]
    if output_format == '5':
        # convert_speech_to_text kısmı burada
        pass
    else:
        # Dosyayı WAV formatına dönüştür
        audio_file = convert_to_wav(input_file, output_format)
        if audio_file is not None:
            # Dönüştürülen ses dosyasını metne çevir
            result = convert_speech_to_text(audio_file)

            # Türkçe karakterlerle uyumlu bir şekilde görüntülemek için decode işlemi
            try:
                result = result.encode('utf-8').decode('utf-8')
            except UnicodeDecodeError:
                pass

            print(result)

            # Geçici dosyayı temizle
            os.remove(audio_file)
