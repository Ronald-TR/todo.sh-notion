import argparse

from notion.client import NotionClient
from settings import TASK_LIST_URL, TOKEN_V2

client = NotionClient(token_v2=TOKEN_V2)
page = client.get_collection_view(TASK_LIST_URL)


def add(task: str) -> None:
    """Create a task in To Do
    Task List

    Parameters
    ----------
    task : str
        Card title
    """
    row = page.collection.add_row()
    row.title = task
    row.status = "To Do"


def done(task: str) -> None:
    """Move all the tasks that have the "task" name into their titles to Done

    Parameters
    ----------
    task : str
        Card title
    """
    for row in page.collection.get_rows(search=task):
        row.status = "Done"


def delete(task: str) -> None:
    """Like "done" command, but performs a delete action.
    Delete all the tasks that have the "task" name into their titles

    Parameters
    ----------
    task : str
        Card title
    """
    for row in page.collection.get_rows(search=task):
        row.remove()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage cards in Notion task list")
    subparsers = parser.add_subparsers(title="actions")

    parser_add = subparsers.add_parser(
        "add", add_help=False, help="Add a task in To Do"
    )
    parser_add.add_argument("task")
    parser_add.set_defaults(func=delete)

    parser_done = subparsers.add_parser(
        "done", add_help=False, help="Mark the task as Done"
    )
    parser_done.add_argument("task")
    parser_done.set_defaults(func=delete)

    parser_delete = subparsers.add_parser(
        "delete", add_help=False, help="Delete the task"
    )
    parser_delete.add_argument("task")
    parser_delete.set_defaults(func=delete)

    argx = parser.parse_args()
    argx.func(argx.task)
