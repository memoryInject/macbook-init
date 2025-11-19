"""
Modern Fancy Print - A stylish console output library
"""


class FancyPrint:
    # ANSI color codes
    COLORS = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "bright_black": "\033[90m",
        "bright_red": "\033[91m",
        "bright_green": "\033[92m",
        "bright_yellow": "\033[93m",
        "bright_blue": "\033[94m",
        "bright_magenta": "\033[95m",
        "bright_cyan": "\033[96m",
        "bright_white": "\033[97m",
    }

    BG_COLORS = {
        "bg_black": "\033[40m",
        "bg_red": "\033[41m",
        "bg_green": "\033[42m",
        "bg_yellow": "\033[43m",
        "bg_blue": "\033[44m",
        "bg_magenta": "\033[45m",
        "bg_cyan": "\033[46m",
        "bg_white": "\033[47m",
    }

    STYLES = {
        "bold": "\033[1m",
        "dim": "\033[2m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "blink": "\033[5m",
        "reverse": "\033[7m",
        "hidden": "\033[8m",
        "strikethrough": "\033[9m",
    }

    RESET = "\033[0m"

    ICONS = {
        "success": "✓",
        "error": "✗",
        "warning": "⚠",
        "info": "ℹ",
        "star": "★",
        "heart": "♥",
        "arrow": "→",
        "bullet": "•",
        "check": "✔",
        "cross": "✘",
        "sparkle": "✨",
        "fire": "🔥",
        "rocket": "🚀",
        "trophy": "🏆",
    }

    @classmethod
    def _apply_style(cls, text, color=None, bg=None, style=None):
        """Apply color and style formatting to text"""
        result = ""

        if style:
            styles = style if isinstance(style, list) else [style]
            for s in styles:
                if s in cls.STYLES:
                    result += cls.STYLES[s]

        if color and color in cls.COLORS:
            result += cls.COLORS[color]

        if bg and bg in cls.BG_COLORS:
            result += cls.BG_COLORS[bg]

        result += str(text) + cls.RESET
        return result

    @classmethod
    def print(
        cls,
        *args,
        color=None,
        bg=None,
        style=None,
        icon=None,
        prefix="",
        suffix="",
        sep=" ",
        end="\n",
    ):
        """
        Modern fancy print with styling options

        Args:
            *args: Text to print
            color: Text color (e.g., 'red', 'green', 'cyan')
            bg: Background color (e.g., 'bg_blue', 'bg_red')
            style: Text style or list of styles (e.g., 'bold', ['bold', 'underline'])
            icon: Icon name from ICONS dict
            prefix: Text to prepend
            suffix: Text to append
            sep: Separator between args
            end: End character
        """
        text = sep.join(str(arg) for arg in args)

        if icon and icon in cls.ICONS:
            text = f"{cls.ICONS[icon]} {text}"

        if prefix:
            text = f"{prefix}{text}"

        if suffix:
            text = f"{text}{suffix}"

        styled_text = cls._apply_style(text, color, bg, style)
        print(styled_text, end=end)

    @classmethod
    def success(cls, *args, **kwargs):
        """Print success message (green with checkmark)"""
        cls.print(*args, color="bright_green", icon="success", **kwargs)

    @classmethod
    def error(cls, *args, **kwargs):
        """Print error message (red with X)"""
        cls.print(*args, color="bright_red", icon="error", style="bold", **kwargs)

    @classmethod
    def warning(cls, *args, **kwargs):
        """Print warning message (yellow with warning symbol)"""
        cls.print(*args, color="bright_yellow", icon="warning", **kwargs)

    @classmethod
    def info(cls, *args, **kwargs):
        """Print info message (cyan with info symbol)"""
        cls.print(*args, color="bright_cyan", icon="info", **kwargs)

    @classmethod
    def header(cls, *args, **kwargs):
        """Print header with style"""
        cls.print(*args, color="bright_magenta", style=["bold", "underline"], **kwargs)

    @classmethod
    def box(cls, text, color="cyan", padding=1):
        """Print text in a box"""
        lines = text.split("\n")
        width = max(len(line) for line in lines) + padding * 2

        border_color = color

        # Top border
        cls.print("┌" + "─" * width + "┐", color=border_color)

        # Content
        for line in lines:
            padded_line = " " * padding + line + " " * (width - len(line) - padding)
            cls.print("│" + padded_line + "│", color=border_color)

        # Bottom border
        cls.print("└" + "─" * width + "┘", color=border_color)

    @classmethod
    def gradient(cls, text, colors=["blue", "cyan", "green"]):
        """Print text with gradient effect"""
        if not text:
            return

        chars_per_color = max(1, len(text) // len(colors))
        result = ""

        for i, char in enumerate(text):
            color_idx = min(i // chars_per_color, len(colors) - 1)
            result += cls._apply_style(char, color=colors[color_idx])

        print(result)

    @classmethod
    def rainbow(cls, text):
        """Print text with rainbow colors"""
        rainbow_colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
        cls.gradient(text, rainbow_colors)

    @classmethod
    def progress(cls, current, total, width=40, color="green"):
        """Print a progress bar"""
        percentage = current / total
        filled = int(width * percentage)
        # bar = '█' * filled + '░' * (width - filled)
        bar = "■" * filled + "□" * (width - filled)
        percent_text = f"{percentage * 100:.1f}%"

        cls.print(f"\033[2K\r[{bar}] {percent_text}", color=color, end="")

        if current >= total:
            print()  # New line when complete


# Create a convenient global instance
fp = FancyPrint()


def demo():
    print("=== Fancy Print Demo ===\n")

    # Basic colored output
    fp.print("Hello, World!", color="cyan", style="bold")
    fp.print("This is underlined", style="underline")
    fp.print("Multiple styles", style=["bold", "italic"], color="magenta")

    print()

    # Preset message types
    fp.success("Operation completed successfully!")
    fp.error("Something went wrong!")
    fp.warning("This is a warning message")
    fp.info("Here's some information")
    fp.header("This is a Header")

    print()

    # Icons
    fp.print("Achievement unlocked!", icon="trophy", color="yellow")
    fp.print("Deploy to production", icon="rocket", color="blue")
    fp.print("Hot feature!", icon="fire", color="red")
    fp.print("Made with", icon="heart", color="magenta")

    print()

    # Box
    fp.box("Important Message\nInside a fancy box!", color="bright_blue")

    print()

    # Gradient and rainbow
    fp.gradient("Gradient Text Effect", colors=["blue", "cyan", "green", "yellow"])
    fp.rainbow("Rainbow Text Effect!")

    print()

    # Progress bar
    import time

    for i in range(101):
        fp.progress(i, 100, color="bright_green")
        time.sleep(0.02)

    print("\n✨ Demo complete! ✨")


# Demo usage
if __name__ == "__main__":
    demo()
