from rich.console import Console, RenderableType
from rich.protocol import rich_cast


def measure(console: Console, renderable: RenderableType, default: int) -> int:
    """Measure a rich renderable.

    Args:
        console: A console object.
        renderable: Rich renderable.
        default: Default width to use if renderable does not expose dimensions.

    Returns:
        Width in cells
    """
    width = default
    renderable = rich_cast(renderable)
    get_console_width = getattr(renderable, "__rich_measure__", None)
    if get_console_width is not None:
        render_width = get_console_width(console, console.options).maximum
        width = max(0, render_width)
    return width
