<div align="center"> 
  <img src="https://github.com/user-attachments/assets/167240c1-6dd4-44c2-b3b6-81faed18f9bf" width="100" alt="DeepSignus">
  <h1>DeepSignus</h1> 
  <div>Real-time hand gesture tracking and virtual drawing system</div> 
  <div>based on monocular camera input and depth estimation.</div> 
</div>

# Features
- 📷 Real-time hand signature drawing using an RGB camera  
- ✍️ Detection of hand and fingertip positions with MediaPipe  
- 🧠 Depth estimation via MiDaS model for 3D effect  
- 🖥️ GUI implemented with PySide6 for mode control  
- 🎞️ Video capture and processing via OpenCV  
- 🧩 Modular class-based architecture for easy extension

# Installation & Running
The application can be installed using the [installer](https://github.com/Dast3X/Virtual-Signature/releases/download/Beta/DeepSignusInstaller.exe).
Alternatively, clone the repo and create a virtual environment:
```bash
# Repository cloning
git clone https://github.com/Dast3X/Virtual-Signature.git

# Go to project directory
cd Virtual-Signature

# Enable venv
python -m venv venv
source .\venv\Scripts\activate

# Install all necessary dependencies.
pip install -r requirements.txt

# Launch the application
python main.py
```
![image](https://github.com/user-attachments/assets/48a74416-f09a-4851-862e-d04e323a24af)
![image](https://github.com/user-attachments/assets/e83ba251-2e4a-49fa-9c27-2980bb9eb9bf)
![image](https://github.com/user-attachments/assets/463ab0d8-acbe-4cb7-8749-49563a69d680)
![image](https://github.com/user-attachments/assets/8e5be24e-737f-42a1-9a99-41f3da509f68)

# Testing
The directory `./tests` contains the `run_tests.py` script, which runs all tests located in the `./tests/scripts` subfolder. After execution, the results are saved as a markdown table in [tests/test_results.md](https://github.com/Dast3X/Virtual-Signature/blob/master/tests/test_results.md).
## Test Structure
```bash
tests/
│
├── run_tests.py
│
├── scripts/
│   ├── test_about.py
│   ├── test_camera_settings_dock.py
│   ├── test_help_dialog.py
│   ├── test_main.py
│   ├── test_signature.py
│   ├── test_signature_settings_dock.py
│   ├── test_statusbar.py
│   ├── test_utils.py
│   └── test_video_thread.py
│
└── test_results.md
```
## Run tests
```bash
# Run tests
python tests/run_tests.py
```
## Results
| Test File | Total Tests | Passed | Failed | Errors | Time (s) | Status |
|-----------|-------------|--------|--------|--------|----------|--------|
| test_about.py | 3 | 3 | 0 | 0 | 0.369 | PASS |
| test_camera_settings_dock.py | 9 | 9 | 0 | 0 | 0.329 | PASS |
| test_help_dialog.py | 10 | 10 | 0 | 0 | 0.083 | PASS |
| test_main.py | 7 | 7 | 0 | 0 | 0.678 | PASS |
| test_signature.py | 12 | 12 | 0 | 0 | 0.008 | PASS |
| test_signature_settings_dock.py | 11 | 11 | 0 | 0 | 0.069 | PASS |
| test_statusbar.py | 2 | 2 | 0 | 0 | 0.220 | PASS |
| test_utils.py | 2 | 2 | 0 | 0 | 0.002 | PASS |
| test_video_thread.py | 8 | 8 | 0 | 0 | 0.096 | PASS |
| **TOTAL** | **64** | **64** | **0** | **0** | **1.854** | **PASSED** |

# Research
This is the experimental part that can be found in `/ipynb`
## 📊 Frame Skip Experiments Summary

To evaluate the trade-off between performance and accuracy, a series of experiments were conducted using different `frame_skip` values (0 to 5). This parameter controls how many video frames are skipped before sending the next one to the neural network.

- **Test setup:** 60 FPS Full HD video, processed via Jupyter Notebook.
- **Metrics collected:** number of processed frames, trajectory points, average FPS, and processing time.
- **Results location:** `/results` folder (includes `plot.png` and markdown tables).

### 🔍 Key Findings

| Frame Skip | Frames Fed | Trajectory Points | Avg. FPS | Processing Time (s) |
|------------|------------|-------------------|----------|----------------------|
| 0          | 60         | 423               | 20.92    | 20.02                |
| 1          | 30         | 210               | 33.37    | 9.33                 |
| 2          | 20         | 140               | 42.69    | 6.66                 |
| 3          | 15         | 103               | 47.98    | 4.84                 |
| 4          | 12         | 79                | 50.85    | 3.89                 |
| 5          | 10         | 61                | 52.87    | 3.06                 |

### 📈 Visual Insights
- **Performance vs. Accuracy Trade-off:**  
  - Higher `frame_skip` = higher FPS and lower processing time.  
  - But this comes with fewer trajectory points and reduced signature smoothness.
    
![image](https://github.com/user-attachments/assets/993fb85b-40aa-454b-b1d1-4358e4a8253a)
- **Trajectory Visualization:**  
  - At `frame_skip = 0`, the trajectory is smooth and highly detailed.  
  - From `frame_skip = 3+`, the curves become jagged and less natural.  
  - `frame_skip = 1` provides the best balance between detail and performance.
    
![image](https://github.com/user-attachments/assets/4feb6b34-aad0-42c6-b4c6-8bf3dafa77dc)
🔧 **Recommendation:**  
Use `frame_skip = 1` for optimal results on modern systems. For lower-end machines, `frame_skip = 2` offers a reasonable compromise.

## 🖼️ Background Removal Using Depth Maps
One of the main challenges in hand gesture and signature tracking is background interference. Inconsistent lighting or complex scenes can reduce detection accuracy, cause false activations, and lead to jittery trajectories.
To mitigate this, a background removal algorithm based on **depth maps** was implemented. This method improves preprocessing before feeding the image into a neural network, reducing background noise and enhancing focus on relevant features.

### 🔍 MiDaS Integration
MiDaS is used to estimate depth from each RGB frame. Three models were tested:
- **MiDaS Small** – Fastest, lower quality
- **DPT Hybrid** – Balanced quality and speed
- **DPT Large** – Highest accuracy, slowest

📸 *Visual examples*
![image](https://github.com/user-attachments/assets/03b7d8ad-f438-4ead-b981-e66ae63ef9a6)
![image](https://github.com/user-attachments/assets/a80a6edd-5e87-4020-af03-82ee2112358a)

### 🧪 Experimental Findings

Although full real-time integration wasn’t implemented, experiments demonstrated the viability of this method. However, **depth estimation is computationally heavy**, especially without a GPU.

### ⏱️ MiDaS Inference Times

| Model           | Avg. Processing Time (CPU) | Avg. Processing Time (GPU) |
|----------------|-----------------------------|-----------------------------|
| MiDaS Small     | 169 ms                      | 31 ms                       |
| DPT Hybrid      | 1640 ms                     | 100 ms                      |
| DPT Large       | 3513 ms                     | 155 ms                      |

> [!WARNING]
> - Avoid using large MiDaS models on CPUs — inference is too slow.
> - **GPU usage is highly recommended** for real-time systems.
> - For practical applications, consider using optimized models like **DepthAnything** or SaaS-based depth estimation.

**Depth-based background removal** offers promising results in improving gesture tracking, but requires sufficient computing power for real-time performance.
# License
MIT, Copyright © 2025, Daniils Grammatikopulo
