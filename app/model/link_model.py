from SQLModel import SQLModel, Field

class Property_Amenities(SQLModel, table=True):
    property_id: int = Field(foreign_key="property.id", primary_key=True)
    amenities_id: int = Field(foreign_key="amenities.id", primary_key=True)


class Property_Object(SQLModel, table=True):
    property_id: int = Field(foreign_key="property.id", primary_key=True)
    object_id: int = Field(foreign_key="object.id", primary_key=True)


class Property_Nearby_Place(SQLModel, table=True):
    property_id: int = Field(foreign_key="property.id", primary_key=True)
    nearbyplace_id: int = Field(foreign_key="nearbyplace.id", primary_key=True)