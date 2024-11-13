import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    phone_number: str = Field(max_length=100, unique=True)
    status: int = Field(default=0)

    # Связь с контрактами
    contracts: List["Contract"] = Relationship(back_populates="customer")


class Contract(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date_b: datetime.date = Field(default=datetime.date.today)
    osmp: int = Field(default=0)
    customer_id: int = Field(foreign_key="customer.id")

    # Обратная связь с заказчиком
    customer: Optional[Customer] = Relationship(back_populates="contracts")
    # Связь с таблицей ContractToService
    services: List["ContractToService"] = Relationship(back_populates="contract")


class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)

    # Связь с таблицей ContractToService
    contract_to_services: List["ContractToService"] = Relationship(back_populates="service")


class ContractToService(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contract_id: int = Field(foreign_key="contract.id")
    service_id: int = Field(foreign_key="service.id")

    # Обратные связи для сервиса и контракта
    contract: Optional[Contract] = Relationship(back_populates="services")
    service: Optional[Service] = Relationship(back_populates="contract_to_services")


class City(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)

    # Связь с улицами
    streets: List["Street"] = Relationship(back_populates="city")


class Street(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    city_id: int = Field(foreign_key="city.id")

    # Обратная связь с городом
    city: Optional[City] = Relationship(back_populates="streets")


class Address(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    house: int = Field()
    frac: Optional[int] = Field(default=None)
    flat: Optional[int] = Field(default=None)
    street_id: int = Field(foreign_key="street.id")
    city_id: int = Field(foreign_key="city.id")

    # Связи с улицей и городом
    street: Optional[Street] = Relationship()
    city: Optional[City] = Relationship()


class Switchboard(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    ip: str = Field(max_length=30)
    address_id: int = Field(foreign_key="address.id")

    # Связь с адресом
    address: Optional[Address] = Relationship()


class Port(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    number: int = Field(default=0)
    name: str = Field(max_length=100)
    status_link: str = Field(max_length=100)
    switchboard_id: int = Field(foreign_key="switchboard.id")

    # Связь с коммутатором
    switchboard: Optional[Switchboard] = Relationship()

