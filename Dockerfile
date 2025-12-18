FROM python:3.13-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    build-essential \
    libgtk-3-0 \
    libgdk-pixbuf-2.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pyinstaller
COPY . .
CMD ["bash", "-c", "pyinstaller --name=BiomeMacro --onefile --windowed --add-data assets:assets --add-data biome_data.py:. --add-data VERSION:. --hidden-import=PIL._tkinter_finder --collect-all customtkinter main.py && chmod -R 777 dist/"]
