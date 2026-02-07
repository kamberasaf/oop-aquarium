"""
Terminal utilities for interactive placement: clear screen and read single keypresses.
Works on Windows (msvcrt) and Unix (termios/tty).
"""

from __future__ import annotations

import sys

# Key result constants for clarity
KEY_LEFT = "left"
KEY_RIGHT = "right"
KEY_UP = "up"
KEY_DOWN = "down"
KEY_ENTER = "enter"
KEY_ESCAPE = "escape"


def clear_screen() -> None:
    """Clear the terminal screen (cross-platform)."""
    if sys.platform == "win32":
        import msvcrt
        # ANSI escape works in Windows 10+ ConHost and WT
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
    else:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()


def get_key() -> str | None:
    """
    Read a single keypress. Returns KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN,
    KEY_ENTER, KEY_ESCAPE, or None for other keys.
    """
    if sys.platform == "win32":
        return _get_key_windows()
    return _get_key_unix()


def _get_key_windows() -> str | None:
    import msvcrt
    ch = msvcrt.getch()
    if ch in (b"\r", b"\n"):
        return KEY_ENTER
    if ch == b"\x1b":  # ESC
        return KEY_ESCAPE
    if ch in (b"\xe0", b"\x00"):  # Arrow key prefix
        ch2 = msvcrt.getch()
        if ch2 == b"K":
            return KEY_LEFT
        if ch2 == b"M":
            return KEY_RIGHT
        if ch2 == b"H":
            return KEY_UP
        if ch2 == b"P":
            return KEY_DOWN
        return None
    # Single printable character (e.g. R, L, 0, 1)
    if len(ch) == 1 and 32 <= ch[0] < 127:
        return ch.decode("ascii").lower()
    return None


def _get_key_unix() -> str | None:
    import select
    import termios
    import tty
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\r" or ch == "\n":
            return KEY_ENTER
        if ch == "\x1b":
            # Escape: could be bare ESC or start of arrow sequence \x1b[A etc.
            if select.select([sys.stdin], [], [], 0.05)[0]:
                second = sys.stdin.read(1)
                if second == "[" and select.select([sys.stdin], [], [], 0.05)[0]:
                    seq = sys.stdin.read(1)
                    if seq == "A":
                        return KEY_UP
                    if seq == "B":
                        return KEY_DOWN
                    if seq == "C":
                        return KEY_RIGHT
                    if seq == "D":
                        return KEY_LEFT
            return KEY_ESCAPE
        # Single printable character
        if 32 <= ord(ch) < 127:
            return ch.lower()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return None


def flush_stdin() -> None:
    """Discard any remaining characters in stdin (e.g. after reading one key)."""
    if sys.platform == "win32":
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        import select
        while select.select([sys.stdin], [], [], 0)[0]:
            sys.stdin.read(1)


def try_get_key() -> str | None:
    """
    If a key is available, read and return it (same as get_key()). Otherwise return None immediately.
    Use this for non-blocking key checks (e.g. pause during demo).
    """
    if sys.platform == "win32":
        import msvcrt
        if not msvcrt.kbhit():
            return None
        return _get_key_windows()
    else:
        import select
        if not select.select([sys.stdin], [], [], 0)[0]:
            return None
        return _get_key_unix()
