import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from django.core import serializers

from projetoevent.helpers.tasks import save_event_task
from projetoevent.models import Event, Ticket, TicketLog
from projetoevent.helpers.ticket_query import format_event_to_json, get_ticket_data
from projetoevent.helpers.event_query import get_running_event_id

from django_q.tasks import async_task


class Home(View):
    def get(self, request):

        context = get_ticket_data(get_running_event_id(), request.GET.get(
            'gate_id', None), None, request.GET.get('ticket', None))

        return render(request, 'projetoevent/home.html', context)

    def post(self, request):

        # stop all running events
        Event.objects.filter(is_running=1).update(is_running=0)

        # set new event to running
        event = Event(
            is_running=1,
            is_uploading=1,
        )
        event.save()

        async_task('projetoevent.helpers.tasks.save_event_task', request.FILES['file'], event)

        context = get_ticket_data(get_running_event_id(), request.GET.get(
            'gate_id', None), None, request.GET.get('ticket', None))

        # return render(request, 'projetoevent/home.html', context)
        return redirect('/home')


class RunEvent(View):

    def post(self, request):
        # set all current event to not running
        Event.objects.filter(is_running=1).update(is_running=0)

        # set the new event to running
        e = Event.objects.get(id=request.POST['event_id'])
        e.is_running = 1
        e.save()

        # filter = '?event_id=' + request.POST['event_id']
        filter = '?filter=1'
        if(request.POST['gate_id'] != '0'):
            filter += '&gate_id=' + request.POST['gate_id']

        """ if(request.POST['user'] != ''):
            filter += '&user=' + request.POST['user'] """

        if(request.POST['ticket'] != ''):
            filter += '&ticket=' + request.POST['ticket']

        return redirect('/home' + filter, {'msg': 'Jogo iniciado com sucesso!'})


class Charts(View):
    def get(self, request):
        if 'event_id' in request.GET:
            context = get_ticket_data(request.GET['event_id'])
        else:
            context = get_ticket_data(get_running_event_id())

        return render(request, 'projetoevent/charts.html', context)


class RefreshTickets():
    def get(request):
        if is_ajax(request) and request.method == "GET":
            data = get_ticket_data(get_running_event_id())
            # json = serializers.serialize('json', data)
            jsona = format_event_to_json(data)

            return JsonResponse(jsona, status=200)

        return JsonResponse({}, status=400)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
