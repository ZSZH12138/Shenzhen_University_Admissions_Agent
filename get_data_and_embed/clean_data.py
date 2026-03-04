from openai import OpenAI
import json
from tqdm import tqdm

client = OpenAI(
    api_key="", # 这是一个LLM清洗数据的文件 请输入自己持有的LLM API
    base_url=""
)

def get_answer(context,url):
    prompt = f"""
            你是一名专业的文本修复与结构化助手。

            我将向你提供一段通过正规渠道爬取的网页文本，该文本可能在爬取或解析过程中受到破坏，例如：
            - 出现多余或错误的换行符（如大量 \\n）
            - 段落被错误切分
            - 表格结构丢失或被打散为零碎文本
            - 列表、编号、标题层级混乱

            请你按照以下步骤处理文本：

            【处理步骤】
            1. 判断文本是否存在明显结构性损坏。
            2. 如果文本基本完整：
               - 在不改变原意的前提下，整理段落结构
               - 合理合并或拆分段落
               - 输出可直接用于下游 AI 处理的干净文本
            3. 如果文本存在明显损坏但可以修复：
               - 尝试恢复合理的段落结构
               - 将表格或列表内容改写为清晰、无歧义的自然语言描述
            4. 如果文本严重损坏，无法可靠修复：
               - 请基于我提供的原文 URL，对该页面内容进行客观、中立的总结
               - 明确说明这是“基于原网页的总结”

            【输出要求】
            - 使用简体中文
            - 输出应为结构清晰的连续文本，按语义合理分段
            - 不要添加原文中不存在的事实
            - 不需要解释你的处理过程，只输出最终文本结果

            【原文 URL】
            {url}

            【待处理文本】
            {context}
        """
    # 调用
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一名专业的文本修复与结构化助手。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )
    return response.choices[0].message.content

if __name__=="__main__":
    with open("szu_admission_articles.json",'r',encoding="utf-8") as f:
        items=json.load(f)
    results=[]
    for item in tqdm(items):
        new_str=get_answer(item["content"],item["url"])
        results.append({"url":item["url"],"title":item["title"],"content":new_str})
    with open("szu_admission_articles_clean.json",'w') as f:
        json.dump(results,f)