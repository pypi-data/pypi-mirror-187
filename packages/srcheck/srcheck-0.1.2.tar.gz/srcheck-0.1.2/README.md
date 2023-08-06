<p align="center">
  <a href="https://github.com/csaybar/srcheck"><img src="https://user-images.githubusercontent.com/16768318/213960001-66bb7d18-13d8-41d4-9de3-1e8a77f73787.png" alt="header" width="55%"></a>
</p>

<p align="center">
    <em>An Agnostic Benchmark for Optical Remote Sensing Image Super-Resolution</em>
</p>

<p align="center">
<a href='https://pypi.python.org/pypi/srcheck'>
    <img src='https://img.shields.io/pypi/v/srcheck.svg' alt='PyPI' />
</a>
<a href='https://anaconda.org/conda-forge/srcheck'>
    <img src='https://img.shields.io/conda/vn/conda-forge/srcheck.svg' alt='conda-forge' />
</a>
<a href="https://opensource.org/licenses/MIT" target="_blank">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
</a>
<a href='https://srcheck.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/eemont/badge/?version=latest' alt='Documentation Status' />
</a>
<a href="https://github.com/psf/black" target="_blank">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black">
</a>
<a href="https://pycqa.github.io/isort/" target="_blank">
    <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" alt="isort">
</a>
</p>

---

**GitHub**: [https://github.com/csaybar/srcheck](https://github.com/csaybar/srcheck)

**Documentation**: [https://srcheck.readthedocs.io/](https://srcheck.readthedocs.io/)

**PyPI**: [https://pypi.org/project/srcheck/](https://pypi.org/project/srcheck/)

**Conda-forge**: [https://anaconda.org/conda-forge/srcheck](https://anaconda.org/conda-forge/srcheck)

**Tutorials**: [https://github.com/davemlz/srcheck/tree/master/docs/tutorials](https://github.com/davemlz/srcheck/tree/master/docs/tutorials)

**Paper**: Coming soon!

---

## Overview

In remote sensing, image super-resolution (ISR) is a technique used to create high-resolution (HR) images from low-resolution (R) satellite images, giving a more detailed view of the Earth's surface. However, with the constant development and introduction of new ISR algorithms, it can be challenging to stay updated on the latest advancements and to evaluate their performance objectively. To address this issue, we introduce SRcheck, a Python package that provides an easy-to-use interface for comparing and benchmarking various ISR methods. SRcheck includes a range of datasets that consist of high-resolution and low-resolution image pairs, as well as a set of quantitative metrics for evaluating the performance of SISR algorithms.

## Installation

Install the latest version from PyPI:

```
pip install srcheck
```

Upgrade `srcheck` by running:

```
pip install -U srcheck
```

Install the latest version from conda-forge:

```
conda install -c conda-forge srcheck
```

Install the latest dev version from GitHub by running:

```
pip install git+https://github.com/csaybar/srcheck
```

## How does it work?

<center>
    <img src="https://user-images.githubusercontent.com/16768318/213967913-3c665d59-5053-43a7-a450-859b7442b345.png" alt="header" width="70%">
</center>

**srcheck** needs either a `torch.nn.Module` class or a compiled model via `torch.jit.trace` or `torch.jit.script`. The following example shows how to run the benchmarks:

```python
import torch
import srcheck

model = torch.jit.load('/content/quantSRmodel.pt', map_location='cpu')
srcheck.benchmark(model, dataset='SPOT-50', metrics=['PSNR', 'SSIM'], type= "NoSRI")
```

srcheck supports two group types of metrics: (a) Surface Reflectance Integrity (SRI) and (b) No Surface Reflectance Integrity (NoSRI). This difference is due to the fact that depending on the application, developers will be interested in optimizing the "image quality" or the "image fidelity". *Image fidelity* refers to how closely the LR image represents the real source distribution (HR). Optimizing fidelity is crucial for applications that require preserving surface reflectance as close as possible to the original values. On the other hand, *image quality* refers to how pleasant the image is for the human eye. Optimizing image quality is important for creating HR image satellite base maps. The image below shows the natural trade-off that exists between these two group types of metrics.


<center>
    <img src="https://user-images.githubusercontent.com/16768318/213970463-5c2a8012-4e76-48ce-bb13-4d51590d359c.png" alt="header" width="60%">
</center>

But what happens if my ISR algorithm increases the image by a factor of 8, but the datasets available in srcheck do not support 8X? In that case, *srcheck* will automatically convert the results to the native resolution of the datasets. For example, if your algorithm increases the image by 2X, and you want to test it on SPOT-50 whose images are 10m in LR and 6m in HR, *srcheck* will upscale the results from 5 meters to 6m using the bilinear interpolation algorithm. Similarly, in the MUS2-50 dataset, *srcheck* will downscale the results from 5m to 2m. This is done in order the results can be compared with the datasets available.

<center>
    <img src="https://user-images.githubusercontent.com/16768318/213971771-04b193e7-83e8-436a-b4a1-0c317cc7b756.png" alt="header" width="75%">
</center>

## Datasets

[**https://zenodo.org/record/7562334**](https://zenodo.org/record/7562334)

More datasets are coming soon!

## Metrics

Metrics documentation is coming soon!
