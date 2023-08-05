# Copyright 2019 The TensorFlow Probability Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Experimental tools for linear algebra."""

from tensorflow_probability.python.experimental.linalg.linear_operator_interpolated_psd_kernel import LinearOperatorInterpolatedPSDKernel
from tensorflow_probability.python.experimental.linalg.linear_operator_psd_kernel import LinearOperatorPSDKernel
from tensorflow_probability.python.experimental.linalg.linear_operator_unitary import LinearOperatorUnitary
from tensorflow_probability.python.experimental.linalg.no_pivot_ldl import no_pivot_ldl
from tensorflow_probability.python.experimental.linalg.no_pivot_ldl import simple_robustified_cholesky
from tensorflow_probability.python.internal import all_util


_allowed_symbols = [
    'LinearOperatorInterpolatedPSDKernel',
    'LinearOperatorPSDKernel',
    'LinearOperatorUnitary',
    'no_pivot_ldl',
    'simple_robustified_cholesky',
]

all_util.remove_undocumented(__name__, _allowed_symbols)
