# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from pathlib import Path as path_t
from typing import Any

import imageio as mgio
import numpy as nmpy


array_t = nmpy.ndarray


def FrameByIMAGEIO(path: path_t, /) -> array_t:
    """"""
    return mgio.v3.imread(path)


try:
    # noinspection PyPackageRequirements
    import itk as ittk

    def FrameByITK(path: path_t, /) -> array_t:
        """
        Also works for sequences
        """
        itk_image = ittk.imread(str(path))
        output = ittk.array_from_image(itk_image)

        return output

    def SaveFrameWithITK(frame: array_t, path: path_t, /) -> None:
        """"""
        itk_np_view = ittk.image_view_from_array(frame)
        ittk.imwrite(itk_np_view, str(path))

except ModuleNotFoundError:

    def RaiseMissingITKException(*_, **__) -> Any:
        """"""
        raise RuntimeError("ITK (https://itk.org/) is not available")

    FrameByITK = RaiseMissingITKException
    SaveFrameWithITK = RaiseMissingITKException
