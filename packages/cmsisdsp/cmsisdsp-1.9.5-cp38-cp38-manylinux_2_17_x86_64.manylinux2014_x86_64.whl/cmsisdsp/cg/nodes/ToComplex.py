###########################################
# Project:      CMSIS DSP Library
# Title:        ToComplex.py
# Description:  Node to convert real to complex
# 
# $Date:        30 July 2021
# $Revision:    V1.10.0
# 
# Target Processor: Cortex-M and Cortex-A cores
# -------------------------------------------------------------------- */
# 
# Copyright (C) 2010-2023 ARM Limited or its affiliates. All rights reserved.
# 
# SPDX-License-Identifier: Apache-2.0
# 
# Licensed under the Apache License, Version 2.0 (the License); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
############################################
from .simu import *

# Convert a stream of reals a b c ...
# to complexes a 0 b 0 c 0 ...
class ToComplex(GenericNode): 
    def __init__(self,inputSize,outputSize,fifoin,fifoout):
        GenericNode.__init__(self,inputSize,outputSize,fifoin,fifoout)

    def run(self):
        a=self.getReadBuffer()
        b=self.getWriteBuffer()
        b[::2]=a[:]
        b[1::2] = 0
        return(0)