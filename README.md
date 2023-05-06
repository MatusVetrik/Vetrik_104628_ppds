# CUDA

### Problem

We are using CUDA for conversion of images from rgb to grayscale. 
We are focusing on comparison of CPU and GPU computation speed.

### How to run code

We are implementing solution with using these modules.
```commandline
from PIL import Image
from numba import cuda
import numpy as np
import time
from math import ceil
import os
import matplotlib.pyplot as plt
```
For installation of next modules run these commands in your terminal.
```commandline
pip install numba
pip install numpy
pip instal matplolit
```

### Solution

We are implementing two functions. One for sequential approach (CPU) and one for parallel 
approach (GPU) using CUDA.

### CPU
In `main_seq()` we are trying sequential approach. 
```commandline
def main_seq():
    s = 0
    for filename in os.listdir(INPUT_FILE_NAME):
        img = plt.imread(f'./assets/images/{filename}')

        start = time.time()
        gray = transform_to_grayscale(img)
        end = time.time()
        s += end-start
        print(f"Time: {end - start} sec")

        plt.imsave(f"./assets/output/{filename}", gray, cmap='gray')
    print(f"Sum: {s}")
```
Our dataset is 100+ random images in directory `/assets/images`. We are looping through this 
directory and each time creating 2D array of rgb values from image. This array is converted
to greyscale in function `transform_to_grayscale(img)`.

```commandline
def transform_to_grayscale(img):
    return 0.2989 * img[:, :, 0] + 0.5870 * img[:, :, 1] + 0.1140 * img[:, :, 2]
```
This function takes whole array of rgb values and multiply `red` by `0.2989`, `blue` by
`0.5870` and `green` by `0.1140`. This is a classic way to turn original image to greyscale.

### GPU

In `main()` we are trying parallel approach.

```commandline
def main():
    s = 0
    for filename in os.listdir(INPUT_FILE_NAME):
        img = np.array(Image.open(f'./assets/images/{filename}'))

        start = time.time()
        gray = to_grayscale(img)
        end = time.time()
        s += end - start
        print(f"Time: {end - start} sec")

        plt.imsave(f"./assets/output2/{filename}", gray, cmap='gray')
    print(f"Sum: {s}")
```

This is similar to previous `main_seq()` function but here we are turning rgb array to 
numpy array. 

```commandline
@cuda.jit
def grayscale_kernel(img, gray_img):
    i, j = cuda.grid(2)
    if i < img.shape[0] and j < img.shape[1]:
        gray_img[i][j] = 0.2989 * img[i, j, 0] + 0.5870 * img[i, j, 1] + 0.1140 * img[i, j, 2]


def to_grayscale(img):
    gray_img = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)

    tpb = (16, 16)
    bpg = (ceil(img.shape[0] / tpb[0]), ceil(img.shape[1] / tpb[1]))

    grayscale_kernel[bpg, tpb](img, gray_img)

    return gray_img
```

As we can see, we are creating array of zeros for output as variable `gray_img`. Then we
are selecting number of cores in `tpb`. Then we divide our array to smaller parts by number
of cores. In `greyscale_kernel` function we are setting `cuda_grid` and performing computation.

### Results
![pexels-edoardo-colombo-1507856.jpg](assets%2Fimages%2Fpexels-edoardo-colombo-1507856.jpg)
![pexels-edoardo-colombo-1507856.jpg](assets%2Foutput%2Fpexels-edoardo-colombo-1507856.jpg)

![pexels-steve-johnson-1843716.jpg](assets%2Fimages%2Fpexels-steve-johnson-1843716.jpg)
![pexels-steve-johnson-1843716.jpg](assets%2Foutput%2Fpexels-steve-johnson-1843716.jpg)

![pexels-josh-hild-2422259.jpg](assets%2Fimages%2Fpexels-josh-hild-2422259.jpg)
![pexels-josh-hild-2422259.jpg](assets%2Foutput%2Fpexels-josh-hild-2422259.jpg)

![pexels-designecologist-1779487.jpg](assets%2Fimages%2Fpexels-designecologist-1779487.jpg)
![pexels-designecologist-1779487.jpg](assets%2Foutput%2Fpexels-designecologist-1779487.jpg)

![pexels-sanketh-rao-716107.jpg](assets%2Fimages%2Fpexels-sanketh-rao-716107.jpg)
![pexels-sanketh-rao-716107.jpg](assets%2Foutput%2Fpexels-sanketh-rao-716107.jpg)

On CPU this computation took for all images `0.77298` seconds (avg/image `0.00678s`). On GPU this computation took `0.32894` 
seconds (avg/image `0.002885`).
As we can see, on CPU it takes circa 2 times longer to make this type of computation. 