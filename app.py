import json
import os
import uuid  # 用于给每条数据生成唯一ID
from datetime import datetime  # 用于获取当前时间戳
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = 'results_db.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

ANSWER_KEY = {
    'q1': 'B', 'q2': 'C', 'q3': 'B', 'q4': 'C', 'q5': 'B',
    'q6': 'C', 'q7': 'C', 'q8': 'A', 'q9': 'B', 'q10': 'B',
    'q11': 'B', 'q12': 'D', 'q13': 'B', 'q14': 'B', 'q15': 'C'
}

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ... (上面的代码不用动，保留引入 json, os, uuid, datetime 和 load_data, save_data 等)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('worker_name')
    
    correct_count = 0
    for q_id, correct_answer in ANSWER_KEY.items():
        user_answer = request.form.get(q_id)
        if user_answer == correct_answer:
            correct_count += 1
            
    score = int((correct_count / 15) * 100)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    record_id = str(uuid.uuid4())
    
    current_data = load_data()
    current_data.append({
        'id': record_id,
        'timestamp': current_time,
        'name': name, 
        'score': score,
        'correct_count': f"{correct_count}/15"
    })
    save_data(current_data)
    
    # 【核心修复】：不要直接返回 HTML！
    # 将计算好的成绩作为参数，重定向到独立的 /success 页面
    return redirect(url_for('success', name=name, score=score, correct_count=correct_count))

# 【新增路由】：专门用来展示成功结果的独立页面
@app.route('/success')
def success():
    # 从网址 (URL) 中提取刚才传过来的名字和成绩
    name = request.args.get('name')
    score = request.args.get('score')
    correct_count = request.args.get('correct_count')
    
    return f"""
    <div style="font-family: sans-serif; text-align: center; padding: 50px;">
        <h2 style="color: #0056b3;">提交成功！</h2>
        <p style="font-size: 18px;"><b>{name}</b>，您的答卷已记录。</p>
        <p style="font-size: 24px; color: #28a745;">最终得分：<b>{score} 分</b></p>
        <p style="color: #666;">（共答对 {correct_count} 道题，总计 15 道）</p>
        <br>
        <p>您可以关闭此页面了。</p>
    </div>
    """

@app.route('/admin')
def admin():
    current_data = load_data()
    current_data.reverse() 
    return render_template('admin.html', results=current_data)

@app.route('/delete/<record_id>')
def delete_record(record_id):
    current_data = load_data()
    updated_data = [item for item in current_data if item.get('id') != record_id]
    save_data(updated_data)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)