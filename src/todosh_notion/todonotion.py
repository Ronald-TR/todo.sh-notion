import argparse
import os
import shutil
from argparse import Namespace
from pathlib import Path

from notion.client import NotionClient

from todosh_notion.settings import TASK_LIST_URL, TOKEN_V2


def add(arg: Namespace) -> None:
    """Create a task in To Do
    Task List

    Parameters
    ----------
    arg : Namespace
        Arg with card title
    """
    client = NotionClient(token_v2=TOKEN_V2)
    page = client.get_collection_view(TASK_LIST_URL)

    row = page.collection.add_row()
    row.title = arg.title
    row.status = "To Do"


def done(arg: Namespace) -> None:
    """Move all the tasks that have the "task" name into their titles to Done

    Parameters
    ----------
    arg : Namespace
        Arg with card title
    """
    client = NotionClient(token_v2=TOKEN_V2)
    page = client.get_collection_view(TASK_LIST_URL)

    for row in page.collection.get_rows(search=arg.title):
        row.status = "Done"


def delete(arg: Namespace) -> None:
    """Like "done" command, but performs a delete action.
    Delete all the tasks that have the "task" name into their titles

    Parameters
    ----------
    arg : Namespace
        Arg with card title
    """
    client = NotionClient(token_v2=TOKEN_V2)
    page = client.get_collection_view(TASK_LIST_URL)

    for row in page.collection.get_rows(search=arg.title):
        row.remove()


def configure(arg: Namespace):
    """Configure todo.sh actions
    Add the actions in ~/.todo.actions.d, create the directory if not exists
    As explained in:
    github.com/todotxt/todo.txt-cli/wiki/Creating-and-Installing-Add-ons

    Parameters
    ----------
    arg : Namespace
    """
    actions_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "actions")
    dest_path = os.path.join(str(Path().home()), ".todo.actions.d")
    os.makedirs(dest_path, exist_ok=True)
    for action in os.listdir(actions_dir):
        abs_action = os.path.join(actions_dir, action)
        if os.path.isfile(abs_action) and not os.path.splitext(action)[-1]:
            shutil.copy(abs_action, dest_path)
    os.system(f"chmod +x {dest_path}/*")


def run():
    parser = argparse.ArgumentParser(description="Manage cards in Notion task list")
    subparsers = parser.add_subparsers(title="actions")

    parser_add = subparsers.add_parser(
        "add", add_help=False, help="Add a task in To Do"
    )
    parser_add.add_argument("title")
    parser_add.set_defaults(func=delete)

    parser_done = subparsers.add_parser(
        "done", add_help=False, help="Mark the task as Done"
    )
    parser_done.add_argument("title")
    parser_done.set_defaults(func=delete)

    parser_delete = subparsers.add_parser(
        "delete", add_help=False, help="Delete the task"
    )

    parser_delete.add_argument("title")
    parser_delete.set_defaults(func=delete)

    parser_configure = subparsers.add_parser(
        "configure", add_help=False, help="Configure todo.sh actions"
    )
    parser_configure.set_defaults(func=configure)

    argx = parser.parse_args()
    argx.func(argx)


if __name__ == "__main__":
    run()
