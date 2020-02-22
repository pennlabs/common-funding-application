from app.models import Grant


def funders_grant_data_to_item(item, funder):
    grant = Grant.objects.filter(item=item, funder=funder)
    return (float(grant.first().amount), item.id) if grant else (None, item.id)


def funder_item_data(item, funders):
    funders_data = []
    for funder in funders:
        grant_amount, grant_id = funders_grant_data_to_item(item, funder)
        funders_data.append((funder.id, grant_amount, grant_id))
    return (item, funders_data)


def get_or_none(model, **kwargs):
    """Get an object, or None."""
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
