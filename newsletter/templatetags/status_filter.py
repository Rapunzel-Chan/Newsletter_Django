from django import template

register = template.Library()


@register.filter
def status_class(value):
    """
    Возвращает CSS-класс по статусу рассылки.
    """
    if not value:
        return "bg-secondary text-white"
    mapping = {
        "created": "bg-rose-200 text-gray-800",
        "started": "bg-rose-400 text-white",
        "completed": "bg-rose-600 text-white",
    }
    return mapping.get(value, "bg-secondary text-white")
