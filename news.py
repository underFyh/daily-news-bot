import os
import requests
from datetime import datetime

def get_news():
    print("正在获取知乎热榜...")
    # 更换为对 GitHub 服务器友好的第三方热搜聚合 API
    url = "https://api.vvhan.com/api/hotlist/zhihu"
    
    # 加上一个“伪装面具”，假装自己是普通浏览器，防止被拦截
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # 设置 10 秒超时，防止卡死
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        today = datetime.now().strftime("%Y-%m-%d")
        content = f"🔥 【知乎热榜】{today}\n\n"
        
        # 提取前 10 条热榜数据
        # 这个第三方 API 返回的数据列表在 'data' 字段里
        for index, item in enumerate(data.get('data', [])[:10]):
            content += f"{index + 1}. {item['title']}\n"
            
        content += "\n祝你今天有个好心情！☀️"
        return content
        
    except Exception as e:
        print(f"抓取新闻失败: {e}")
        return "⚠️ 获取新闻失败，请检查 API 接口状态。"

def push_to_wechat(content):
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
        "summary": "您的每日知乎热榜已送达！", 
        "contentType": 1, 
        "uids": [uid]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") == 1000:
            print("✅ 推送成功！请查看微信。")
        else:
            print(f"❌ 推送失败：{result}")
    except Exception as e:
        print(f"❌ 请求 WxPusher 失败: {e}")

if __name__ == "__main__":
    news_content = get_news()
    push_to_wechat(news_content)
