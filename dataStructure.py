from pydantic import BaseModel, validator, root_validator
from typing import Optional, List, Dict, Tuple
from datetime import datetime
import re

################################################################
## Errores
################################################################

class NameError(Exception):
    '''Exception raised when validation string is invalid'''

    def __init__(self, value:str, message:str) ->None:
        self.value = value
        self.message = message
        super().__init__(message)

class UnitMissingError(Exception):
    '''Exception raised when a vulue is given but not the units'''

    def __init__(self, values:dict, message:str) ->None:
        self.values = values
        self.message = message
        super().__init__(message)

class ErrorMissingError(Exception):
    '''Exception raised when a value is given but no error is provided '''
    def __init__(self, values:dict, message:str) ->None:
        self.values = values
        self.message = message
        super().__init__(message)

class DlimiterNumberError(Exception):
    '''Exception raised when incorrect number of delimiter'''

    def __init__(self, value:int, message:str) ->None:
        self.value = value
        self.message = message
        super().__init__(message)
class WrongDateFormat(Exception):
    '''Exception raised when incorrect number of delimiter'''

    def __init__(self, value:int, message:str) ->None:
        self.value = value
        self.message = message
        super().__init__(message)
class MultitransError(Exception):
    '''Exception raised when incorrect Multitransition value'''

    def __init__(self, value:str, message:str) ->None:
        self.value = value
        self.message = message
        super().__init__(message)


################################################################
## Values and units
################################################################

class PairValueUnit(BaseModel):
    quantity:   Optional[float] = None
    units:      Optional[str] = None

    @root_validator(pre = True)
    @classmethod
    def checkForUnits(cls, values:Dict)->Dict:
        valueToCheck = values.get('quantity')
        unitToCheck = values.get('units')
        if valueToCheck!=None and unitToCheck==None:
            raise UnitMissingError(values = values, message="A measure has to have units")
        return values

class PairValueUnitCom(BaseModel):
    quantity:   Optional[list[float]] = None
    units:      Optional[str] = None
    comments:   Optional[List[str]] 

    @root_validator(pre = True)
    @classmethod
    def checkForUnits(cls, values:Dict)->Dict:
        valueToCheck = values.get('quantity')
        unitToCheck = values.get('units')
        if valueToCheck!=None and unitToCheck==None:
            raise UnitMissingError(values = values, message="A measure has to have units")
        return values

class MagnitudError(BaseModel):
    quantity: Optional[float] = None
    error: Optional[float] = None
    units : Optional[str] = None
    @root_validator(pre = True)
    @classmethod
    def checkForUnits(cls, values:Dict)->Dict:
        valueToCheck = values.get('quantity')
        unitToCheck = values.get('units')
        errorToCheck = values.get('error')
        if valueToCheck!=None and unitToCheck==None:
            raise UnitMissingError(values = values, message="A measure has to have units")
        if valueToCheck!=None and errorToCheck==None:
            raise ErrorMissingError(values = values, message="A measure has to have an error")
        return values


class PairListValueUnit(BaseModel):
    quantity:   Optional[List[float]] = []
    units:      Optional[str] = None

    @root_validator(pre = True)
    @classmethod
    def checkForUnits(cls, values:Dict)->Dict:
        valueToCheck = values.get('quantity')
        unitToCheck = values.get('units')
        if valueToCheck!=[] and unitToCheck==None:
            raise UnitMissingError(values = values, message="A measure has to have units")
        return values



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
    wafer:          Optional[Dict]
    absorber:       Optional[List]
    membrane:       Optional[Dict]
    pads:           Optional[List]
    stems:          Optional[Dict]
    stack:          Optional[List]
    place:          str = 'INMA'
    startingDate:   Optional[datetime]
    endingDate:     Optional[datetime]


    @validator('startingDate', pre = True)
    @classmethod
    def dateFormated(cls,value:str)->datetime:
        delimiter = re.findall(r'\D', value)
        vd = delimiter[0]
        if len(delimiter)!=2:
            raise DlimiterNumberError(value, 'Error in date delimiter')
        else:
            dateFormat=f'%Y{vd}%m{vd}%d'
        if int(value.split(vd)[0])<2000:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if int(value.split(vd)[1])>12:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if len(delimiter)==2:
            if delimiter[0]!=delimiter[1]:
                raise DlimiterNumberError(value, 'Error in date delimiter')
        value = datetime.combine(datetime.strptime(value, dateFormat),datetime.min.time())
        return value


    @validator('endingDate', pre = True, allow_reuse=True)
    @classmethod
    def dateFormated(cls,value:str)->datetime:
        delimiter = re.findall(r'\D', value)
        vd = delimiter[0]
        if len(delimiter)!=2:
            raise DlimiterNumberError(value, 'Error in date delimiter')
        else:
            dateFormat=f'%Y{vd}%m{vd}%d'
        if int(value.split(vd)[0])<2000:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if int(value.split(vd)[1])>12:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if len(delimiter)==2:
            if delimiter[0]!=delimiter[1]:
                raise DlimiterNumberError(value, 'Error in date delimiter')
        value = datetime.combine(datetime.strptime(value, dateFormat),datetime.min.time())
        return value

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
    image:          Optional[str]
    comments:       Optional[str]


    @validator('purchaseDate', pre = True)
    @classmethod
    def dateFormated(cls,value:str)->datetime:
        delimiter = re.findall(r'\D', value)
        vd = delimiter[0]
        if len(delimiter)!=2:
            raise DlimiterNumberError(value, 'Error in date delimiter')
        else:
            dateFormat=f'%Y{vd}%m{vd}%d'
        if int(value.split(vd)[0])<2000:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if int(value.split(vd)[1])>12:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if len(delimiter)==2:
            if delimiter[0]!=delimiter[1]:
                raise DlimiterNumberError(value, 'Error in date delimiter')
        value = datetime.combine(datetime.strptime(value, dateFormat),datetime.min.time())
        return value

class Layer(BaseModel):
    '''
    Layer details
    '''
    material:           str
    orintation:         Optional[str]
    thickness:          Optional[PairValueUnit]
    width:              Optional[PairValueUnit]
    length:             Optional[PairValueUnit]
    process:            str
    fabricationDetails: Optional[Dict]
    fabricationDate:    Optional[datetime]

    @validator('fabricationDate', pre = True)
    @classmethod
    def dateFormated(cls,value:str)->datetime:
        delimiter = re.findall(r'\D', value)
        vd = delimiter[0]
        if len(delimiter)!=2:
            raise DlimiterNumberError(value, 'Error in date delimiter')
        else:
            dateFormat=f'%Y{vd}%m{vd}%d'
        if int(value.split(vd)[0])<2000:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if int(value.split(vd)[1])>12:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if len(delimiter)==2:
            if delimiter[0]!=delimiter[1]:
                raise DlimiterNumberError(value, 'Error in date delimiter')
        value = datetime.combine(datetime.strptime(value, dateFormat),datetime.min.time())
        return value

class Stems(BaseModel):
    '''
    stems detais
    '''
    material:           str
    orintation:         Optional[str]
    type:               str
    width:              Optional[PairValueUnit]
    long:               Optional[PairValueUnit]
    height:             Optional[PairValueUnit]
    process:            str
    fabricationDetails: Optional[Dict]
    fabricationDate:    Optional[datetime]

    @validator('type')
    @classmethod
    def validate_SampleName(cls, value):
        if value not in ['inner','outer']:
            raise NameError(value=value, message="The field type can only take the values inner or outer")
        return value

    @validator('fabricationDate', pre = True)
    @classmethod
    def dateFormated(cls,value:str)->datetime:
        delimiter = re.findall(r'\D', value)
        vd = delimiter[0]
        if len(delimiter)!=2:
            raise DlimiterNumberError(value, 'Error in date delimiter')
        else:
            dateFormat=f'%Y{vd}%m{vd}%d'
        if int(value.split(vd)[0])<2000:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if int(value.split(vd)[1])>12:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if len(delimiter)==2:
            if delimiter[0]!=delimiter[1]:
                raise DlimiterNumberError(value, 'Error in date delimiter')
        value = datetime.combine(datetime.strptime(value, dateFormat),datetime.min.time())
        return value

class Pads(BaseModel):
    '''
    Layer details
    '''
    material:           str
    orintation:         Optional[str]
    thickness:          Optional[PairValueUnit]
    shape:              Optional[Dict]
    process:            str
    fabricationDetails: Optional[Dict]
    fabricationDate:    Optional[datetime]


    @validator('fabricationDate', pre = True)
    @classmethod
    def dateFormated(cls,value:str)->datetime:
        delimiter = re.findall(r'\D', value)
        vd = delimiter[0]
        if len(delimiter)!=2:
            raise DlimiterNumberError(value, 'Error in date delimiter')
        else:
            dateFormat=f'%Y{vd}%m{vd}%d'
        if int(value.split(vd)[0])<2000:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if int(value.split(vd)[1])>12:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if len(delimiter)==2:
            if delimiter[0]!=delimiter[1]:
                raise DlimiterNumberError(value, 'Error in date delimiter')
        value = datetime.combine(datetime.strptime(value, dateFormat),datetime.min.time())
        return value

class ShapePads(BaseModel):
    '''
    Shape definition
    '''
    image:              Optional[str]
    parameter_X:        Optional[PairValueUnit]
    parameter_h:        Optional[PairValueUnit]
    parameter_Y:        Optional[PairValueUnit]
    parameter_H:        Optional[PairValueUnit]
    parameter_D:        Optional[PairValueUnit]

################################################################
## fabrication processes
################################################################

class AnnealingProfile(BaseModel):
    steps:          Optional[int] = None
    temperature:    Optional[PairValueUnit]
    time:           Optional[PairValueUnit]

class Annealing(BaseModel):
    type:       Optional[str] = 'NA'
    ramp:       Optional[str] = 'NA'
    profile:    Optional[List[AnnealingProfile]]


class FabricationPresure(BaseModel):
    atmosphere: Optional[str] = 'ar'
    type:       Optional[str] = "pressure"
    quantity:   Optional[float] = None
    units:      Optional[str] = None

    @root_validator()
    @classmethod
    def checkForUnits(cls, values:Dict) -> Dict:
        valueToCheck = values.get('quantity')
        unitToCheck = values.get('units')
        if valueToCheck!=None and unitToCheck==None:
            raise UnitMissingError(values = values, message="A measure has to have units")
        return values

class Sputtering(BaseModel):

    method:                 str = 'dc-sputtering'
    annealing:              Optional[Annealing]
    chamberName:            Optional[str]
    chamberConfiguration:   Optional[str]
    basePresure:            Optional[PairValueUnit]
    fabricationPresure:     Optional[FabricationPresure]
    fabricationPower:       Optional[PairValueUnit]
    fabricationDCVias:      Optional[PairValueUnit]
    fabricationIDC:         Optional[PairValueUnit]
    depositionRate:         Optional[PairValueUnit]
    place:                  str
    fabricationDate:        datetime

    @validator('fabricationDate', pre = True)
    @classmethod
    def dateFormated(cls,value:str)->datetime:
        delimiter = re.findall(r'\D', value)
        vd = delimiter[0]
        if len(delimiter)!=2:
            raise DlimiterNumberError(value, 'Error in date delimiter')
        else:
            dateFormat=f'%Y{vd}%m{vd}%d'
        if int(value.split(vd)[0])<2000:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if int(value.split(vd)[1])>12:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if len(delimiter)==2:
            if delimiter[0]!=delimiter[1]:
                raise DlimiterNumberError(value, 'Error in date delimiter')
        value = datetime.combine(datetime.strptime(value, dateFormat),datetime.min.time())
        return value

class EbeamEvaporation(BaseModel):
    place: str
    fabricationDate: Optional[datetime]

    @validator('fabricationDate', pre = True)
    @classmethod
    def dateFormated(cls,value:str)->datetime:
        delimiter = re.findall(r'\D', value)
        vd = delimiter[0]
        if len(delimiter)!=2:
            raise DlimiterNumberError(value, 'Error in date delimiter')
        else:
            dateFormat=f'%Y{vd}%m{vd}%d'
        if int(value.split(vd)[0])<2000:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if int(value.split(vd)[1])>12:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if len(delimiter)==2:
            if delimiter[0]!=delimiter[1]:
                raise DlimiterNumberError(value, 'Error in date delimiter')
        value = datetime.combine(datetime.strptime(value, dateFormat),datetime.min.time())
        return value

class Electroplating(BaseModel):
    place: str
    fabricationDate: Optional[datetime]
    @validator('fabricationDate', pre = True)
    @classmethod
    def dateFormated(cls,value:str)->datetime:
        delimiter = re.findall(r'\D', value)
        vd = delimiter[0]
        if len(delimiter)!=2:
            raise DlimiterNumberError(value, 'Error in date delimiter')
        else:
            dateFormat=f'%Y{vd}%m{vd}%d'
        if int(value.split(vd)[0])<2000:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if int(value.split(vd)[1])>12:
            raise WrongDateFormat(value,'Appropiate date format YYYY-MM-DD')
        if len(delimiter)==2:
            if delimiter[0]!=delimiter[1]:
                raise DlimiterNumberError(value, 'Error in date delimiter')
        value = datetime.combine(datetime.strptime(value, dateFormat),datetime.min.time())
        return value

################################################################
## Measured data
################################################################
class MeasTypeGeneral(BaseModel):
    xrd:        Optional[List]
    transport:  Optional[List]


class TCmeas(BaseModel):
    fromFile:       str
    cryostat:       str
    holder:         str
    primaryType:    str
    secondaryType:  str
    current:        float
    reentrant:      str
    data:           Optional[List[PairListValueUnit]]
    date:           Optional[datetime]
    place:          Optional[str] = 'INMA'
    comments:       Optional[List[str]]

    @validator('primaryType', pre = True)
    @classmethod
    def check_str(cls,value:str)->str:
        if value not in ['normal', 'double', 'probable', 'tail', 'no tc', 're-entring']:
            raise MultitransError(value,'primaryType can only take values'\
                + 'normal, double, probable, tail, no tc, re-entring')
        return value
    @validator('secondaryType', pre = True)
    @classmethod
    def check_str_(cls,value:str)->str:
        if value not in ['round','straight']:
            raise MultitransError(value,'secondaryType can only take values round and straight')
        return value


################################################################
## Calculated data
################################################################

class MeasRN(BaseModel):
    resistance:     float
    temperature:    float
    percentage:     float


class TcDescription(BaseModel):
    fromFile:       Optional[str]
    fromCurrent:    Optional[PairValueUnit]
    RN:             Optional[List[MeasRN]]

class FormFactor(BaseModel):
    '''
    Calculated data from shape
    '''
    area:       Optional[PairValueUnit]
    perimeter:  Optional[PairValueUnit]
    aspectRatio:Optional[PairValueUnit]

class Transport(BaseModel):
    '''
    Calculated data from transport measurements
    '''

    sheetResistance: Optional[PairValueUnit]
    minCurrent:      Optional[PairValueUnitCom]
    tcDescription:   Optional[List]

class CalculatedData(BaseModel):
    '''
    General structure
    '''
    formFactors: Optional[FormFactor]
    transport:   Optional[List]






