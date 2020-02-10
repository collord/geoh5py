import uuid
from typing import List, Union

from geoh5io.data import DataAssociationEnum
from geoh5io.shared import Entity


class PropertyGroup:
    """ Group for properties"""

    _attribute_map = {
        "Association": "association",
        "Group Name": "group_name",
        "ID": "uid",
        "Properties": "properties",
        "Property Group Type": "property_group_type",
    }

    def __init__(self, **kwargs):

        self._group_name = "prop_group"
        self._uid = uuid.uuid4()
        self._association: DataAssociationEnum = DataAssociationEnum.VERTEX
        self._properties: List[uuid.UUID] = []
        self._property_group_type = "multi-element"
        self._parent = None

        for attr, item in kwargs.items():
            try:
                if attr in self._attribute_map.keys():
                    attr = self._attribute_map[attr]
                setattr(self, attr, item)
            except AttributeError:
                continue

    @property
    def parent(self) -> Entity:
        return self._parent

    @parent.setter
    def parent(self, parent):
        """
        The parent of an object in the workspace
        :return: Entity: Parent entity
        """
        if isinstance(parent, Entity):
            parent = parent.uid

        self._parent = parent

    @property
    def attribute_map(self):
        return self._attribute_map

    @property
    def uid(self) -> uuid.UUID:
        return self._uid

    @uid.setter
    def uid(self, uid: Union[str, uuid.UUID]):
        if isinstance(uid, str):
            uid = uuid.UUID(uid)
        self._uid = uid

    @property
    def group_name(self) -> str:
        return self._group_name

    @group_name.setter
    def group_name(self, new_group_name: str):
        self._group_name = new_group_name

    @property
    def association(self) -> DataAssociationEnum:
        return self._association

    @association.setter
    def association(self, value):
        if self._association is None:

            if isinstance(value, str):
                value = getattr(DataAssociationEnum, value.upper())

            assert isinstance(
                value, DataAssociationEnum
            ), f"Association must be of type {DataAssociationEnum}"
            self._association = value

    @property
    def properties(self) -> List[uuid.UUID]:
        return self._properties

    @properties.setter
    def properties(self, uids: List[Union[str, uuid.UUID]]):

        properties = []
        for uid in uids:
            if isinstance(uid, str):
                uid = uuid.UUID(uid)
            properties.append(uid)
        self._properties += properties

    @property
    def property_group_type(self) -> str:
        return self._property_group_type

    @property_group_type.setter
    def property_group_type(self, group_type: str):
        self._property_group_type = group_type
