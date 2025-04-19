import os
from uuid import uuid4

import ffmpeg
import speech_recognition as sr
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

recognizer = sr.Recognizer()


@csrf_exempt
def speech_to_text(request):
    if request.method == "POST" and request.FILES.get("audio"):
        input_path, output_path = f"{uuid4()}.wav", f"{uuid4()}.wav"

        with open(input_path, "wb+") as input_tmp:
            for chunk in request.FILES["audio"].chunks():
                input_tmp.write(chunk)

        ffmpeg.input(input_path).output(output_path, acodec="pcm_s16le", ac=1, ar="16k").run(quiet=True)

        with sr.AudioFile(output_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language="ru-RU")

        os.remove(input_path)
        os.remove(output_path)

        return JsonResponse({"text": text})

    return JsonResponse({"error": "Invalid request"}, status=400)
