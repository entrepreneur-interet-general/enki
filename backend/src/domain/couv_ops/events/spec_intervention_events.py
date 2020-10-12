from typing import Literal, TypedDict

from pandas import Timestamp

intervention_cause_options = ['victim', 'fire', 'other']
InterventionCause = Literal[intervention_cause_options]
class InterventionEvent(TypedDict):
    timestamp: Timestamp
    ongoing: bool # True when intervention opens; False when intervention closes 
    raw_intervention_id: int # 'Operation-Software'  intervention ID 
    adresss: str
    area: str # Reference on a partitioned map 
    cause: InterventionCause
    raw_cause: str # Cause label from 'Operation-Software' (motif)