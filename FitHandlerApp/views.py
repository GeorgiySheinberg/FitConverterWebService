from django.shortcuts import render

from .converters.converters import convert_to_excel, convert_to_csv
from .models import MyFiles


def index(request):
    if request.method == "POST":
        print(dict(request.POST))
        fit_file = MyFiles.objects.create(
            file=request.FILES.get("file"),
        )

        file_name = str(fit_file.file).replace("upldfile/", "")
        if dict(request.POST).get("format")[0] == 'csv':
            file = convert_to_csv(
                f"media/upldfile/{file_name}",
                file_name,
                dict(request.POST).get("fit_messages")
            )
        if dict(request.POST).get("format")[0] == 'xlsx':
            file = convert_to_excel(
                f"media/upldfile/{file_name}",
                file_name,
                dict(request.POST).get("fit_messages")
            )

        file = MyFiles.objects.create(
            file=file
        )
        context = {
            "file": file
        }

        return render(request, 'download_media.html', context)
    if request.method == "GET":
        return render(request, 'test.html', )
