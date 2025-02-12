import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

ALLOWED_FILE_EXTENSIONS = ['.txt', '.pdf', '.doc', '.docx', '.csv', '.jpg', '.jpeg', '.png', '.wav', '.mp3', '.aac', '.mp4']

@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        valid_files = []
        invalid_files = []

        for file in files:
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension in ALLOWED_FILE_EXTENSIONS:
                valid_files.append(file)
            else:
                invalid_files.append(file.name)

        if invalid_files:
            return JsonResponse({'message': f'以下文件类型不允许上传: {", ".join(invalid_files)}'}, status=400)

        for file in valid_files:
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        return JsonResponse({'message': '文件上传成功'})

    return JsonResponse({'message': '无效的请求方法'}, status=400)