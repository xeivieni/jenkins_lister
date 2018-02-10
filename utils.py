from terminaltables import AsciiTable

COLORS = {
    "red": "\033[1;31m",
    "blue": "\033[1;34m",
    "yellow": "\033[1;43m",
    "cyan": "\033[1;36m",
    "green": "\033[0;32m",
    "bold": "\033[;1m",
    "reverse": "\033[;7m",
    "reset": "\033[0;0m",
}


def format_data(data):
    table = AsciiTable(data)
    print(table.table)
