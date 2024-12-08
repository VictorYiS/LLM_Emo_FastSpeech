import json
import sys
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import openai
from dotenv import load_dotenv
import os

from llm import SpeechSynthesizer

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取 OpenAI API 密钥和代理地址
openai.api_key = os.getenv("OPENAI_API_KEY")
proxy_url = os.getenv("PROXY_URL")
openai_engine = "gpt-3.5-turbo"

if not openai.api_key:
    print("错误: API key未找到。请在.env文件中设置OPENAI_API_KEY", file=sys.stderr)
    raise ValueError("API key not found. Please set OPENAI_API_KEY in your .env file.")

# Configure proxy globally
if proxy_url:
    os.environ["HTTP_PROXY"] = proxy_url
    os.environ["HTTPS_PROXY"] = proxy_url
    print(f"已配置代理: {proxy_url}")

synthesizer = SpeechSynthesizer()

app = Flask(__name__)
# CORS(app)

# 配置 Flask 的 JSON 响应
app.config['JSON_AS_ASCII'] = False  # 禁用 ASCII 编码


@app.route("/gpt", methods=["POST"])
def gpt_endpoint():
    data = request.json
    prompt = data.get("prompt")
    speaker = data.get("speaker", 0)  # 默认说话人
    emotion = data.get("emotion", "Neutral")  # 默认情感

    if not prompt:
        print("错误: 未提供prompt", file=sys.stderr)
        return jsonify({"error": "No prompt provided"}), 400

    try:
        print(f"\n[{datetime.now()}] 收到新请求:")
        print(f"Prompt: {prompt}")

        # 获取GPT响应
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Speak English"},
                *[
                    {"role": "user" if "user" in msg else "assistant", "content": msg.split(": ", 1)[1]}
                    for msg in prompt.split("\n")
                ],
            ],
            max_tokens=100,
            temperature=0.7,
        )

        result_text = response["choices"][0]["message"]["content"].strip()
        print(f"GPT响应文本: {result_text}")

        # 生成语音文件
        try:
            output_path = synthesizer.generate(result_text, emotion=emotion, speaker_id=speaker)
            # 将 Path 对象转换为字符串，并只保留文件名
            audio_filename = Path(output_path).name
            print(f"生成的音频文件名: {audio_filename}")

            # 返回包含文本和音频文件名的响应
            return jsonify({
                "response": result_text,
                "audio_path": audio_filename  # 只返回文件名
            })

        except Exception as e:
            print(f"语音生成错误: {str(e)}", file=sys.stderr)
            # 即使语音生成失败，也返回文本响应
            return jsonify({
                "response": result_text,
                "error": "Audio generation failed",
                "error_details": str(e)
            })

    except Exception as e:
        error_msg = str(e)
        print(f"GPT请求错误: {error_msg}", file=sys.stderr)
        return jsonify({"error": error_msg}), 500


# 添加获取音频文件的端点
@app.route("/audio/<path:filename>")
def get_audio(filename):
    try:
        # 使用 synthesizer 的 result_dir 作为音频目录
        audio_dir = Path(synthesizer.paths.result_dir)
        file_path = audio_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Audio file not found: {filename}")

        return send_file(
            str(file_path),  # 转换为字符串
            mimetype="audio/wav"  # 根据实际音频格式调整
        )
    except Exception as e:
        print(f"音频文件访问错误: {str(e)}", file=sys.stderr)
        return jsonify({"error": str(e)}), 404


if __name__ == "__main__":
    print(f"\n{'=' * 50}")
    print(f"启动服务器 - 时间: {datetime.now()}")
    print(f"运行于: http://0.0.0.0:5001")
    print(f"{'=' * 50}\n")
    app.run(debug=True, host="0.0.0.0", port=5001)