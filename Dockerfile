FROM quay.io/ubi9/ubi

# Enable AppStream & install Python 3.9 and benchmarking tools
RUN dnf -y install \
    python3.9 \
    python3-pip \
    iperf3 \
    hping3 \
    sysbench \
    procps \
    && dnf clean all

# Optional: symlink python -> python3.9 for convenience
RUN alternatives --install /usr/bin/python python /usr/bin/python3.9 1

# Set working directory
WORKDIR /app

# Copy Python benchmark code and dependencies
COPY src/ /app/

# Install Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Set default command
ENTRYPOINT ["python", "benchmarker.py"]
CMD ["--config", "/app/benchmark.json"]
