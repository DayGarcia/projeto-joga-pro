from projetoevent.models import Event


def get_running_event_id():
    running_event_id = Event.objects.filter(
        is_running=1).values_list('id', flat=True)
    if len(running_event_id) > 0:
        return running_event_id[0]
    else:
        return 0
