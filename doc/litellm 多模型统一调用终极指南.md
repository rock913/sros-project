1. 为什么选择 litellm？
在现代 AI 应用开发中，我们常常需要测试和集成来自不同厂商的语言模型（LLM）。例如，OpenAI 的 GPT 系列在通用能力上很强，而通义千问（Qwen）在中文处理上可能有优势，SiliconFlow 则提供了高性价比的开源模型推理服务。

但问题是，每个服务商都有自己独特的 API 接口、SDK 和认证方式。如果为每个模型都写一套独立的调用逻辑，代码会变得非常冗余、难以维护，并且在模型之间切换时成本很高。

litellm 就是解决这个问题的“瑞士军刀”。

它提供了一个与 OpenAI API 完全兼容的统一接口，让你能够用完全相同的代码格式来调用超过 100 种不同的 LLM。你只需要改变一个 model 参数，就可以无缝地在 OpenAI, Azure, Cohere, Anthropic, Replicate, HuggingFace, 以及像通义千问、SiliconFlow 这样的国内优秀服务之间切换。

核心优势:

代码一致性: 使用一套代码逻辑调用所有模型。

轻松切换: 只需更改模型名称字符串即可切换模型。

简化认证: 通过标准化的环境变量简化 API 密钥管理。

统一输出: 返回与 OpenAI 一致的数据结构，方便解析。

2. 基础准备：安装与 API Key 配置
在开始之前，请先完成以下两个步骤。

2.1 安装 litellm
打开你的终端或命令行，运行以下 pip 命令：

pip install litellm

2.2 配置 API 密钥（重要！）
litellm 的一大便利之处在于它会自动从环境变量中读取 API 密钥。这是管理密钥的最佳实践，可以避免将敏感信息硬编码在代码中。

请根据你计划使用的服务，设置对应的环境变量：

对于 OpenAI:

export OPENAI_API_KEY="sk-..." 

对于通义千问 (Qwen on DashScope):

注意: Qwen 的官方服务托管在阿里云的“灵积模型服务”（DashScope）上。因此，litellm 通过 dashscope 这个 provider 来调用它。

export DASHSCOPE_API_KEY="sk-..." 

对于 SiliconFlow:

export SILICONFLOW_API_KEY="sk-..."

提示: 你可以将以上 export 命令添加到你的 ~/.bashrc, ~/.zshrc 或其他 shell 配置文件中，这样每次打开新的终端时它们都会自动加载。

3. 实践教程：统一调用文本生成模型
我们将使用 litellm.completion() 函数，这是调用所有文本生成模型的核心。

3.1 定义统一的调用函数
我们可以封装一个简单的函数，通过传入不同的 model 名称来实现模型切换。

import litellm
import os

# 推荐：在调试时开启详细日志，可以看到 litellm 构造的请求细节
litellm.set_verbose=True

def generate_text(model_name, user_prompt):
    """
    使用 litellm 统一调用各类文本生成模型。
    
    参数:
    model_name (str): litellm 格式的模型名称 (e.g., "gpt-3.5-turbo", "dashscope/qwen-turbo")
    user_prompt (str): 用户输入的问题
    
    返回:
    str: 模型生成的文本内容
    """
    messages = [
        {"role": "system", "content": "你是一个乐于助人的 AI 助手。"},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        print(f"\n----- 正在调用模型: {model_name} -----")
        response = litellm.completion(
            model=model_name,
            messages=messages
        )
        # litellm 返回的是一个 ModelResponse 对象，其结构与 OpenAI 的返回一致
        content = response.choices[0].message.content
        print(f"模型输出: {content}")
        return content
    except Exception as e:
        print(f"调用模型 {model_name} 时发生错误: {e}")
        return None

# --- 使用示例 ---
prompt = "请给我介绍一下长城。"

# 1. 调用 OpenAI
generate_text("gpt-3.5-turbo", prompt)

# 2. 调用通义千问
# 注意：模型名称需要加上 provider 前缀 "dashscope/"
generate_text("dashscope/qwen-turbo", prompt)

# 3. 调用 SiliconFlow 上的开源模型 (以 Qwen-7B-Chat 为例)
# 注意：模型名称需要加上 provider 前缀 "siliconflow/"
# 你需要去 SiliconFlow 平台确认具体的模型标识符
generate_text("siliconflow/alibaba-cloud/qwen-7b-chat", prompt)

代码解析:

你可以看到，无论是调用哪个模型，litellm.completion() 的参数和使用方式完全一样。

切换模型的唯一操作就是改变 model 参数的字符串。

litellm 会根据模型名称的前缀（如 dashscope/ 或 siliconflow/）自动路由到正确的 API 端点，并使用对应的环境变量（DASHSCOPE_API_KEY, SILICONFLOW_API_KEY）进行认证。对于没有前缀的 gpt-3.5-turbo，它会默认使用 openai。

4. 实践教程：统一调用 Embedding 模型
同样地，我们可以使用 litellm.embedding() 函数来统一调用各类 Embedding 模型。

4.1 定义统一的 Embedding 函数
import litellm
import os

# 推荐：开启详细日志
litellm.set_verbose=True

def get_embeddings(model_name, texts):
    """
    使用 litellm 统一调用各类 Embedding 模型。
    
    参数:
    model_name (str): litellm 格式的模型名称
    texts (list): 需要进行 embedding 的文本列表
    
    返回:
    list: 向量列表
    """
    try:
        print(f"\n----- 正在调用 Embedding 模型: {model_name} -----")
        response = litellm.embedding(
            model=model_name,
            input=texts
        )
        # 提取 embedding 向量
        embeddings = [item.embedding for item in response.data]
        
        print(f"成功为 {len(embeddings)} 段文本生成向量。")
        print(f"第一个向量的维度: {len(embeddings[0])}")
        return embeddings
    except Exception as e:
        print(f"调用 Embedding 模型 {model_name} 时发生错误: {e}")
        return None

# --- 使用示例 ---
text_list = ["你好，世界", "这是一个 litellm 教程"]

# 1. 调用 OpenAI Embedding
get_embeddings("text-embedding-3-small", text_list)

# 2. 调用通义千问 Embedding
# 注意 provider 前缀
get_embeddings("dashscope/text-embedding-v1", text_list)

# 3. 调用 SiliconFlow Embedding (以 bge-large-zh-v1.5 为例)
# 注意 provider 前缀
get_embeddings("siliconflow/bge-large-zh-v1.5", text_list)

代码解析:

和文本生成一样，litellm.embedding() 的调用方式对所有模型保持一致。

你只需要更改 model 参数，就可以在 OpenAI, 通义千问, SiliconFlow 等不同平台的 Embedding 模型之间自由切换，而无需改动任何其他代码。

5. 总结与项目集成建议
通过以上教程，你可以看到 litellm 的强大之处。在你的项目中，可以这样进行集成：

模型配置: 在项目的配置文件（如 config.yaml 或 settings.py）中定义一个模型列表，方便管理。

# settings.py
AVAILABLE_GENERATION_MODELS = {
    "openai_gpt3.5": "gpt-3.5-turbo",
    "qwen_turbo": "dashscope/qwen-turbo",
    "siliconflow_qwen": "siliconflow/alibaba-cloud/qwen-7b-chat"
}

AVAILABLE_EMBEDDING_MODELS = {
    "openai": "text-embedding-3-small",
    "qwen": "dashscope/text-embedding-v1",
    "siliconflow_bge": "siliconflow/bge-large-zh-v1.5"
}

动态调用: 在你的业务逻辑中，根据配置或用户选择，动态地传入对应的模型名称字符串给 litellm 函数。

from settings import AVAILABLE_GENERATION_MODELS

# 假设用户选择了 "qwen_turbo"
selected_model_key = "qwen_turbo"
model_to_use = AVAILABLE_GENERATION_MODELS[selected_model_key]

# 直接调用
generate_text(model_to_use, "今天天气怎么样？")

这种方式让你的应用具备了极高的灵活性，可以随时引入新的模型服务或在不同模型间进行 A/B 测试，而无需重构核心代码。