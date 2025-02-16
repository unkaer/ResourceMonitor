# 基础镜像
FROM python:3.9-slim

# 安装依赖
RUN pip install psutil

# 将程序文件复制到容器
COPY adjust_resources.py /app/adjust_resources.py

# 设置工作目录
WORKDIR /app

# 启动程序
CMD ["python", "adjust_resources.py"]
