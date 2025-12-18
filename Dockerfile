FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.13 \
    python3.13-venv \
    python3.13-dev \
    python3-pip \
    build-essential \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
RUN python3.13 -m ensurepip --upgrade && python3.13 -m pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN python3.13 -m pip install --no-cache-dir -r requirements.txt
RUN python3.13 -m pip install --no-cache-dir pyinstaller
COPY . .
CMD ["bash", "-c", "python3.13 -m PyInstaller --name=BiomeMacro --onefile --windowed --add-data assets:assets --add-data biome_data.py:. --add-data VERSION:. --hidden-import=PIL._tkinter_finder --hidden-import=pynput.keyboard._xorg --hidden-import=pynput.mouse._xorg --collect-all customtkinter --collect-all pynput main.py && chmod -R 777 dist/"]
