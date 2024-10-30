import random 
import time
from dataclasses import dataclass
from typing import Tuple, Dict

@dataclass
class SensorConfig : 
    nombre: str
    unidad: str
    rango: Tuple[float, float]
    precision: int
    color: str
    limites_alarma: Dict[str, float]
