# 🔎 ***Multi-source Data Crawling and Intelligent Analysis System***
用Python编写的爬虫项目，抓取了包括宜家、亚马逊、RUSTA、TARGET等网站在内的商品数据，提供便捷化的数据分析报表，同时本地化部署模型构建知识库，为企业决策提供有力支持，大幅提升工作效率！

<div align="center" style="margin-top:20px;margin-bottom:20px;">
<img src="https://github.com/xuanzhenhuang/WebScrapy/blob/main/images/FInereport.png?raw=true" width="1000px">
</div>
<div align="center" style="margin-top:20px;margin-bottom:20px;">
<img src="https://github.com/xuanzhenhuang/WebScrapy/blob/main/images/DeepSeek2.png?raw=true" width="1000px">
</div>

<p align="center">
   <a href="./README.md">简体中文</a> |
   <a href="./README_en.md">English</a>
</p>

<details open>
<summary><b>📕 Table of Contents</b></summary>

- 🛠 [智能数据爬虫 | 多平台高效采集方案](#-智能数据爬虫-|-多平台高效采集方案)
- 🌱 [项目流程](#-项目流程)
- 🌟 [项目亮点](#-项目亮点)
- 🚀 [快速开始](#-快速开始)
- 📜 [前提条件](#-前提条件)
- 📌 [执行顺序](#-执行顺序)
- 🔧 [技术架构与优化](#-技术架构与优化)
- 🔨 [核心功能](#-核心功能)
- 📦 [使用场景](#-使用场景)


</details>

---

🛠 **智能数据爬虫 | 多平台高效采集方案**  

在当今数字化商业环境中，企业面临着海量且分散的数据。对于供应商而言，了解同类产品在不同平台和国家的定价以及客户反馈，对于优化运营策略和提升竞争力至关重要。然而，多源数据的爬取面临着反爬机制的挑战，数据处理和整合的复杂性也较高。传统的定价和决策方式效率低下且缺乏精准性。因此，开发一个多源数据爬取与智能化分析系统具有重要的现实意义。

本项目旨在通过整合多种先进技术，基于Python构建自动化数据采集代码，支持**IKEA（宜家）、Amazon、TARGET、RUSTA**等网站的商品数据抓取，涵盖价格、库存、描述、图片及评论等结构化数据。项目经历多次架构优化，适用于大规模数据采集与商业分析场景。实现了针对多源商超数据的高效爬取、深度分析和智能应用，帮助企业实现数据驱动的决策，提升运营效率和定价准确性。

---

### 📚 项目流程

1. **多源数据爬取**  
    运用 Python 和 Drissionpage 对 IKEA、AMAZON、RUSTA、TARGET 等大型商超平台进行数据爬取。针对动态加载页面，解析 offset 翻页规律，通过监听数据抓包获取关键信息。设计随机请求头、动态等待（短停 + 长停组合）及分批次写入机制，同时设置页面异常刷新处理，保存因网络波动导致抓取中断的断点，避免重复爬取。结合日志监控和异常报警，确保数据抓取完整率。利用多线程和异步获取操作提升抓取效率。

2. **数据清洗与预处理**  
    基于 Python 对爬取到的数据进行清洗，去除噪声数据、处理缺失值、统一数据格式等，为后续的分析和可视化做准备。

3. **数据分析与可视化**  
    使用 FineReport 开发动态报表，实现父子格联动、参数传参等功能。集成实时汇率 API 和快速翻译功能，实现商品价格的自动化换算和可视化展示，减少人工干预。

4. **本地 AI 部署与知识库构建**  
    基于 Ollama + Docker + RagFlow 部署本地大语言模型 DeepSeek。结合微调后的 BERT 模型分析评论的情感极性。将处理后的数据构建成包含 10 万 + 条结构化数据的私有知识库，支持快速检索和智能定价。

5. **自动化工具开发与任务调度**  
    使用 pyinstaller 将爬虫和数据分析脚本封装为可执行文件。利用任务计划程序定期抓取最新数据，并自动生成数据分析报告，为企业决策提供支持。

---

### 🌟 项目亮点

1. **高效的数据爬取与反爬策略**  
    通过优化的反爬机制和多线程异步操作，实现了高完整率和高效率的数据爬取，解决了多源数据获取的难题。

2. **全面的数据分析与可视化**  
    结合多种工具和技术，实现了数据的深度分析和直观可视化展示，减少了人工工作量，提升了决策效率。

3. **本地 AI 与知识库应用**  
    本地化部署大语言模型，结合情感分析构建私有知识库，为企业提供了智能定价和精准决策的支持。

4. **自动化与便捷性**  
    封装脚本为可执行文件，实现定时任务和自动报告生成，提高了系统的易用性和实用性。

## 🚀 快速开始

### 📜 前提条件

- Python 环境（建议 Python 3.7 及以上）
- 安装 Drissionpage、FineReport9.0、transformers（用于 BERT 模型）、Ollama、Docker 等。
- 确保有足够的系统资源用于运行 Docker 容器和模型部署。
- PyTorch（可以根据自己电脑的配置情况在[PyTorch官网](https://pytorch.org/)安装）
- CUDA（如果有GPU并且想要用于加速模型训练的话需要自行安装一下CUDA）
- bert-base-uncased(可以在[huggingface官网](https://huggingface.co/google-bert/bert-base-uncased)将模型下载到本地)
  > 如果没有办法访问到huggingface官网的话也可以在 [镜像站](https://hf-mirror.com/) 自行安装。

### 📌 执行顺序

1. **环境搭建**  
    安装所需的 Python 库和工具，配置 SQL Server 数据库，启动 Docker 服务。

2. **数据爬取**  
    运行数据爬取脚本，根据配置的参数爬取多源商超数据。

3. **数据处理与分析**  
    执行数据清洗和预处理脚本，然后使用 FineReport 进行数据分析和可视化配置。

### 🔧 **技术架构与优化**  
1. **动态渲染与效率提升**  
   - 初代方案：基于`Selenium`遍历产品详情页，因速度瓶颈显著改进。  
   - 二代优化：采用`DrissionPage`替代Selenium，减少驱动依赖，结合`DataLoader`实现结构化存储。  
   - **当前方案**：**首页直采+多线程加速**，绕过逐页加载环节，数据采集效率提升300%+，图片下载使用异步`Requests`协程处理。

2. **反爬策略与稳定性**  
   - **智能请求调控**：随机请求头(User-Agent轮换)、动态间隔（0.5-3秒操作延迟，每50请求休眠10-30秒），模拟真实用户行为。  
   - **IP保护机制**：针对TARGET等高防护站点，集成代理IP池（需自行配置），失败请求自动重试与异常熔断。  
   - **页面解析容错**：XPath与CSS选择器动态适配，应对网站DOM结构变更。

3. **模块化扩展设计**  
   - 解析器(`parsers`)、下载器(`downloaders`)、管道(`pipelines`)独立解耦，新增站点仅需实现对应模块。  
   - 数据输出支持JSON/CSV/MySQL，通过`pipelines`灵活切换。

4. **AI 部署与知识库构建**  
    基于 Ollama 和 Docker 部署 DeepSeek 模型，微调 BERT 模型进行情感分析，构建私有知识库。

5. **自动化任务设置**  
    使用 pyinstaller 封装脚本为可执行文件，设置任务计划程序定期执行数据抓取和报告生成任务。

### 🔨 **核心功能**  
- **宜家（IKEA）**：首页批量采集+多线程加速，绕过单页访问瓶颈  
- **TARGET**：动态行为模拟+分级反爬对抗，保障长周期任务稳定性  
- **自动化运维**：定期爬取最新数据并更新数据库以及报表 

### 📦 **使用场景**  
- 竞品价格监控与动态调价策略  
- 商品库存波动预警  
- 市场趋势分析（评论情感分析、品类热度）  
- 学术研究数据集构建  

<div align="center" style="margin-top:20px;margin-bottom:20px;">
<img src="https://github.com/xuanzhenhuang/WebScrapy/blob/main/images/DeepSeek.jpg?raw=true" width="1000px">
</div>
<div align="center" style="margin-top:20px;margin-bottom:20px;">
<img src="https://github.com/xuanzhenhuang/WebScrapy/blob/main/images/DeepSeek3.png?raw=true" width="1000px">
</div>
