from pydantic import BeforeValidator
from typing import Annotated


PyObjectId = Annotated[str, BeforeValidator(str)]
