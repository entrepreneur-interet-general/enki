from typing import Literal, TypedDict, Union

vehicule_unavailable_status_options = [
    'departed_to_intervention',  
    'arrived_on_intervention', 
    'transport_to_hospital',
    'arrived_at_hospital', 
    'left_hospital', 
    'retrievable_within_15_minutes', # sport 
    'selected',  # présentation spontannée, sélection / instance de départ
    'waiting',  
    'broken',
    'lacks_staff', # manque personnel, omnibus
    'cancelled',
    'set_aside', # indispo délestage, indispo 1er départ
    'realocated', # monté en garde
    'undefined', # or unused
    'misc_unavailable'    
    ]
vehicule_available_status_options = [
    'arrived_at_home' ,
    'misc_available'
    ]
vehicule_status_options = vehicule_unavailable_status_options + vehicule_available_status_options
VehiculeStatus = Literal[vehicule_status_options]

vehicule_role_options = ['victim_rescue', 'pump', 'other']
VehiculeRole = Literal[vehicule_role_options]


class VehiculeEventData(TypedDict):
    raw_vehicule_id: int # 'Operation-Software'  vehicule ID 
    raw_intervention_id: Union[int, None] # 'Operation-Software'  intervention ID 
    status: VehiculeStatus
    is_available: bool
    raw_status: str # Status label from 'Operation-Software' 
    home_area: str # Reference on a partitioned map of where the vehicule belongs
    role: VehiculeRole
