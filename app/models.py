from datetime import datetime
from pydantic import BaseModel, Field


class UserContext(BaseModel):
    user_id: str
    email: str | None = None
    name: str | None = None
    tenant_id: str | None = None

    scopes: set[str] = Field(default_factory=set)
    roles: set[str] = Field(default_factory=set)

    @property
    def permissions(self) -> set[str]:
        """
        Combine delegated scopes and application roles.

        Delegated user tokens usually contain scopes.
        Application/service tokens usually contain roles.
        """
        return self.scopes | self.roles


class Room(BaseModel):
    room_id: str
    name: str
    location: str
    capacity: int


class Booking(BaseModel):
    booking_id: str
    room_id: str
    user_id: str
    title: str
    start_time: datetime
    end_time: datetime
    attendees_count: int
