""""read_label_dict.py"""

from typing import Dict
from configparser import ConfigParser
from todoist_api_python.api_async import TodoistAPIAsync


async def read_label_dict(api: TodoistAPIAsync) -> Dict:
    """
    Read label list into dictionary
    """

    # Initialize label dictionary
    label_dict = {}

    # Get labels
    try:
        labels = await api.get_labels()
    except Exception as error:
        raise error

    # Construct label dictionary
    for label in labels:
        label_dict[label.id] = label

    return label_dict
