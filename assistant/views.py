from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework import status

from .chain import LLMApp

class AssistantView(APIView):
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'chat_throttle'

    def __init__(self, **kwargs):
        self.__llm_app = LLMApp()

    def get(self, request, *args, **kwargs):
        print(f"session: key{request.session.session_key}")
        return Response({"status": "ok"}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        prompt = request.data.get("prompt")
        message_history = request.session.get("message_history", [])

        if not prompt:
            return Response({"detail": "prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

        message_history.append(prompt)
        request.session["message_history"] = message_history
        request.session.modified = True

        return Response({"message_history": message_history}, status=status.HTTP_200_OK)

    #     try:
    #         result = await self.__llm_app.ainvoke(input=prompt, message_history=message_history)
    #         generation = result.generation
    #         mood = result.mood
    #     except Exception as err:
    #         print(err)

        