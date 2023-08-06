from dataclasses import dataclass


@dataclass
class SubmitResponse:
    upload: dict
    publish: dict
