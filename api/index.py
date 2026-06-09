import streamlit as st
import random
import os

# ---------------------------------------------------------
# Vercel 适配部分
# Vercel 的 Python 运行时需要寻找一个名为 "app", "application" 或 "handler" 的顶层对象。
# ---------------------------------------------------------

class VercelApp:
    def __init__(self):
        pass
    def __call__(self, environ, start_response):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return [b"Streamlit app is initialized. Please ensure your deployment platform supports WebSocket for Streamlit."]

# 定义 Vercel 识别的 app 对象
app = VercelApp()

# ---------------------------------------------------------
# Streamlit 应用主逻辑
# ---------------------------------------------------------

def run_streamlit_app():
    # 设置页面配置
    st.set_page_config(page_title="PP薄壁材料和注塑技术知识库", layout="centered")

    # 1. 界面上方显示大标题
    st.title("PP薄壁材料和注塑技术知识库")

    # 初始化聊天记录
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 显示聊天记录
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 专业知识关键词
    PROFESSIONAL_KEYWORDS = [
        "PP", "聚丙烯", "薄壁", "注塑", "注射", "模具", "压力", "速度", "温度", "收缩", 
        "绿色", "供应链", "碳中和", "循环", "回收", "降解", "材料", "成型", "缺陷", "翘曲"
    ]

    def is_professional_question(question):
        """判断是否为专业问题"""
        return any(keyword.lower() in question.lower() for keyword in PROFESSIONAL_KEYWORDS)

    def get_professional_response(question):
        """模拟专业解答逻辑"""
        responses = [
            "PP（聚丙烯）在薄壁注塑中具有极佳的流动性，但需要严格控制注射速度和保压压力以防止翘曲。",
            "绿色供应链的核心在于从材料选择到回收利用的全生命周期管理，PP材料的循环再生是其中的关键环节。",
            "薄壁注塑技术要求模具具有极高的强度和精密的排气系统，以应对高速高压的注射环境。",
            "在注塑工艺中，提高熔体温度可以降低粘度，有利于薄壁件的充填，但要注意材料的热降解风险。",
            "绿色供应链管理（GSCM）可以显著降低企业的碳足迹，通过优化物流和采用环保材料实现可持续发展。"
        ]
        return random.choice(responses) + f"\n\n（针对您的提问：'{question}'，这是基于知识库的专业分析。）"

    # 2. 聊天对话框交互逻辑
    if prompt := st.chat_input("请输入您关于薄壁注塑或绿色供应链的问题..."):
        # 显示用户输入
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 调用特定逻辑进行解答
        with st.chat_message("assistant"):
            if is_professional_question(prompt):
                response = get_professional_response(prompt)
            else:
                # 3. 交互规则：非专业问题的幽默拒绝
                response = "专注学习才是你最美的样子！让我们回到好玩的注塑世界吧！"
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# 运行应用
if __name__ == "__main__":
    run_streamlit_app()
else:
    # 当被 Vercel 或其他模块加载时运行
    run_streamlit_app()
