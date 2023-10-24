FROM rayproject/ray-ml:65ed62-py310-gpu

WORKDIR /workspace

COPY ../requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./copilot ./copilot
COPY main.py main.py

COPY Makefile Makefile
