"""
Module for formatting Python files

:author: Julian M. Kleber
"""
import os
import re
import subprocess


import click

from prettify_py.split_line_cutoff import format_file_line_length


@click.group()
def format_py() -> None:
    """
    The cli function is the entry point for the command line interface.

    It should not contain any logic that would be better
    placed in a separate function or class method. The cli function is also where you
    should call click's `click.command()` decorator to define your CLI's options and help text.

    :return: None.

    :doc-author: Julian M. Kleber
    """

    pass


@click.command()
@click.argument("file_name")
@click.option("-n", default=100, help="Number of symbols")
def format_file(file_name: str, n: int) -> None:
    """
    The format_file function takes a file name and an integer n as input.
    It then formats the file by removing all white space at the end of each line,
    and then reformats it so that no line is longer than n characters.
    The function also removes any trailing whitespace from lines in the file.

    :param file_name:str: Used to Specify the name of the file to be formatted.
    :param n:int: Used to Specify the cutoff for line length.
    :return: None.

    :doc-author: Trelent
    """

    file_name, file_extension = os.path.splitext(file_name)
    base_formatting(dir_name=file_name)
    remove_white_space_file(
        dir_name="./", file_name=file_name, suffix=file_extension)

    format_file_line_length(file_name=file_name + file_extension, cutoff=n)
    remove_white_space_file(
        dir_name="./", file_name=file_name, suffix=file_extension)

    subprocess.run(["docformatter", file_name + file_extension])


@click.command()
@click.argument("dir_name")
@click.option("-n", default=100, help="Number of symbols")
def format_dir(dir_name: str, n: int) -> None:
    """
    The format function is a wrapper for the format_docstrings and strip_whitespace functions.

    It takes in a string, d, which is the name of the directory containing all of your Python files.
    The function then calls both format_docstrings and strip_whitespace
    on each file in that directory.

    :param d:str: Used to Pass the docstring to the function.
    :return: None.

    :doc-author: Trelent
    """

    base_formatting(dir_name=dir_name)
    strip_whitespace(dir_name=dir_name)
    format_line_len_dir(dir_name=dir_name, cutoff=n)
    format_docstrings(dir_name=dir_name)


def format_line_len_dir(dir_name: str, cutoff: int) -> None:
    """
    The format_line_len_dir function takes a directory name and a cutoff value as input.
    It then finds all the .py files in that directory, and calls the format_file_line_
    length function on each of them.

    :param dir_name:str: Used to Specify the directory name.
    :param cutoff:int: Used to Specify the number of characters that a line should not exceed.
    :return: None.

    :doc-author: Trelent
    """

    dir_content = os.listdir(dir_name)
    py_files = [x for x in dir_content if x.endswith(".py")]
    for py_f in py_files:
        format_file_line_length(file_name=dir_name + py_f, cutoff=cutoff)


def format_docstrings(dir_name: str) -> None:
    """
    The format_docstrings function takes a directory as an argument and
    formats all the docstrings in that directory.

    It does this by running the pydocstyle command on each file in the
    given directory, and then writing to a text file
    called "docstring_errors.txt" which contains any errors
    found by docformatter.

    :param f:str: Used to Specify the file name and the ->none parameter is used
                  to specify that no output will be returned.
    :return: A list of the docstrings in each python file.

    :doc-author: Trelent
    """

    dir_content = os.listdir(dir_name)
    py_files = [x for x in dir_content if x.endswith(".py")]
    for py_f in py_files:
        subprocess.run(["docformatter", dir_name + py_f, "-i"])


def strip_whitespace(dir_name: str) -> None:
    """
    The format function takes a file path as an argument and recursively
    walks through the directory structure, looking for Python files.  When it
    finds one, it opens the file and strips trailing whitespace from each line.

    :param f:str: Used to Specify the file path of the directory you want to format.
    :return: None.

    :doc-author: Julian M. Kleber
    """

    for path, dirs, files in os.walk(dir_name):
        for f in files:
            file_name, file_extension = os.path.splitext(f)
            if file_extension == ".py":
                remove_white_space_file(
                    suffix=file_extension, file_name=file_name, dir_name=dir_name
                )


def remove_white_space_file(file_name: str, suffix: str, dir_name: str = "") -> None:
    """
    The remove_white_space_file function removes all white space from a file.

    It takes in the name of a file as an argument and returns None.

    :param file_name:str: Used to Specify the file name of the file you want
                          to remove white space from.
    :param dir_name:str: Used to Specify the dir name of the file you want
                        to remove white space from.
    :return: None.

    :doc-author: Trelent
    """
    re_strip = re.compile(r"[ \t]+(\n|\Z)")
    file_name = file_name + suffix
    path_name = os.path.join(dir_name, file_name)
    with open(path_name, "rb") as f:
        data = f.read().decode("UTF-8")
    data = re_strip.sub(r"\1", data)

    with open(path_name, "w", encoding="UTF-8") as f:
        f.write(data)


def base_formatting(dir_name: str) -> None:
    """
    The base_formatting function takes a directory name as an argument and runs the black formatter on all files in that directory.

    :param dir_name:str: Used to Specify the directory that you want to format.
    :return: None.

    :doc-author: Trelent
    """

    subprocess.run(["black", dir_name])


# Register commands

format_py.add_command(format_dir)
format_py.add_command(format_file)

if __name__ == "__main__":
    format_py()
