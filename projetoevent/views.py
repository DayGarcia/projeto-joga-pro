from importlib.resources import path
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.core import serializers

import openpyxl
from projetoevent.consts.action import ALREADY_CHECKED, INVALID, VALID
from projetoevent.models import Event, Ticket, TicketLog
from projetoevent.helpers.ticket_query import get_ticket_data


class ExcelUpload(View):
    def get(self, request):
        context = get_ticket_data()

        return render(request, 'projetoevent/home.html', context)

    def post(self, request):
        # Define variable to load the wookbook
        wookbook = openpyxl.load_workbook(request.FILES['file'])

        # Define variable to read the active sheet:
        worksheet = wookbook.active

        e = Event(
            is_running=0
        )
        e.save()

        # Iterate the loop to read the cell values
        for i in range(0, worksheet.max_row):
            if i == 0:
                continue
            for col in worksheet.iter_cols(1, worksheet.max_column):
                t = Ticket(
                    code=worksheet.cell(row=i+1, column=2).value,
                    rfid=worksheet.cell(row=i+1, column=3).value,
                    status=worksheet.cell(row=i+1, column=4).value,
                    user_id=worksheet.cell(row=i+1, column=5).value,
                    type=worksheet.cell(row=i+1, column=6).value,
                    gate=worksheet.cell(row=i+1, column=7).value,
                    sector=worksheet.cell(row=i+1, column=8).value,
                    block=worksheet.cell(row=i+1, column=9).value,
                    row=worksheet.cell(row=i+1, column=10).value,
                    seat=worksheet.cell(row=i+1, column=11).value,
                    extra=worksheet.cell(row=i+1, column=12).value,
                    event=e
                )
                t.save()

        return render(request, 'projetoevent/home.html', {'msg': 'Jogo importado com sucesso!'})
        # return redirect('/home', {'msg': 'Jogo importado com sucesso!'})


class Charts(View):
    def get(self, request):
        if 'id' in request.GET:
            context = get_ticket_data(request.GET['id'])
        else:
            context = get_ticket_data()

        return render(request, 'projetoevent/charts.html', context)


class RefreshTickets():
    def get(request):
        if is_ajax(request) and request.method == "GET":
            data = get_ticket_data()
            json = serializers.serialize('json', data)
            print('meta', json)

            return JsonResponse({"data": json}, status=200)

        return JsonResponse({}, status=400)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
