from rich.console import Console
console = Console()
consoleerr = console
try:
    consoleerr = Console(stderr=True)
except TypeError:
    try:
        from sys import stderr
        consoleerr = Console(file=stderr)
    except Exception:
        pass
print = console.log
printerr = consoleerr.log