from pydantic import BaseModel, validator, root_validator
from typing import Optional, List, Dict, Tuple
from datetime import datetime



################################################################
## Most genaral description
################################################################
class Tes(BaseModel):
    '''
    Base classs to create sample before pushing the data to a MongoDB.
    It contains the general data structure
    '''
    
    tesName:            str
    tags:               Optional[List[str]]
    fabrication:        Optional[Dict]
    measurements:       Optional[List]
    calculatedData:     Optional[List]
    creationDate:       datetime = datetime.now()
    comments:           Optional[List]


    @validator('tesName')
    @classmethod
    def validate_SampleName(cls, value):
        if ' ' in value or value=='':
            raise NameError(value=value, message="A sample has to have a name and no blank spaces are allowed")
        return value

################################################################
## fabrication
################################################################
class Fabrication(BaseModel):
    '''
    General structure for a TES
    '''
    wafer:      Optional[Dict]
    absorber:   Optional[Dict]
    membrane:   Optional[Dict]
    pads:       Optional[Dict]
    stems:      Optional[Dict]
    stack:      Optional[Dict]

class Wafer(BaseModel):
    '''
    Wafer details
    '''
    waferName:      str
    material:       str
    orientation:    str
    maker:          Optional[str]  
    purchaseDate:   Optional[datetime]
    divisions:      Optional[List]
    chipsOnWafer:   Optional[List]
    comments:       Optional[str]

class Layer(BaseModel):
    '''
    Layer details
    '''
    material:           str
    orintation:         Optional[str]
    thickness:          float
    process:            str
    fabricationDetails: Optional[Dict]

class Stems(BaseModel):
    '''
    stems detais
    '''
    material:           str
    orintation:         Optional[str]
    type:               str
    process:            str
    fabricationDetails: Optional[Dict]

    @validator('type')
    @classmethod
    def validate_SampleName(cls, value):
        if value not in ['inner','outer']:
            raise NameError(value=value, message="The field type can only take the values inner or outer")
        return value
