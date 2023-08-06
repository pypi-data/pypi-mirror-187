import argparse
from datetime import datetime, date
from io import StringIO
import re
import os
from operator import attrgetter
import sys
import yaml
import logging

import rich
from rich.table import Table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from src.adapters.orm import metadata, start_mappers
from src.adapters.repository import SqlAlchemyRepository

from src.domain.commands import CommandHandler, Printer
from src.service_layer import services
from src.utils import format_task_dict


def init_db(home_dir):
    engine = create_engine(f"sqlite:////{home_dir}/.terka/tasks.db")
    metadata.create_all(engine)
    return engine


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?")
    parser.add_argument("entity", nargs="?")
    parser.add_argument("--log",
                        "--loglevel",
                        dest="loglevel",
                        default="info")
    args = parser.parse_known_args()
    args, kwargs = args

    home_dir = os.path.expanduser('~')
    logger = logging.getLogger(__name__)

    logging.basicConfig(
        format="[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
        # stream=sys.stdout,
        filename = "/home/am/.terka/terka.log",
        level=args.loglevel.upper(),
        datefmt="%Y-%m-%d %H:%M:%S")

    engine = init_db(home_dir)
    start_mappers()
    Session = sessionmaker(engine)
    with open(f"{home_dir}/.terka/config.yaml", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    task_id = config.get("task_id")
    project_name = config.get("project_name")
    if task_id or project_name:
        focus_type = "task" if task_id else "project"
        print("Using terka in focus mode")
        print(f"Current focus is {focus_type}: {task_id or project_name}")
    task_dict = format_task_dict(config, args, kwargs)
    with Session() as session:
        repo = SqlAlchemyRepository(session)
        printer =  Printer()
        command_handler = CommandHandler(repo)
        if (project := task_dict.get("project")):
            task_dict["project_id"] = services.lookup_project_id(project, repo)
            del task_dict["project"]
        if (assignee := task_dict.get("assignee")):
            task_dict["assignee"] = services.lookup_user_id(assignee, repo)
        if (due_date := task_dict.get("due_date")):
            task_dict["due_date"] = datetime.strptime(due_date, "%Y-%m-%d")
        logger.debug(task_dict)
        results, _, _ = command_handler.execute(args.command, args.entity, task_dict)
        printer.print(results)



if __name__ == "__main__":
    main()
