from django import template

register = template.Library()


@register.filter
def status_class(value):
    """
    Возвращает CSS-класс по статусу рассылки.
    """
    return {
        "created": "Создана",
        "started": "Запущена",
        "completed": "Завершена",
    }.get(value, "secondary")
