from dataclasses import dataclass, field
import numpy as np
from typing import List, Dict


@dataclass
class Data:
    classes_index: List[int] = field(default_factory=list)
    classes_name: List[str] = field(default_factory=list)
    name_index: Dict[str, int] = field(default_factory=dict)
    index_name: Dict[int, str] = field(default_factory=dict)
    document_data: List[str] = field(default_factory=list)
    class_index_document_data: np.uint16 = np.empty(0, dtype=np.uint16)

    def add_classes(self, classes: List[str]):
        index = len(self.classes_index) if len(self.classes_index) == 0 else 0
        for cl in classes:
            if cl not in self.classes_name:
                self.classes_name.append(cl)
                self.classes_index = np.append(self.classes_index, index)
                self.name_index.update({cl: index})
                self.index_name.update({index: cl})
                index += 1

    def add_data(self, class_name_data: List[str], document_data: List[str]):
        self.add_classes(class_name_data)
        self.document_data = self.document_data + document_data
        self.class_index_document_data = np.append(self.class_index_document_data, np.array(
            [self.name_index[name] for name in class_name_data], dtype=np.uint16))
