from django.views.generic import ListView


class ExcelUpload(ListView):
    template_name = 'projetoevent/excel/upload.html'
