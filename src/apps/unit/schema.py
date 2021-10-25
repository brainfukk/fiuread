from dataclasses import dataclass
from typing import Dict, List

TYPE_ALIASES = {
    str: "string",
    int: "integer",
    list: "array",
    dict: "dictionary",
}


@dataclass
class UnitExerciseElementAnswerDataSchema:
    """
    variants::Variants of answers
    answers::Correct answers in {0: 1} format
    """

    variants: List[str]
    answers: Dict[int, str]

    @classmethod
    def get_ref_schema(cls):
        result = {
            "title": "{} Schema".format(cls.__name__),
            "description": "{} configuration schema".format(cls.__name__),
            "type": "object",
            "properties": {},
        }
        desc_data = {
            desc_item.split("::")[0].strip(): desc_item.split("::")[1].strip()
            for desc_item in [item.strip() for item in cls.__doc__.strip().split("\n")]
        }
        for key, annotation in cls.__annotations__.items():
            if hasattr(annotation, "__origin__"):
                result["properties"][key] = {
                    "type": TYPE_ALIASES[annotation.__origin__],
                }
            else:
                result["properties"][key] = {"type": TYPE_ALIASES[annotation]}
            result["properties"][key]["description"] = desc_data[key]
        return result
