import datetime
from django import template
from django.utils.timezone import now

register = template.Library()

@register.filter
def format_post_time(value):
    """
    Format the post time based on the given criteria:
    - "방금" for less than 5 minutes ago
    - "..분전" for less than an hour ago
    - "HH:MM" for posts within today
    - "MM/DD" for posts within the same year but not today
    - "YY/MM/DD" for posts in a different year
    """
    if not isinstance(value, datetime.datetime):
        return value  # If value is not a datetime object, return it as-is

    now_time = now()
    delta = now_time - value

    if delta.days == 0:  # Same day
        if delta.seconds < 300:  # Less than 5 minutes
            return "방금"
        elif delta.seconds < 3600:  # Less than an hour
            minutes = delta.seconds // 60
            return f"{minutes}분전"
        else:  # More than an hour but today
            return value.strftime("%H:%M")
    elif now_time.year == value.year:  # Same year
        return value.strftime("%m/%d")
    else:  # Different year
        return value.strftime("%y/%m/%d")
