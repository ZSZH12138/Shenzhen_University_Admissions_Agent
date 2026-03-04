# SZU Admission RAG – Data Construction Module



本模块用于构建深圳大学招生问答 Agent 的底层知识库数据，包含数据抓取、文本清洗、文本切分、向量化以及向量索引构建等完整流程。



注意：本模块 \*\*未集成自动化 pipeline\*\*，请用户根据需求按步骤逐个运行脚本。



---



## 文件说明



本目录包含以下脚本：



### get\_data.py

用于网页数据抓取。



**使用说明：**



- 在文件内部填写需要爬取的网址  

- 可使用 `get\_list\_page(root\_url)` 函数获取可爬取页面列表  

- 直接运行 `main()` 函数即可开始抓取  



```bash

python get\_data.py

```



**输出：**



`szu\_admission\_articles.json`



---

### clean\_data.py



用于调用 LLM 对原始文本进行清洗与结构优化。



```bash

python clean\_data.py

```



**需要：**

`szu\_admission\_articles.json`



**输出：**

`szu\_admission\_articles\_clean.json`



---

### cut\_data.py



用于按规则切分文本块，并生成 `chunk\_id`。



```bash

python cut\_data.py

```



**需要：**

`szu\_admission\_articles\_clean.json`





**输出：**

`szu\_admission\_chunks.json`



---

### embedding.py



用于：



- 生成向量 `.npy` 文件  

- 构建 FAISS 索引 `.index` 文件  



```bash

python embedding.py

```



**需要：**

`szu\_admission\_chunks.json`



**输出：**



szu\_admission.index  

szu\_embeddings.npy



---

## 运行顺序



请按如下顺序依次运行：



1. get\_data.py  

2. clean\_data.py  

3. cut\_data.py  

4. embedding.py  


本模块未集成自动 pipeline，请勿跳步骤运行。

