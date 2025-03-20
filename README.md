# Zlib Mail to R2 AutoUploader  
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)  

自动下载 Z-Library 邮件附件并上传到 R2 存储桶的自动化脚本  

---

## 📌 项目概述  
本项目通过 GitHub Actions 实现以下功能：  
1. **自动化邮件处理**：每1分钟自动登录 Gmail，下载主题为 `Z-Library` 的邮件附件  
2. **存储上传**：将附件上传到兼容 S3 API 的 R2 存储桶（如 DigitalOcean Spaces）  
3. **日志记录**：全程记录操作日志，便于排查问题  
4. **环境隔离**：通过 GitHub Secrets 安全管理敏感信息  

---

## 🛠️ 环境要求  
| 组件 | 说明 |
|------|------|
| **Python** | 3.x 版本（由 GitHub Actions 管理） |
| **R2 存储桶** | 需配置 S3 兼容 API 的存储服务（如 AWS S3、DigitalOcean Spaces） |
| **Gmail 账户** | 需开启 IMAP 和应用专用密码（两步验证必需） |

---

## 🚀 快速开始  
### 1. 配置环境变量  
在 GitHub 仓库的 **Settings > Secrets and variables > Actions** 中添加以下变量：  

| 变量名 | 说明 |
|--------|------|
| `access_key_id` | R2 存储桶的访问密钥 |
| `secret_access_key` | R2 存储桶的密钥 |
| `endpoint_url` | R2 存储桶的访问地址（如 `https://nyc3.digitaloceanspaces.com`） |
| `bucket_name` | 目标存储桶名称 |
| `username` | Gmail 登录邮箱 |
| `password` | Gmail 应用专用密码（[生成方法](https://support.google.com/accounts/answer/185833)） |

---

### 2. 配置 Gmail IMAP  
1. 登录 Gmail → **安全设置** → 启用 **两步验证**  
2. 进入 **App Passwords** 生成应用专用密码（适用于 R2 脚本）  
3. 在 **转发和 POP/IMAP** 设置中启用 **IMAP**  

---

### 3. 启动自动化
部署后将按以下规则自动执行：  

## 📂 文件结构
zlib_mail_r2/  
├── zlib_save_r2.py       # 核心处理脚本  
├── .github/              # GitHub Actions 配置目录  
│   └── workflows/  
│       └── main.yml      # 自动化工作流配置  
├── README.md             # 当前文档  
└── requirements.txt      # 依赖版本锁定（可选）  

---

## 📝 版本日志  
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2024-03-01 | 初始版本发布 |
| v1.1 | 2024-03-05 | 优化日志格式，修复附件名称解析问题 |

---

## 🤝 贡献指南  
1. Fork 本仓库  
2. 创建新分支 (`git checkout -b feature/your-feature`)  
3. 提交代码 (`git commit -m '描述你的修改'`)  
4. Push 到你的仓库 (`git push origin feature/your-feature`)  
5. 提交 Pull Request  

---

## 📝 许可证  
MIT License  

---

## 📌 待办事项  
- [ ] 添加上传失败重试机制  
- [ ] 支持多存储桶配置  
- [ ] 添加附件类型过滤（仅处理 PDF/EPUB）  
- [ ] 生成详细操作报告  

---

通过以上配置，你可以完全自动化 Z-Library 邮件附件的归档流程。如需进一步帮助，请提交 Issue！  
💡 **安全提示**：请勿在代码或公开仓库中直接存储敏感信息，始终使用 GitHub Secrets 或环境变量管理。
