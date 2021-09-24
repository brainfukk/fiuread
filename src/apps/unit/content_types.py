import json
from dataclasses import asdict, dataclass
from typing import List


@dataclass
class BaseView:
    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict())


@dataclass
class ImageView(BaseView):
    source: str
    alt: str


@dataclass
class ListViewItem(BaseView):
    content: str


@dataclass
class ListView(BaseView):
    title: str
    items: List[ListViewItem]


@dataclass
class PlainTextView(BaseView):
    content: str


def load_content():
    pass
