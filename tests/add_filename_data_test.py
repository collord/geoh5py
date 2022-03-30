#  Copyright (c) 2022 Mira Geoscience Ltd.
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

import os
from io import BytesIO

import numpy as np
import pytest

from geoh5py.data import Data
from geoh5py.groups import ContainerGroup
from geoh5py.objects import Curve
from geoh5py.shared.utils import compare_entities
from geoh5py.workspace import Workspace


def test_add_file(tmp_path):
    workspace = Workspace(os.path.join(tmp_path, "testProject.geoh5"))
    workspace_copy = Workspace(os.path.join(tmp_path, "testProject_B.geoh5"))
    curve = Curve.create(workspace)
    group = ContainerGroup.create(workspace)
    data = curve.add_data({"ABC": {"values": "axs"}})

    xyz = np.random.randn(32)
    np.savetxt(os.path.join(tmp_path, "numpy_array.txt"), xyz)
    file_name = "numpy_array.txt"
    for obj in [data, curve, group]:
        try:
            file_data = obj.add_file(os.path.join(tmp_path, file_name))
        except NotImplementedError:
            assert isinstance(
                obj, Data
            ), "Only Data should return 'NotImplementedError'"
            continue

        assert file_data.file_name == file_name, "File_name not properly set."
        # Rename the file locally and write back out
        file_data.file_name = "numpy_array.dat"
        file_data.save(tmp_path)
        assert os.path.exists(
            os.path.join(tmp_path, file_data.file_name)
        ), f"Input path '{os.path.join(tmp_path, file_data.file_name)}' does not exist."
        workspace.finalize()
        new_xyz = np.loadtxt(os.path.join(tmp_path, "numpy_array.dat"))
        xyz_bytes = np.loadtxt(BytesIO(file_data.values))
        np.testing.assert_array_equal(
            new_xyz, xyz_bytes, err_msg="Loaded and stored bytes array not the same"
        )
        obj.copy(parent=workspace_copy)

        workspace_copy = Workspace(os.path.join(tmp_path, "testProject_B.geoh5"))
        copied_obj = workspace_copy.get_entity(obj.uid)[0]
        rec_data = copied_obj.get_entity("numpy_array.txt")[0]
        compare_entities(file_data, rec_data, ignore=["_parent"])

    with pytest.raises(ValueError) as excinfo:
        file_data.values = "abc"

    assert "Input 'values' for FilenameData must be of type 'bytes'." in str(
        excinfo.value
    )
