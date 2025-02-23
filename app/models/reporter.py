from pydantic import BaseModel

class Reporter(BaseModel):
    """
    Represents a reporter with a name and organization.
    """
    name: str
    organization: str