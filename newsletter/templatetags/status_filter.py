from django import template

register = template.Library()


@register.filter
def status_class(value):
    """
    Возвращает CSS-класс по статусу рассылки.
    """
    if not value:
        return "secondary"
    mapping = {
        "created": "$purple",
        "started": "success",
        "completed": "info",
    }
    return mapping.get(value, "secondary")
