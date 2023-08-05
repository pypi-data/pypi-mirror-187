from enum import Enum


class NetworksNames(str, Enum):
    AlastriaDefaultName = "Alastria"
    LacchainDefaultName = "Lacchain"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
