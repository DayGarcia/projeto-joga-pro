from projetoevent.models import Event, Ticket, TicketLog
from projetoevent.consts.action import ALREADY_CHECKED, INVALID, VALID


def get_ticket_data(event_id=None):
    if(event_id):
        return {
            'events': Event.objects.all().order_by('id'),
            'valid_tickets': TicketLog.objects.filter(action=1).filter(event_id=event_id).order_by('id')[:10],
            'invalid_tickets': TicketLog.objects.exclude(action=1).order_by('created_at')[:10],
            'valid_count': TicketLog.objects.filter(action=VALID).count(),
            'invalid_count': TicketLog.objects.filter(action=INVALID).count(),
            'already_checked_count': TicketLog.objects.filter(action=ALREADY_CHECKED).count(),
            'total_count': Ticket.objects.filter(event__is_running=1).count(),
            'gates': Ticket.objects.filter(event__is_running=1).distinct().order_by('gate').values_list('gate', flat=True),
            'id': event_id
        }
    else:
        return {
            'events': Event.objects.all().order_by('id'),
            'valid_tickets': TicketLog.objects.filter(action=1).order_by('id')[:10],
            'invalid_tickets': TicketLog.objects.exclude(action=1).order_by('created_at')[:10],
            'valid_count': TicketLog.objects.filter(action=VALID).count(),
            'invalid_count': TicketLog.objects.filter(action=INVALID).count(),
            'already_checked_count': TicketLog.objects.filter(action=ALREADY_CHECKED).count(),
            'total_count': Ticket.objects.filter(event__is_running=1).count(),
            'gates': Ticket.objects.filter(event__is_running=1).distinct().order_by('gate').values_list('gate', flat=True),
        }
