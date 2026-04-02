import os
import requests
from datetime import datetime

def get_news():
    print("正在获取知乎日报...")
    url = "https://news-at.zhihu.com/api/4/news/latest"
    response = requests.get(url)
    data = response.json()
    
    today = datetime.now().strftime("%Y-%m-%d")
    content = f"📰 【知乎早报】{today}\n\n"
    
    # 提取前 10 条新闻标题
    for index, story in enumerate(data.get('stories', [])[:10]):
        content += f"{index + 1}. {story['title']}\n"
        
    content += "\n祝你今天有个好心情！☀️"
    return content

def push_to_wechat(content):
    # 从 GitHub Secrets 中读取我们刚才存的钥匙
    app_token = os.environ.get("WXPUSHER_APP_TOKEN")
    uid = os.environ.get("WXPUSHER_UID")
    
    if not app_token or not uid:
        print("❌ 错误：找不到 WxPusher 的配置信息，请检查 GitHub Secrets！")
        return

    print("正在推送到微信...")
    url = "https://wxpusher.zjiecode.com/api/send/message"
    payload = {
        "appToken": app_token,
        "content": content,
        "summary": "您的每日知乎早报已送达！", # 微信列表里显示的摘要
        "contentType": 1, # 1表示纯文本
        "uids": [uid]
    }
    response = requests.post(url, json=payload)
    result = response.json()
    
    if result.get("code") == 1000:
        print("✅ 推送成功！请查看微信。")
    else:
        print(f"❌ 推送失败：{result}")

if __name__ == "__main__":
    news_content = get_news()
    push_to_wechat(news_content)
