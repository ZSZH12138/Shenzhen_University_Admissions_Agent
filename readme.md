# SZU Admission Agent



本项目为一个基于检索增强生成（RAG, Retrieval-Augmented Generation）架构的深圳大学招生问答 Agent。系统通过向量检索结合大语言模型，实现对招生相关问题的精准回答。



---



## 项目结构说明



- `get\_data\_and\_embed/`  

&nbsp; 用于数据获取、文本切分与向量化处理。运行该目录下的代码后，会生成向量索引文件及文本切分文件。



- `admission\_agent/`  

&nbsp; 基于 Django 构建的 Web 应用，负责前端展示与后端问答逻辑处理。



---



## 使用步骤

### 一. 数据构建  


进入 `get\_data\_and\_embed` 文件夹，运行数据处理与向量化脚本：  

请根据文件夹中的 `readme.md` 完成相关操作  

运行完成后，将生成以下两个文件：  

`szu\_admission.index` —— 向量索引文件  

`szu\_admission\_chunks.json` —— 文本切分数据文件  



### 二. 文件放置

将生成的两个文件复制至以下目录：  

`admission\_agent/agent/`  



### 三. 启动 Django 项目



进入 `admission\_agent` 文件夹，根据文件夹中的 `readme.md` 完成相关操作。







