from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin


def update_views(request, object):      # 2 property it's object from db thay will be update
    """ Логика для обновления просмотров на посте, каждый раз, когда юзер просмотрит его """

    context = {}

    # getting the model of that specific object
    hit_count = get_hitcount_model().objects.get_for_object(object)

    # getting hits by specific objects
    hits = hit_count.hits

    hitcontext = context["hitcount"] = {'pk': hit_count.pk}

    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    if hit_count_response.hit_counted:

        hits = hits + 1

        hitcontext['hitcounted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

