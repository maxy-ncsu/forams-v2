# ===============================================================================
# Copyright 2018 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import time
import numpy as np
import cv2
import matplotlib.pyplot as plt

from Amscope_Camera.camera import *

cam = ToupCamCamera()
cam.open()
time.sleep(2)

img = np.array(cam.get_pil_image())
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

plt.imshow(img)
plt.show()

# for saving images
path = 'images/cam_test_1/test_image-{:02d}.jpg'.format(1)
cam.save(path)
time.sleep(2)

