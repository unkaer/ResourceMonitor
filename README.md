# ResourceMonitor

**ResourceMonitor** 是保持服务器CPU、内存最低占用的python脚本，保活甲骨文免费服务器用，推荐Docker部署。

## 克隆本项目

首先，克隆本项目到本地：

```bash
git clone https://github.com/unkaer/ResourceMonitor.git
cd ResourceMonitor
```

## 构建 Docker 镜像
在项目根目录下，使用以下命令构建 Docker 镜像：

```bash
docker build -t resource-adjuster .
```

## 部署运行
构建完成后，可以通过以下命令启动 Docker 容器：

```bash
docker run --rm -d --name resource-adjuster resource-adjuster
```
其中 `--rm` 会在容器停止时自动删除容器，-d 则使容器在后台运行。

## 调试运行
如果需要调试容器，可以使用以下命令启动容器，并进入交互模式：

```bash
docker run --rm -it --name resource-adjuster resource-adjuster
```

## 查看运行日志
可以通过以下命令查看正在运行的容器：

```bash
docker ps -a
```
查看容器的实时日志输出：

```bash
docker logs resource-adjuster
```

## 停止与删除容器
停止并删除运行中的容器：

```bash
docker stop resource-adjuster
docker rm resource-adjuster
```