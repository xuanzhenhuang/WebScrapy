# 🔎 ***Multi-source Data Crawling and Intelligent Analysis System***
This is a crawler project written in Python. It fetches product data from websites such as IKEA, Amazon, RUSTA, and TARGET, and provides convenient data analysis reports. Meanwhile, it deploys models locally to build a knowledge base, offering strong support for enterprise decision - making and significantly improving work efficiency!

<div align="center" style="margin-top:20px;margin-bottom:20px;">
<img src="https://github.com/xuanzhenhuang/WebScrapy/blob/main/images/FInereport.png?raw=true" width="1000px">
</div>
<div align="center" style="margin-top:20px;margin-bottom:20px;">
<img src="https://github.com/xuanzhenhuang/WebScrapy/blob/main/images/DeepSeek2.png?raw=true" width="1000px">
</div>

<p align="center">
   <a href="./README.md">Simplified Chinese</a> |
   <a href="./README_en.md">English</a>
</p>

<details open>
<summary><b>📕 Table of Contents</b></summary>

- 🛠 [Intelligent Data Crawler | High - efficiency Multi - platform Data Collection Solution](#-intelligent-data-crawler-|-high-efficiency-multi-platform-data-collection-solution)
- 🌱 [Project Process](#-project-process)
- 🌟 [Project Highlights](#-project-highlights)
- 🚀 [Quick Start](#-quick-start)
- 📜 [Prerequisites](#-prerequisites)
- 📌 [Execution Order](#-execution-order)
- 🔧 [Technical Architecture and Optimization](#-technical-architecture-and-optimization)
- 🔨 [Core Functions](#-core-functions)
- 📦 [Use Cases](#-use-cases)

</details>

---

🛠 **Intelligent Data Crawler | High - efficiency Multi - platform Data Collection Solution**  

In today's digital business environment, enterprises are faced with a vast amount of scattered data. For suppliers, understanding the pricing and customer feedback of similar products on different platforms and in different countries is crucial for optimizing operational strategies and enhancing competitiveness. However, crawling multi - source data faces challenges from anti - crawling mechanisms, and the complexity of data processing and integration is relatively high. Traditional pricing and decision - making methods are inefficient and lack precision. Therefore, developing a multi - source data crawling and intelligent analysis system has important practical significance.

This project aims to integrate multiple advanced technologies to build automated data collection code based on Python, supporting the collection of product data from websites such as **IKEA, Amazon, TARGET, and RUSTA**, including structured data such as prices, inventory, descriptions, images, and reviews. After multiple rounds of architecture optimization, the project is suitable for large - scale data collection and business analysis scenarios. It realizes efficient crawling, in - depth analysis, and intelligent application of multi - source supermarket data, helping enterprises make data - driven decisions and improve operational efficiency and pricing accuracy.

---

### 📚 Project Process

1. **Multi - source Data Crawling**  
    Use Python and Drissionpage to crawl data from large supermarket platforms such as IKEA, AMAZON, RUSTA, and TARGET. For dynamically loaded pages, analyze the offset pagination rules and obtain key information by monitoring data packet capture. Design random request headers, dynamic waiting (a combination of short and long pauses), and batch - writing mechanisms. Set up page exception refresh handling to save breakpoints when crawling is interrupted due to network fluctuations, avoiding repeated crawling. Ensure the integrity of data crawling through log monitoring and exception alerts. Improve crawling efficiency through multi - threading and asynchronous operations.

2. **Data Cleaning and Preprocessing**  
    Clean the crawled data based on Python, removing noisy data, handling missing values, and standardizing data formats to prepare for subsequent analysis and visualization.

3. **Data Analysis and Visualization**  
    Develop dynamic reports using FineReport, implementing functions such as parent - child cell linkage and parameter passing. Integrate real - time exchange rate APIs and fast translation functions to achieve automatic conversion and visual display of product prices, reducing manual intervention.

4. **Local AI Deployment and Knowledge Base Construction**  
    Deploy the local large - language model DeepSeek based on Ollama + Docker + RagFlow. Analyze the sentiment polarity of reviews by combining the fine - tuned BERT model. Build a private knowledge base containing over 100,000 structured data records to support quick retrieval and intelligent pricing.

5. **Automated Tool Development and Task Scheduling**  
    Package the crawler and data analysis scripts into executable files using pyinstaller. Use the task scheduler to regularly crawl the latest data and automatically generate data analysis reports to support enterprise decision - making.

---

### 🌟 Project Highlights

1. **Efficient Data Crawling and Anti - crawling Strategies**  
    Through optimized anti - crawling mechanisms and multi - threaded asynchronous operations, high - integrity and high - efficiency data crawling is achieved, solving the problem of multi - source data acquisition.

2. **Comprehensive Data Analysis and Visualization**  
    By combining multiple tools and technologies, in - depth data analysis and intuitive visual display are realized, reducing manual workload and improving decision - making efficiency.

3. **Local AI and Knowledge Base Application**  
    Locally deploy large - language models and build a private knowledge base in combination with sentiment analysis, providing support for intelligent pricing and precise decision - making for enterprises.

4. **Automation and Convenience**  
    Package scripts into executable files and implement scheduled tasks and automatic report generation, improving the usability and practicality of the system.

## 🚀 Quick Start

### 📜 Prerequisites

- Python environment (Python 3.7 or higher is recommended).
- Install Drissionpage, FineReport 9.0, transformers (for the BERT model), Ollama, Docker, etc.
- Ensure that there are sufficient system resources for running Docker containers and model deployment.
- PyTorch (You can install it on the [PyTorch official website](https://pytorch.org/) according to your computer's configuration).
- CUDA (If you have a GPU and want to use it to accelerate model training, you need to install CUDA yourself).
- bert - base - uncased (You can download the model to your local machine from the [huggingface official website](https://huggingface.co/google - bert/bert - base - uncased)).
  > If you can't access the huggingface official website, you can also install it from the [mirror site](https://hf - mirror.com/).

### 📌 Execution Order

1. **Environment Setup**  
    Install the required Python libraries and tools, configure the SQL Server database, and start the Docker service.

2. **Data Crawling**  
    Run the data crawling script to crawl multi - source supermarket data according to the configured parameters.

3. **Data Processing and Analysis**  
    Execute the data cleaning and preprocessing scripts, and then use FineReport for data analysis and visualization configuration.

### 🔧 **Technical Architecture and Optimization**  
1. **Dynamic Rendering and Efficiency Improvement**  
   - **Initial Solution**: Traverse product detail pages based on `Selenium`, which was improved due to significant speed bottlenecks.  
   - **Second - generation Optimization**: Replace Selenium with `DrissionPage` to reduce driver dependencies, and use `DataLoader` for structured storage.  
   - **Current Solution**: **Direct collection from the homepage + multi - threading acceleration**, bypassing the page - by - page loading process, increasing data collection efficiency by over 300%. Asynchronous `Requests` coroutines are used for image downloads.

2. **Anti - crawling Strategies and Stability**  
   - **Intelligent Request Regulation**: Random request headers (User - Agent rotation), dynamic intervals (0.5 - 3 seconds of operation delay, and a 10 - 30 - second sleep every 50 requests) to simulate real user behavior.  
   - **IP Protection Mechanism**: For high - security sites like TARGET, integrate a proxy IP pool (needs to be configured manually), with automatic retry for failed requests and abnormal circuit - breaking.  
   - **Page Parsing Fault Tolerance**: Dynamically adapt XPath and CSS selectors to handle changes in the website's DOM structure.

3. **Modular Expansion Design**  
   - Parsers (`parsers`), downloaders (`downloaders`), and pipelines (`pipelines`) are independently decoupled. Only the corresponding modules need to be implemented when adding new sites.  
   - Data output supports JSON/CSV/MySQL, and can be flexibly switched through `pipelines`.

4. **AI Deployment and Knowledge Base Construction**  
    Deploy the DeepSeek model based on Ollama and Docker, fine - tune the BERT model for sentiment analysis, and build a private knowledge base.

5. **Automated Task Setup**  
    Package the scripts into executable files using pyinstaller, and set up the task scheduler to regularly perform data crawling and report generation tasks.

### 🔨 **Core Functions**  
- **IKEA**: Batch collection on the homepage + multi - threading acceleration, bypassing the bottleneck of single - page access.  
- **TARGET**: Dynamic behavior simulation + hierarchical anti - crawling countermeasures to ensure the stability of long - term tasks.  
- **Automated Operation and Maintenance**: Regularly crawl the latest data and update the database and reports.

### 📦 **Use Cases**  
- Competitor price monitoring and dynamic pricing strategies.  
- Early warning of product inventory fluctuations.  
- Market trend analysis (review sentiment analysis, category popularity).  
- Building datasets for academic research.

<div align="center" style="margin-top:20px;margin-bottom:20px;">
<img src="https://github.com/xuanzhenhuang/WebScrapy/blob/main/images/DeepSeek.jpg?raw=true" width="1000px">
</div>
<div align="center" style="margin-top:20px;margin-bottom:20px;">
<img src="https://github.com/xuanzhenhuang/WebScrapy/blob/main/images/DeepSeek3.png?raw=true" width="1000px">
</div>
