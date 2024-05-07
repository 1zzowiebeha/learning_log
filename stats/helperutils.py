from django.db.models import Sum
from django.contrib.auth.models import User

from learning_logs.models import TopicHourData, Topic
# cache this for better performance. there may come problems
# .. if we have a zero-downtime system that lets us
# .. alter columns in production.
# in that case, we may wish to update the cache after
# .. we alter.

# we'll also want to change this, so that
# .. we update this value in max_hours_reached,
# .. so that we can populate the cache again during run-time.

max_length = TopicHourData._meta.get_field('hours').max_length

def get_total_hours(topic: Topic):
    total_hours = TopicHourData.objects.filter(topic=topic) \
                                       .aggregate(Sum('hours'))['hours__sum']
    if total_hours is None:
        return 0
    else:
        return total_hours
    
def max_hours_reached(topic: Topic):
    """Return a boolean based on whether the
    given topic's 'hours' fields has
    reached its max_length value."""

    # cache this for better performance. there may come problems
    # .. if we have a zero-downtime system that lets us
    # .. alter columns in production.
    # in that case, we may wish to update the cache afterwards.

    # aggregate the hours field and use it in this comparison
    # better performance?
    total_hours = get_total_hours(topic)

    if total_hours >= max_length:
        return True
    else:
        return False