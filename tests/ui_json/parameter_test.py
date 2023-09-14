#  Copyright (c) 2023 Mira Geoscience Ltd.
#
#  This file is part of geoh5py.
#
#  geoh5py is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  geoh5py is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with geoh5py.  If not, see <https://www.gnu.org/licenses/>.


import pytest

from geoh5py.shared.exceptions import (
    TypeValidationError,
    UUIDValidationError,
    ValueValidationError,
)
from geoh5py.ui_json.parameters import (
    BoolParameter,
    FloatParameter,
    IntegerParameter,
    Parameter,
    RestrictedParameter,
    StringListParameter,
    StringParameter,
    UUIDParameter,
)

# pylint: disable=protected-access


def test_skip_validation_on_none_value():
    param = StringParameter("my_param", None)
    assert param.value is None


def test_parameter_validations_on_setting():
    param = StringParameter("my_param")
    param.value = "me"
    msg = "Type 'int' provided for 'my_param' is invalid. Must be: 'str'."
    with pytest.raises(TypeValidationError, match=msg):
        param.value = 1


def test_parameter_str_representation():
    param = Parameter("my_param")
    assert str(param) == "<Parameter> : 'my_param' -> None"


def test_restricted_parameter_construction():
    param = RestrictedParameter("my_param", ["a", "b", "c"])
    assert param.name == "my_param"
    assert param.value is None
    assert param._restrictions == ["a", "b", "c"]
    assert param.validations == {"value": ["a", "b", "c"]}


def test_restricted_parameter_validations():
    param = RestrictedParameter("my_param", ["a", "b", "c"])
    msg = "Value 'd' provided for 'my_param' is invalid. Must be one of: 'a', 'b', 'c'."
    with pytest.raises(ValueValidationError, match=msg):
        param.value = "d"
    param = RestrictedParameter("my_param", restrictions="a")
    msg = "Value 'b' provided for 'my_param' is invalid. Must be: 'a'."
    with pytest.raises(ValueValidationError, match=msg):
        param.value = "b"


def test_string_parameter_type_validation():
    param = StringParameter("my_param")
    msg = "Type 'int' provided for 'my_param' is invalid. "
    msg += "Must be: 'str'."
    with pytest.raises(TypeValidationError, match=msg):
        param.value = 1


def test_string_parameter_optional_validations():
    param = StringParameter("my_param")
    param.validations = {"types": [str]}
    param.value = None
    param.value = "this is ok"
    msg = "Type 'int' provided for 'my_param' is invalid. Must be: 'str'."
    with pytest.raises(TypeValidationError, match=msg):
        param.value = 1


def test_integer_parameter_type_validation():
    param = IntegerParameter("my_param")
    msg = "Type 'str' provided for 'my_param' is invalid. "
    msg += "Must be: 'int'."
    with pytest.raises(TypeValidationError, match=msg):
        param.value = "1"


def test_float_parameter_type_validation():
    param = FloatParameter("my_param")
    msg = "Type 'int' provided for 'my_param' is invalid. "
    msg += "Must be: 'float'."
    with pytest.raises(TypeValidationError, match=msg):
        param.value = 1


def test_bool_parameter_default():
    param = BoolParameter("my_param")
    assert param.value is False


def test_bool_parameter_type_validation():
    param = BoolParameter("my_param")
    msg = "Type 'str' provided for 'my_param' is invalid. "
    msg += "Must be: 'bool'."
    with pytest.raises(TypeValidationError, match=msg):
        param.value = "butwhy?"


def test_uuid_parameter_type_validation():
    param = UUIDParameter("my_param")
    msg = "Parameter 'my_param' with value 'notauuid' is not a valid uuid string."
    with pytest.raises(UUIDValidationError, match=msg):
        param.value = "notauuid"


def test_string_list_parameter_type_validation():
    param = StringListParameter("my_param")
    param.value = "this is ok"
    param.value = ["this", "is", "also", "ok"]
    msg = (
        "Type 'int' provided for 'my_param' is invalid. "
        "Must be one of: 'list', 'str'."
    )
    with pytest.raises(TypeValidationError, match=msg):
        param.value = 1
