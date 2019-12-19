from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
import datetime
from threading import Thread
import json as Json
from typing import List, Dict


@dataclass_json
@dataclass
class Data:
    classes_index: List[int] = field(default_factory=list)
    classes_name: List[str] = field(default_factory=list)
    name_index: Dict[str, int] = field(default_factory=dict)
    index_name: Dict[int, str] = field(default_factory=dict)
    document_data: List[str] = field(default_factory=list)
    class_index_document_data: List[int] = field(default_factory=list)

    def add_classes(self, clas):
        for cl in clas:
            if cl not in self.classes_name:
                index = self.classes_index[-1] + 1 if self.classes_index else 0
                self.classes_name.append(cl)
                self.classes_index.append(index)
                self.name_index.update({cl: index})
                self.index_name.update({index: cl})

    def add_data(self, class_name_data, document_data):
        self.add_classes(class_name_data)
        if isinstance(class_name_data, list) and isinstance(
                document_data, list):
            for name, val in zip(class_name_data, document_data):
                self.document_data.append(val)
                self.class_index_document_data.append(self.name_index[name])
            return
        self.document_data.append(document_data)
        self.class_index_document_data.append(self.name_index[class_name_data])

    def save_to_json(self):
        Thread(
            target=self._save_to_json,
            args=(),
            name='Class to json').start()

    def _save_to_json(self):
        json = self.to_json()
        name = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(f'{name}.json', 'w') as f:
            f.write(json)
        return name

    @staticmethod
    def load_from_json(file_name):
        with open(file_name, 'r') as f:
            json = Json.load(f)
        return Data.from_dict(json)

    def __eq__(self, value):
        if isinstance(value, Data):
            return (self.classes_name == value.classes_name and self.name_index == value.name_index and self.document_data ==
                    value.document_data and self.class_index_document_data == value.class_index_document_data)
        return NotImplemented
