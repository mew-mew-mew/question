from flask import Flask, render_template, request

app = Flask(__name__)

# 临时数据库（存放在内存中）
# 注意：在真实生产环境中，建议后续升级为 SQLite 或 MySQL
results_db = []

# 15道题的标准答案字典 (对应你题库的 Answer Key)
ANSWER_KEY = {
    'q1': 'B', 'q2': 'C', 'q3': 'B', 'q4': 'C', 'q5': 'B',
    'q6': 'C', 'q7': 'C', 'q8': 'A', 'q9': 'B', 'q10': 'B',
    'q11': 'B', 'q12': 'D', 'q13': 'B', 'q14': 'B', 'q15': 'C'
}

@app.route('/')
def index():
    # 返回手机端答题页面
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # 获取考生姓名
    name = request.form.get('worker_name')
    
    # 判分逻辑
    correct_count = 0
    for q_id, correct_answer in ANSWER_KEY.items():
        # 获取用户选择的答案
        user_answer = request.form.get(q_id)
        if user_answer == correct_answer:
            correct_count += 1
            
    # 计算百分制得分 (答对题数 / 15 * 100)
    score = int((correct_count / 15) * 100)
    
    # 将成绩保存到数据库
    results_db.append({
        'name': name, 
        'score': score,
        'correct_count': f"{correct_count}/15"
    })
    
    # 返回结果给用户
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
    # 返回电脑端后台管理页面
    return render_template('admin.html', results=results_db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)