# from django.http import HttpResponseForbidden, HttpResponseNotFound, FileResponse
# from django.conf import settings
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.utils.decorators import method_decorator
# from django.views import View
from django.http import JsonResponse
from django.middleware.csrf import get_token
# import os

# class ProtectedMediaView(View):
#     @method_decorator(login_required)
#     @method_decorator(user_passes_test(lambda u: u.is_staff))
#     def get(self, request, path):
#         media_path = os.path.join(settings.MEDIA_ROOT, path)

#         if not os.path.exists(media_path):
#             return HttpResponseNotFound("File not found.")

#         return FileResponse(open(media_path, "rb"))

def csrf_token(request):
    token = get_token(request)
    print(token)
    return JsonResponse({"csrfToken": token})