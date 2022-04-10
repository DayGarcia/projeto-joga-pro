from projetoevent.models import Event, Ticket, TicketLog
from projetoevent.consts.action import ALREADY_CHECKED, INVALID, VALID


def get_ticket_data(event_id=None, gate=None, user=None, code=None):
    if(event_id):
        valid_tickets = TicketLog.objects.filter(action=VALID).filter(
            event_id=event_id).order_by('id')[:10]
        invalid_tickets = TicketLog.objects.exclude(
            action=VALID).order_by('created_at')[:10]
        valid_count = TicketLog.objects.filter(action=VALID).count()
        invalid_count = TicketLog.objects.filter(action=INVALID).count()
        already_checked_count = TicketLog.objects.filter(
            action=ALREADY_CHECKED).count()
        total_count = Ticket.objects.filter(event__is_running=1).count()

    # else:
    #     events = Event.objects.all().order_by('id')
    #     valid_tickets = TicketLog.objects.filter(
    #         action=VALID).order_by('id')[:10]
    #     invalid_tickets = TicketLog.objects.exclude(
    #         action=VALID).order_by('created_at')[:10]
    #     valid_count = TicketLog.objects.filter(action=VALID).count()
    #     invalid_count = TicketLog.objects.filter(action=INVALID).count()
    #     already_checked_count = TicketLog.objects.filter(
    #         action=ALREADY_CHECKED).count()
    #     total_count = Ticket.objects.filter(event__is_running=1).count(),
    #     gates = Ticket.objects.filter(event__is_running=1).distinct().order_by(
    #         'gate').values_list('gate', flat=True)

    events = Event.objects.all().order_by('id')
    gates = Ticket.objects.filter(event__is_running=1).distinct().order_by(
        'gate').values_list('gate', flat=True)

    id = event_id

    return {
        'events': events,
        'valid_tickets': valid_tickets,
        'invalid_tickets': invalid_tickets,
        'valid_count': valid_count,
        'invalid_count': invalid_count,
        'already_checked_count': already_checked_count,
        'total_count': total_count,
        'gates': gates,
        'id': id
    }
