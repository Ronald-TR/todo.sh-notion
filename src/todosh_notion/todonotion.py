import argparse

from notion.client import NotionClient

from todosh_notion.settings import TASK_LIST_URL, TOKEN_V2

client = NotionClient(token_v2=TOKEN_V2)
page = client.get_collection_view(TASK_LIST_URL)


def add(text):
    row = page.collection.add_row()
    row.title = text
    row.status = "To Do"


def done(text):
    for row in page.collection.get_rows(search=text):
        row.status = "Done"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage cards into Notion task list")
    parser.add_argument("add", help="Add a task in To Do")
    parser.add_argument("done", help="Mark the task as Done")
