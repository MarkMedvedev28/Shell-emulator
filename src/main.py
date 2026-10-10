"""Эмулятор командной оболочки UNIX-подобной ОС (вариант 22)."""

import argparse
import os
import re
import shlex
import sys

DEFAULT_VFS_NAME = "vfs"
MAX_EXIT_ARGS = 1
VAR_PATTERN = re.compile(r"\$(?:\{(\w+)\}|(\w+))")


class ShellError(Exception):
    """Ошибка выполнения команды, текст выводится пользователю."""


class ExitRequest(Exception):
    """Запрос на завершение эмулятора командой exit."""

    def __init__(self, code):
        """Сохраняет код завершения."""
        super().__init__(code)
        self.code = code


def expand_variables(line):
    """Раскрывает $VAR и ${VAR} значениями переменных окружения ОС."""
    def substitute(match):
        """Возвращает значение переменной или пустую строку."""
        return os.environ.get(match.group(1) or match.group(2), "")
    return VAR_PATTERN.sub(substitute, line)


def parse(line):
    """Раскрывает переменные и делит строку на слова с учётом кавычек."""
    try:
        return shlex.split(expand_variables(line), comments=True)
    except ValueError as error:
        raise ShellError(f"parse error: {error}") from error


def cmd_ls(args):
    """ls — заглушка: выводит имя команды и аргументы."""
    print("ls", args)


def cmd_cd(args):
    """cd — заглушка: выводит имя команды и аргументы."""
    print("cd", args)


def cmd_exit(args):
    """exit [N] — завершает эмулятор с кодом N (по умолчанию 0)."""
    if len(args) > MAX_EXIT_ARGS:
        raise ShellError("exit: too many arguments")
    if args and not args[0].isdigit():
        raise ShellError(f"exit: {args[0]}: numeric argument required")
    raise ExitRequest(int(args[0]) if args else 0)


COMMANDS = {"ls": cmd_ls, "cd": cmd_cd, "exit": cmd_exit}


def run_line(line):
    """Выполняет одну строку; при ошибке печатает её и возвращает False."""
    try:
        words = parse(line)
        if not words:
            return True
        command = COMMANDS.get(words[0])
        if command is None:
            raise ShellError(f"{words[0]}: command not found")
        command(words[1:])
    except ShellError as error:
        print(error)
        return False
    return True


def run_script(path, vfs_name):
    """Выполняет стартовый скрипт, показывая ввод и вывод.

    Строки, начинающиеся с #, — комментарии. При ошибке выполнение
    останавливается с сообщением о номере строки.
    """
    try:
        with open(path, encoding="utf-8") as file:
            lines = file.read().splitlines()
    except OSError as error:
        raise ShellError(f"cannot read script '{path}': "
                         f"{error.strerror}") from error
    for number, line in enumerate(lines, start=1):
        if not line.strip() or line.strip().startswith("#"):
            continue
        print(f"{vfs_name}$ {line}")
        if not run_line(line):
            raise ShellError(f"script error at {path}:{number}")


def parse_args(argv):
    """Разбирает параметры командной строки."""
    parser = argparse.ArgumentParser(description="Эмулятор оболочки UNIX")
    parser.add_argument("--vfs", help="путь к физическому расположению VFS")
    parser.add_argument("--script", help="путь к стартовому скрипту")
    return parser.parse_args(argv)


def vfs_name_of(path):
    """Имя VFS — имя каталога из пути или имя по умолчанию."""
    if not path:
        return DEFAULT_VFS_NAME
    return os.path.basename(os.path.normpath(path)) or DEFAULT_VFS_NAME


def repl(vfs_name):
    """Интерактивный цикл: приглашение, ввод, выполнение."""
    while True:
        try:
            line = input(f"{vfs_name}$ ")
        except EOFError:
            print()
            return
        run_line(line)


def main(argv=None):
    """Точка входа: печатает параметры, выполняет скрипт, запускает REPL."""
    options = parse_args(argv)
    vfs_name = vfs_name_of(options.vfs)
    print(f"[debug] vfs path = {options.vfs}")
    print(f"[debug] script   = {options.script}")
    print(f"[debug] vfs name = {vfs_name}")
    try:
        if options.script:
            run_script(options.script, vfs_name)
        repl(vfs_name)
    except ExitRequest as request:
        return request.code
    except ShellError as error:
        print(error)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
