from pydantic import BaseModel, Filed
from enum import Enum


class ShipmentStatus(str, Enum): #str makes each enum member a string as well as an enum member.
    placed = "placed"
    transit = "in_transit"
    packed = "packed"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"





