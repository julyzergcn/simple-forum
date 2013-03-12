from django.template import Library


register = Library()

@register.filter
def can_edit(value, arg):
    user, obj = value, arg
    if user.is_staff:
        return True
    if hasattr(obj, 'created_by'):
        return obj.created_by==user
    return False

@register.filter
def can_delete(value, arg):
    return can_edit(value, arg)
