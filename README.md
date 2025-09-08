# iOSA
## About iOSA
The iOSA tool is a Python-based solution designed to assist in diagnosing Obstructive Sleep Apnea (OSA). It manages and analyzes clinical and multimedia data, incorporating pattern recognition to identify potential OSA indicators.

It enhances the diagnostic process by supporting data integrity and security. The iOSA tool aids physicians in improving OSA diagnosis efficiency and accuracy in clinical settings.

iOSA is designed to manage patient profiles, store data related to OSA, export the data to specific reports, and detect patterns between the stored data. To achieve this, the iOSA tool is divided into four modules: Patient Profile Management Module, Apnea Data Management Module, Reporting Module, and Pattern Detection Module.

## Installation
### 1. Python
The system requires Python 3.9.10 version. It can be downloaded from [here](https://www.python.org/downloads/release/python-3910/).

If you have problems installing Python, please refer to the Python installation section of the [iOSA_Installation_guide_v3](iOSA_Installation_guide_v3.pdf) manual.

### 2. MySQL
The core database is MySQL; an official release can be downloaded from [here](https://dev.mysql.com/downloads/installer/).

**NOTE:** It is highly recommended to follow the steps described in the MySQL section of [iOSA_Installation_guide_v3](iOSA_Installation_guide_v3.pdf) manual. The system requires a special configuration to work correctly. So, if you experience any malfunction regarding the database, please make sure the guide was followed correctly.

### 3. MongoDB
The system works with a second database using NoSQL technology to handle the multimedia data. For this, MongoDB version 7.0.9 is required, and an official release can be downloaded from [here](https://www.mongodb.com/try/download/community).

Again, the MongoDB section in [iOSA_Installation_guide_v3](iOSA_Installation_guide_v3.pdf) manual can be consulted for guidance.

### 4. K-Lite Codecs
Due to the handling of different multimedia files, it is encouraged to download a codec package to prevent file compatibility errors. A free and lightweight codec package can be downloaded from [here](https://www.codecguide.com/download_kl.htm).

In the K-Lite Codecs section of the [iOSA_Installation_guide_v3](iOSA_Installation_guide_v3.pdf) manual, the package that can cover most multimedia files the system can use is described."

### 5. 7Zip
The computer where the system is being installed may not have a file extraction utility, so 7Zip can be downloaded from [here](https://7-zip.org/).

### 6. FFmpeg
The system handles audio files and video files; if the computer where the system is being installed doesn’t have audio codecs, a possible crash may occur. The necessary audio codes are in the FFmpeg package; they can be downloaded from [here](https://ffmpeg.org/download.html).

**NOTE:** It is highly recommended to follow the steps described in the FFmpeg section of the [iOSA_Installation_guide_v3](iOSA_Installation_guide_v3.pdf) manual. If the path is set incorrectly, the system will not be able to handle the video files.

### 7. Tesseract-ORC
The system also recognizes text from files and images. For this task, it uses Tesseract-OCR, which can be downloaded from [here](https://github.com/UB-Mannheim/tesseract/wiki).

**NOTE:** It is highly recommended to follow the steps described in the Tesseract-ORC section of the [iOSA_Installation_guide_v3](iOSA_Installation_guide_v3.pdf) manual. If the path is set incorrectly, the system will not be able to handle the video files.

### 8. Visual C++ Redistributable Packages for Visual Studio 2013
The system requires the computer to be able to run C++ code, so if the computer doesn’t have the Microsoft C++ packages, they can be downloaded from [here](https://www.microsoft.com/en-us/download/details.aspx?id=40784). This step is described in the Visual C++ section of the [iOSA_Installation_guide_v3](iOSA_Installation_guide_v3.pdf) manual.

## Python Dependencies
The code already has a requirements.txt file, so it is only necessary to run it once to download them. Alternatively, the .bat script can be used to install them automatically, and it can be found [here](code/bin/utils/install_dependecies.bat).

##### For more system setups, read the [iOSA_Installation_guide_v3](iOSA_Installation_guide_v3.pdf) manual.
