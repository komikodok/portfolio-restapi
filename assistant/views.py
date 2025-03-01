from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.exceptions import Throttled
from django.shortcuts import get_object_or_404

from groq import BadRequestError, RateLimitError, APIStatusError
from pydantic import ValidationError
from datetime import datetime
import random
from log import logger
from .models import MessageHistory, Assistant
from .serializers import AssistantSerializer
from .llm import LLMApp

class AssistantView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'chat_throttle'

    def __init__(self, **kwargs):
        self.__llm_app = LLMApp()

    def get(self, request, *args, **kwargs):
        mood = random.choice(["normal", "happy"])
        assistant_image_url = AssistantView.get_image_url(request=request, mood=mood)
        time_of_day = AssistantView.get_time_of_day()

        greeting = [
            "Halo, Senang bertemu denganmu 😊.",
            f"Ada yang bisa aku bantu {time_of_day} ini?",
            f"Selamat {time_of_day} 😁.",
            "Halo! Tanyakan apa saja, aku siap membantu 🚀.",
            f"Halo! Mari kita mulai {time_of_day} ini dengan hal seru!✨."
        ]
        greeting = random.choice(greeting)

        return Response({
            "generation": greeting,
            "image_url": assistant_image_url
        })

    def post(self, request, *args, **kwargs):
        prompt = request.data.get("prompt")
        message_history = request.session.get("message_history", [])

        if not prompt:
            return Response({"detail": "prompt is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user or None

        result = self.__llm_app.invoke(user_input=prompt, message_history=message_history)
        generation = result.generation
        mood = result.mood

        message = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": generation},
        ]
        message_history.extend(message)
        MessageHistory.objects.create(user=user, message=message)

        request.session["message_history"] = message_history[-20:]
        request.session.modified = True

        assistant_image_url = AssistantView.get_image_url(request, mood=mood)

        return Response({
            "generation": generation,
            "image_url": assistant_image_url
        }, status=status.HTTP_201_CREATED)

    @staticmethod
    def get_image_url(request: Request, mood: str):
        assistant = get_object_or_404(Assistant, mood=mood)
        assistant_serializer = AssistantSerializer(assistant, context={"request": request}).data
        image_url = assistant_serializer.get("image_url", "")
        return image_url
    
    @staticmethod
    def get_time_of_day():
        time_of_day = datetime.now().hour
        return next((time for start, end, time in [
            (5, 12, "Pagi"),
            (12, 15, "Siang"),
            (15, 18, "Sore"),
            (0, 5, "Malam"),
            (18, 24, "Malam")
        ] if start <= time_of_day < end), "Malam")

    def get_throttles(self):
        if self.request.method == "POST":
            return [ScopedRateThrottle()]
        return []
    
    def handle_exception(self, exc):
        request = getattr(self, "request", None)
        
        match exc:
            case BadRequestError() | ValidationError():
                assistant_image_url = AssistantView.get_image_url(request, mood="sad")
                logger.error(f"Error: {exc.detail}")
                return Response({
                    'generation': "Maaf aku tidak mendengarnya, bisa tolong ulangi?",
                    'image_url': assistant_image_url
                }, status=status.HTTP_400_BAD_REQUEST)

            case RateLimitError() | Throttled():
                assistant_image_url = AssistantView.get_image_url(request, mood="sad")
                logger.error(f"Error: {exc.detail}")
                return Response({
                    'generation': "Ruby mau istirahat, silahkan kembali lagi besok!",
                    'image_url': assistant_image_url
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)

            case _:
                assistant_image_url = AssistantView.get_image_url(request, mood="sad")
                logger.error(f"Error: {exc.detail}")
                return Response({
                    'generation': "Maaf servernya error nih, silahkan coba lagi nanti ya?",
                    'image_url': assistant_image_url
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClearMessageHistory(APIView):

    def post(self, request):
        request.session["message_history"] = []
        request.session.modified = True

        return
        