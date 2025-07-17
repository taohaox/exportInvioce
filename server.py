from flask import Flask, request, send_file, jsonify, after_this_request
from flask_cors import CORS
import tempfile
import os
from app import generate_invoice_word
# AI相关导入
from openai import OpenAI

app = Flask(__name__)
# 只允许 https://export.gonyb.com 跨域访问
# 配置CORS
CORS(app, resources={
    r"/*": {
        "origins": ["https://export.gonyb.com","*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    },
    
})

# AI客户端初始化（可根据demo_ai.py调整）
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

@app.route('/export_invoice', methods=['POST'])
def export_invoice():
    data = request.json
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
        tmp_path = tmp.name

    @after_this_request
    def remove_file(response):
        try:
            os.remove(tmp_path)
        except Exception:
            pass
        return response

    generate_invoice_word(data, tmp_path)
    return send_file(tmp_path, as_attachment=True, download_name='invoice.docx')

@app.route('/recognize_address', methods=['POST'])
def recognize_address():
    data = request.json
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'success': False, 'message': '缺少输入文本'})
    prompt = f"""
请从如下文本中智能提取收件联系人、收件地址、收件电话、邮编，返回JSON格式：
{{
  'import_contact': '联系人',
  'import_address': '收件地址',
  'import_phone': '收件电话',
  'import_zip': '邮编'
}}
如果无法识别某项，值请留空。

文本：{text}
"""
    try:
        completion = client.chat.completions.create(
            model="deepseek-v3",
            messages=[{'role': 'user', 'content': prompt}]
        )
        import re, json
        # 尝试提取JSON
        content = completion.choices[0].message.content
        match = re.search(r'\{[\s\S]*\}', content)
        if match:
            result = match.group(0)
            # 替换单引号为双引号，兼容AI输出
            result = result.replace("'", '"')
            info = json.loads(result)
            # 如果所有字段都为空，提示不是有效地址
            if not any([info.get('import_contact','').strip(), info.get('import_address','').strip(), info.get('import_phone','').strip(), info.get('import_zip','').strip()]):
                return jsonify({'success': False, 'message': '未检测到有效的地址信息，请检查输入内容'})
            return jsonify({'success': True,
                            'import_contact': info.get('import_contact', ''),
                            'import_address': info.get('import_address', ''),
                            'import_phone': info.get('import_phone', ''),
                            'import_zip': info.get('import_zip', '')})
        else:
            return jsonify({'success': False, 'message': 'AI未能正确识别'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'AI接口异常: {e}'})

if __name__ == '__main__':
    app.run(debug=True, port=5001) 