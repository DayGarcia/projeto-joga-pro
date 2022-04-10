from projetoevent.models import Event


def get_running_event_id():
    return Event.objects.filter(
        is_running=1).values_list('id', flat=True)[0]
