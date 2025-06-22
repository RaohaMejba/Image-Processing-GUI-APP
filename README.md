# Image Processing GUI Application

## Overview

This project is a Python-based GUI application for grayscale image processing using custom filter kernels. Built using the `Tkinter` library for GUI components and `PIL` (Pillow) for image processing, the app allows users to upload an image, apply various filters (Box Blur, Edge Detection, Sharpen, High Pass, Low Pass), and save the processed results. The filters are implemented using 2D convolution operations.

<p align="center">
  <img src="Project Screenshots/User Interface of GUI.png" width="800">
</p>

## Features

* Fullscreen graphical user interface (GUI)
* Upload and display a grayscale version of any image
* Apply the following filters:

  * Box Blur
  * Edge Detection (Sobel operator)
  * Sharpen
  * High Pass Filter
  * Low Pass Filter
* Save all processed outputs to a selected directory
* Displays images in a 2x3 grid with centered titles and button panel
* Customized styling with background image support

## Getting Started

### Prerequisites

Ensure the following libraries are installed:

```bash
pip install numpy pillow
```

### Running the App

1. Clone the repository:

```bash
git clone https://github.com/RaohaMejba/Image-Processing-GUI-APP.git
cd grayscale-image-processing-gui
```

2. Run the Python script:

```bash
python app.py
```

### Directory Structure

```
├── app.py
├── Image/
│   └── Background.png
├── Project Screenshots/
│   └── GUI_Screenshot_1.png
│   .............
│   └── GUI_Screenshot_5.png
├── requirements.txt
└── README.md
```

## Filters and Convolution Details

### Kernel Convolution Principle

All filters in this application operate using **2D convolution**. This involves sliding a matrix (kernel) over each pixel of the input image and computing a weighted sum of the surrounding pixels.

```python
output[i, j] = sum(kernel[x, y] * image[i+x, j+y])
```

Each filter uses a distinct kernel matrix to emphasize different features:

### 1. Box Blur

* **Purpose**: Smoothens the image by averaging surrounding pixels.
* **Kernel**:

```
1/9 * [[1, 1, 1],
       [1, 1, 1],
       [1, 1, 1]]
```

### 2. Edge Detection (Sobel Operator)

* **Purpose**: Highlights horizontal and vertical edges in the image.
* **Kernels**:

```
Gx = [[ 1, 0, -1],
      [ 2, 0, -2],
      [ 1, 0, -1]]

Gy = [[ 1,  2,  1],
      [ 0,  0,  0],
      [-1, -2, -1]]
```

* **Result**: sqrt(Gx^2 + Gy^2)

### 3. Sharpen

* **Purpose**: Enhances edges and fine details.
* **Kernel**:

```
[[ 0, -1,  0],
 [-1,  5, -1],
 [ 0, -1,  0]]
```

### 4. High Pass Filter

* **Purpose**: Detects rapid intensity changes (fine details, noise).
* **Kernel**:

```
[[-7/9, -7/9,  0],
 [   0,   5,   0],
 [   0, -7/9, -7/9]]
```

### 5. Low Pass Filter

* **Purpose**: Removes high-frequency content, smoothens noise.
* **Kernel**:

```
[[0, 0, 0],
 [0, 5/9, 0],
 [0, 0, 0]]
```

## Project Screenshot

<p align="center">
  <img src="Project Screenshots/GUI_Screenshoot_1.png" width="800">
  <img src="Project Screenshots/GUI_Screenshoot_3.png" width="800">
  <img src="Project Screenshots/GUI_Screenshoot_5.png" width="800">
</p>

## License

This project is open-source and free to use under the MIT License.

## Contact

**Raoha Bin Mejba**

**Email:** raoha77@outlook.com 
