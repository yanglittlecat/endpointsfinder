# Juicy Endpoints (Burp Suite 插件)

**Juicy Endpoints** 是一个用于 Burp Suite 的扩展插件，使用 Python 编写（Jython 环境）。该插件会从 HTTP 响应中自动提取“juicy”的端点路径，例如 `/api/user`, `/admin/panel` 等，非常适用于安全测试人员发现隐藏接口、敏感路径等内容。

---

## ✨ 功能特点

- 🚀 自动提取响应中的接口路径
- 🧠 过滤无用路径（数字路径、资源文件路径等）
- 🖱️ 通过右键菜单一键执行提取
- 📋 支持复制所有结果、清空等功能
- 📌 以 Burp Suite 标签页形式展示

---

## 📦 安装使用

### 1. 环境准备
请使用 **Jython 2.7.x** 将该插件以 `.py` 格式加载进 Burp Suite。

> 注：Jython 下载地址：[https://www.jython.org/download](https://www.jython.org/download)

### 2. 加载插件

1. 打开 Burp Suite
2. 点击 `Extender` > `Extensions`
3. 选择 `Add`
4. `Extension type` 选择 `Python`
5. 加载本插件脚本文件 `apifinderv1.0.py`

### 3. 使用方法

1. 在 Burp 中抓取 HTTP 请求
2. 右键选择 `find endpoints`
3. 打开 `Juicy endPoints` 标签页查看提取结果
4. 使用 `copy all` 复制所有接口路径，或 `clear` 清空结果

---

## 📖 示例截图

> 这里你可以上传截图显示插件在 Burp 中的界面效果。

---

## 🔍 提取规则说明

- 仅提取以 `/` 开头的路径
- 排除纯数字路径，如 `/123`
- 排除资源型路径，如 `.js`, `.css`, `.png`, `.jpg`, `.ico`, `.svg`, `.woff`, `.ttf` 等

---

## 👨‍💻 作者信息

- 👤 作者：yanglittlecat
- 📫 GitHub: [@yanglittlecat](https://github.com/yanglittlecat)

---

## 📝 License

本项目使用 MIT 许可证开源发布，欢迎使用、修改与分发。
