from pydantic import BaseModel, Field, computed_field, field_validator
from typing import List, Annotated, Literal, Set, Optional

class Review(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    comment: str

AllowedTags = Literal['beauty', 'furniture', 'grocery', 'appliances']

class Product(BaseModel):
    id: int = Field(..., gt=0) # Required field
    title: Annotated[Optional[str], Field(default=None)] # Optional field
    description: Optional[str] = Field(default=None, description='Product description.')
    category: Annotated[Optional[str], Field(default=None)]
    price: Annotated[Optional[float], Field(default=None, gt=0)]
    rating: Annotated[Optional[float], Field(default=None, gt=0, max=5)]
    stock: Annotated[Optional[int], Field(default=0)]
    discountPercentage: Annotated[Optional[float], Field(default=None)]
    tags: Annotated[Set[AllowedTags], Field(...)]
    reviews: List[Review]

    @computed_field
    @property
    def finalPrice(self) -> float:
        return self.price - (self.price * self.discountPercentage) / 100
    
    @field_validator('discountPercentage') # This decorator links the function to the specific field discountPercentage
    @classmethod #Validators within Pydantic models must be class methods
    def validate_discount_percentage(cls, value: float) -> float:
        if value < 0:
            raise ValueError('Discount percentage cannot be a negative value.')
        return value
    
