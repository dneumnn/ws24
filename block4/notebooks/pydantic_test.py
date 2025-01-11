#see: 
# - https://towardsdatascience.com/pydantic-or-dataclasses-why-not-both-convert-between-them-ba382f0f9a9c
# - https://docs.pydantic.dev/latest/concepts/models/#dynamic-model-creation

print("start with a python dataclass")
from dataclasses import dataclass, field, fields

@dataclass
class User:
    name: str  = field(metadata={"title": 'Name', "description": "The name of the user."})
    age: int   = field(metadata={"title": 'Age', "description": "The age of the user."})

print("convert dataclass into pydantic model")
from pydantic import create_model, Field
field_kwargs = {}
for _field in fields(User):
    field_kwargs[_field.name] = (_field.type, Field(title=_field.metadata.get("title"), 
                                                    description=_field.metadata.get("description"))
                                )

dynamic_model = create_model(
    'PydanticUser',
    **field_kwargs,
)

print("get JSON schema out of pydantic model")
print(dynamic_model.model_json_schema())

