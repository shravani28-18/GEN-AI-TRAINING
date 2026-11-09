from dataclasses import dataclass


@dataclass
class Record:

    topic: str
    animal_type: str
    recommendation: str
    quantity_or_schedule: str
    source_doc: str
    source_url: str