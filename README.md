# TorrentBotX

`TorrentBotX` 是一个**面向多下载器、多 PT 站点**的自动化下载与管理平台。项目目标是：通过统一的接口，实现
qBittorrent、aria2、Transmission 多下载器和主流 PT 站点的联动，支持定时任务、自动清理和 Telegram 机器人交互，极大提升下载管理体验与自动化水平。

---

## 项目亮点

- **多下载器支持**：集成 qBittorrent、aria2、Transmission，下载管理一站式搞定
- **多 PT 站点集成**：内置 M-Team、dicmusic、carpt、ptskit 四大 PT 站点适配器
- **Telegram 机器人交互**：支持通过 TG Bot 远程管理、搜索、添加、监控、操作下载任务
- **灵活定时调度**：内置 APScheduler，可按需自动清理、自动任务检测与管理
- **自动化任务处理**：自动下载、自动删种/荣退、分类、批量管理
- **高度模块化**：结构清晰，便于二次开发与扩展
- **本地 SQLite 数据库**：任务、用户、历史等数据安全持久化
- **优雅日志与通知**：全局日志系统和灵活的通知机制，支持 Telegram 消息推送

---

## 目录结构

```text
torrentbotx/
├── .gitignore
├── README.md
├── requirements.txt
├── run.py              # 主入口
├── setup.py            # 启动前环境和DB检查
├── tests/              # 单元测试
└── torrentbotx/
    ├── __init__.py
    ├── bots/
    │   └── telegram/   # Telegram Bot 交互
    ├── config/         # 配置与配置工具
    ├── core/           # 系统主调度/业务中枢
    ├── db/             # 数据库及操作
    ├── downloaders/    # qBittorrent/aria2/Transmission 适配器
    ├── models/         # 业务数据结构
    ├── notifications/  # 消息推送与通知
    ├── tasks/          # 定时任务调度、自动化逻辑
    ├── trackers/       # PT 站点 API 适配
    └── utils/          # 工具模块（如日志等）
````

---

## 功能一览

* **下载器管理**：一套接口管理多个下载器，支持自动登录、分类、状态监控
* **PT 站点适配**：可同时处理多个 PT 站点的登录、搜索、资源下载、流量优惠识别等
* **TG Bot 命令集**：

    * 资源搜索
    * 种子任务添加、分类、删除、状态查询
    * 远程批量管理
* **定时任务**：

    * 任务健康检查
    * 自动删种、自动荣退
    * 周期资源同步
* **通知系统**：任务完成、异常、警告、主动推送均支持
* **任务持久化**：所有任务、用户、资源等数据自动存储于 SQLite，本地安全

---

## 安装与部署

### 1. 克隆项目

```bash
git clone https://github.com/astralwaveorg/torrentbotx.git
cd torrentbotx
```

### 2. 初始化环境与依赖

```bash
python3 setup.py
```

* 首次运行会自动创建虚拟环境、安装依赖、初始化数据库和目录结构

### 3. 激活虚拟环境

```bash
source venv/bin/activate
```

### 4. 配置项目

* 编辑 `torrentbotx/config/config.yaml`（或参考 `example.yaml`）填写：

    * 下载器连接信息
    * Telegram Bot Token 及允许的用户ID
    * PT 站点 API/COOKIE/Token 等
    * 定时任务参数

### 5. 启动服务

```bash
python run.py
```

* 运行后，项目将自动启动 Telegram Bot、各下载器适配与定时任务调度

---

## 使用指南

### 1. **Telegram Bot**

* 加入配置的 Telegram 机器人，发送 `/start` 即可交互
* 支持命令和按钮操作，参考 `/help` 获取命令清单
* 支持资源搜索、任务添加、状态监控、任务删除/分类等操作

### 2. **任务管理与自动化**

* 所有自动化任务通过配置文件或 web 控制台调整（未来规划）
* 支持自动删种、下载完成推送、定期巡检

### 3. **数据库操作**

* 所有数据持久化到本地 `torrentbotx.db`，无需单独部署数据库

---

## 依赖环境

* **Python 3.8+**
* **macOS / Linux / WSL**
* 推荐使用虚拟环境 (`venv`)
* 所有依赖在 `requirements.txt` 列出

---

## 开发规范

1. **使用“绝对导入”，避免相对导入**

```python
# ✅ 推荐
from torrentbotx.utils.logger import get_logger

# ❌ 不推荐
from ..utils.logger import get_logger
```

**原因**：绝对导入清晰易懂、工具补全友好、避免跨目录报错、兼容 IDE 和打包工具。

2. **所有模块函数使用全路径导入**

```python
# ✅ 推荐
from torrentbotx.utils.string_utils import to_snake_case

# ❌ 不推荐
from string_utils import to_snake_case  # 模糊来源
```

**原因**：明确函数来源，避免命名冲突，便于维护与代码审查。

3. **函数、变量使用小写+下划线命名**

```python
def get_user_info():
    ...
```

4. **类名使用大驼峰命名（PascalCase）**

```python
class UserProfile:
    ...
```

5. **模块名使用小写或小写加下划线**

```bash
# 文件名
user_service.py
```

**原因**：统一命名规范，提升团队协作效率，遵守社区标准。

6. **所有模块、类、函数必须写 docstring（推荐 Google 风格）**

```python
def get_user_info(user_id: int) -> dict:
    """
    获取用户信息

    Args:
        user_id (int): 用户 ID

    Returns:
        dict: 用户信息字典
    """
```

**原因**：提升可读性、文档自动生成支持好、方便团队理解代码。

7. **使用 pytest 编写测试，目录统一为 tests/**

```bash
tests/
├── test_user_service.py
```

**原因**：pytest 简洁强大，测试目录分离清晰，便于 CI/CD 集成。

8. **统一代码格式使用 black + isort + flake8**

```bash
black .         # 自动格式化
isort .         # 自动排序导入
flake8 .        # 静态检查
```

**原因**：强制格式一致、消除代码风格争议、提升代码质量。

9. **配置使用单独模块 + .env 文件 + pydantic 管理**

```python
# config/settings.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    log_level: str = "info"

    class Config:
        env_file = ".env"
```

**原因**：配置与逻辑解耦、支持多环境、类型安全、默认值可控。

10. **`统一入口：main.py + if **name** == "**main**":`**

```python
# main.py
def main():
    ...


if __name__ == "__main__":
    main()
```

**原因**：方便调试、作为脚本或模块都能运行、清晰入口点。

11. **依赖管理使用 `requirements.txt` 或 `poetry` / `pip-tools`**

```bash
pip freeze > requirements.txt
# 或使用 poetry 管理依赖
```

**原因**：可重复安装、版本可控、便于部署与 CI 流程。

12. **避免硬编码常量，使用配置、常量模块或环境变量管理**
13. **日志使用封装好的工具，不直接用 print()**
14. **异常处理统一封装，重要操作加异常捕获**

---

## ✅ 推荐工具生态

| 工具            | 用途               |
| --------------- | ------------------ |
| black           | 代码格式化         |
| isort           | import 排序        |
| flake8 / pylint | 静态代码检查       |
| mypy            | 类型检查           |
| pydantic        | 配置/数据校验      |
| pytest          | 单元测试           |
| coverage.py     | 测试覆盖率         |
| pre-commit      | Git 提交前自动检查 |

---

## 常见问题与维护

* **升级依赖/代码**

  ```bash
  git pull origin main
  pip install -r requirements.txt
  ```
* **DB/配置/下载器异常**

    * 查看 `torrentbotx/utils/logger.py` 的日志输出
    * 检查配置文件与网络环境

---

## 许可证

MIT License，详见 [LICENSE](LICENSE)

---

## 贡献与反馈

* 欢迎 Issue、PR、建议！
* QQ/Telegram 交流群敬请期待

---

**Enjoy Your Automated Torrent Life!**
