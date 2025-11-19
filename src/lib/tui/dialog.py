import sys
import tty
import termios


def confirm(prompt="Continue?", default=True):
    """
    Display a modern inline confirmation prompt

    Args:
        prompt: The question to ask
        default: Default selection (True for Yes, False for No)

    Returns:
        True if Yes is selected, False if No is selected
    """
    # ANSI color codes
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    # YELLOW = "\033[93m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"
    REVERSE = "\033[7m"

    # Icons
    ARROW = "›"

    selected = 0 if default else 1

    # Save terminal settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)

        while True:
            # Clear line and move to start
            sys.stdout.write("\r\033[K")

            # Draw prompt
            sys.stdout.write(f"{CYAN}{ARROW}{RESET} {BOLD}{prompt}{RESET} ")

            # Draw Yes button
            if selected == 0:
                sys.stdout.write(f"{GREEN}{REVERSE}{BOLD} Yes {RESET} ")
            else:
                sys.stdout.write(f"{DIM}[Yes]{RESET} ")

            # Draw No button
            if selected == 1:
                sys.stdout.write(f"{RED}{REVERSE}{BOLD} No {RESET}")
            else:
                sys.stdout.write(f"{DIM}[No]{RESET}")

            sys.stdout.flush()

            # Read key
            char = sys.stdin.read(1)

            # Handle input
            if char == "\x03":  # Ctrl+C
                sys.stdout.write("\r\033[K")
                sys.stdout.write(f"{RED}{BOLD}✗ Interrupted{RESET}\n")
                sys.stdout.flush()
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                sys.exit(1)
            elif char == "\x1b":  # ESC or arrow key
                next1 = sys.stdin.read(1)
                if next1 == "[":
                    next2 = sys.stdin.read(1)
                    if next2 == "C":  # Right arrow
                        selected = 1
                    elif next2 == "D":  # Left arrow
                        selected = 0
                else:
                    # ESC key - exit
                    sys.stdout.write("\r\033[K")
                    sys.stdout.write(f"{RED}{BOLD}✗ Aborted{RESET}\n")
                    sys.stdout.flush()
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                    sys.exit(1)
            elif char == "\r" or char == "\n":  # Enter
                result = selected == 0
                sys.stdout.write("\r\033[K")
                if result:
                    sys.stdout.write(
                        f"{CYAN}{ARROW}{RESET} {prompt} {GREEN}{BOLD}✓ Yes{RESET}\n"
                    )
                else:
                    sys.stdout.write(
                        f"{CYAN}{ARROW}{RESET} {prompt} {RED}{BOLD}✗ No{RESET}\n"
                    )
                sys.stdout.flush()
                return result
            elif char.lower() == "y":
                sys.stdout.write("\r\033[K")
                sys.stdout.write(
                    f"{CYAN}{ARROW}{RESET} {prompt} {GREEN}{BOLD}✓ Yes{RESET}\n"
                )
                sys.stdout.flush()
                return True
            elif char.lower() == "n":
                sys.stdout.write("\r\033[K")
                sys.stdout.write(
                    f"{CYAN}{ARROW}{RESET} {prompt} {RED}{BOLD}✗ No{RESET}\n"
                )
                sys.stdout.flush()
                return False
            elif char == "\t":  # Tab
                selected = 1 - selected
            elif char == "h":  # Vim left
                selected = 0
            elif char == "l":  # Vim right
                selected = 1

    finally:
        # Restore terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.stdout.write("\033[G")
        sys.stdout.flush()
