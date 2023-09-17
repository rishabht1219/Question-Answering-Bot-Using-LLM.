from pydantic import BaseModel, validator

class Item(BaseModel):
    text : str

    @validator('text')
    def input_text_must_be_string(cls, v):
        if type(v) != str:
            raise ValueError('must be a string')
        return v

class ResponseModel(BaseModel):
    text : str = ''
    summary : str = ''
    url : str = ''
    first_link : str = ''