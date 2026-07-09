from django.shortcuts import render


def upload_document(request):

    return render(
        request,
        "documents/upload.html"
    )