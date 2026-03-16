from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Splits the string by the given argument."""
    return value.split(arg)

@register.filter
def trim(value):
    """Removes leading and trailing whitespace."""
    return value.strip()

@register.filter
def mul(value, arg):
    """Multiplies the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def startswith(value, arg):
    """Checks if the string starts with the given argument."""
    if not value or not arg:
        return False
    return str(value).startswith(str(arg))

@register.filter
def abs_value(value):
    """Returns the absolute value of a number."""
    try:
        import math
        return math.fabs(float(value))
    except (ValueError, TypeError):
        return 0

@register.filter
def message_time(value):
    """Format time for messages like '2 min ago', 'Yesterday', 'Oct 8, 2022'"""
    from django.utils import timezone
    from datetime import timedelta
    
    if not value:
        return ""
    
    # Si c'est déjà un datetime, l'utiliser directement
    if hasattr(value, 'date'):
        dt = value
    else:
        # Essayer de convertir
        try:
            from django.utils.dateparse import parse_datetime
            dt = parse_datetime(str(value))
            if not dt:
                return ""
        except:
            return ""
    
    now = timezone.now()
    if dt.tzinfo is None:
        dt = timezone.make_aware(dt)
    
    diff = now - dt
    
    # Moins d'une minute
    if diff.total_seconds() < 60:
        return "just now"
    
    # Moins d'une heure
    if diff.total_seconds() < 3600:
        minutes = int(diff.total_seconds() / 60)
        return f"{minutes} min ago"
    
    # Aujourd'hui
    if dt.date() == now.date():
        return dt.strftime("%I:%M %p").lstrip('0')
    
    # Hier
    yesterday = now.date() - timedelta(days=1)
    if dt.date() == yesterday:
        return "Yesterday"
    
    # Cette année
    if dt.year == now.year:
        return dt.strftime("%b %d, %Y")
    
    # Autre année
    return dt.strftime("%b %d, %Y")