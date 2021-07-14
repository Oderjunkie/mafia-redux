from rich.console import Console
console = Console()
consoleerr = Console(stderr=True)
print = console.log
printerr = consoleerr.log