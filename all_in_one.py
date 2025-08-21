from flask import Flask, render_template_string

app = Flask(__name__)

# 导航主页
NAV_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>工具导航</title>
    <style>
        :root {
            --primary: #2c3e50;
            --accent: #3498db;
            --background: #f8f9fa;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 2rem;
            background: var(--background);
            min-height: 100vh;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            margin-bottom: 3rem;
        }

        h1 {
            color: var(--primary);
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 300;
        }

        .tool-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            padding: 1rem;
        }

        .tool-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            border: 1px solid rgba(0,0,0,0.05);
        }

        .tool-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }

        .tool-card h2 {
            color: var(--accent);
            margin: 1rem 0 0.5rem;
            font-weight: 500;
        }

        .tool-icon {
            font-size: 2.5rem;
            color: var(--primary);
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>工具集合</h1>
            <p style="color: #7f8c8d">精选实用小工具</p>
        </div>

        <div class="tool-grid">
            <a href="/divination" class="tool-card">
                <div class="tool-icon">☯</div>
                <h2>六爻占卜</h2>
                <p style="color: #95a5a6">易经智慧预测</p>
            </a>

            <a href="/calculator" class="tool-card">
                <div class="tool-icon">⧻</div>
                <h2>科学计算器</h2>
                <p style="color: #95a5a6">高效数学运算</p>
            </a>
        </div>
    </div>
</body>
</html>
'''

# 六爻工具
DIVINATION_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>赛博算命</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --primary-color: rgba(255, 255, 255, 0.15);
            --text-color: #333;
        }

        body {
            min-height: 100vh;
            margin: 0;
            padding: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            background: linear-gradient(45deg, #f3f4f6, #f9fafb);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        .container {
            width: 100%;
            max-width: 500px;
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        h1 {
            color: var(--text-color);
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 500;
        }

        .input-group {
            display: grid;
            gap: 1rem;
            margin-bottom: 2rem;
        }

        input {
            padding: 1rem;
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s ease;
        }

        input:focus {
            outline: none;
            border-color: #4F46E5;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }

        button {
            background: #4F46E5;
            color: white;
            padding: 1rem;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        button:hover {
            background: #4338CA;
        }

        .result-card {
            margin-top: 2rem;
            padding: 1.5rem;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        .hexagram-item {
            padding: 1rem 0;
            border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        }

        .hexagram-item:last-child {
            border-bottom: none;
        }

        .hexagram-name {
            color: #4F46E5;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }

        /* 新增信息样式 */
        .hexagram-props {
            color: #666;
            font-size: 0.9em;
            margin: 0.3rem 0;
        }
        .hexagram-props span {
            display: inline-block;
            margin-right: 1rem;
        }
        .hexagram-dynamic {
            color: #e53e3e;
            font-weight: 500;
            margin: 0.3rem 0;
        }
        .hexagram-desc {
            color: #666;
            line-height: 1.6;
        }

        .disclaimer {
            margin-top: 3rem;
            text-align: center;
            color: rgba(0, 0, 0, 0.6);
            font-size: 14px;
            line-height: 1.8;
            padding: 1rem;
            border-top: 1px solid rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>赛博算命</h1>

        <div class="input-group">
            <input type="number" id="num1" placeholder="输入第一个数字">
            <input type="number" id="num2" placeholder="输入第二个数字">
            <input type="number" id="num3" placeholder="输入第三个数字">
        </div>
        <button onclick="calculate()">开始解读</button>

        <div id="result" class="result-card"></div>

        <div class="disclaimer">
            <p>作者：钱一一</p>
            <p>上述工具是基于传统周易文化的数字娱乐，解读结果仅供娱乐参考</p>
            <p>拒绝封建迷信，倡导科学理性</p>
        </div>
    </div>

    <script>
        const HEXAGRAM_DEF = {
            "大安": {
        "卦属": "震", "五行": "木", "方位": "正东",
        "特性": ["长期", "缓慢", "稳定"],
        "动态吉凶": {"求安稳": "吉", "求变化": "凶"},
        "克拜": "三清",
        "解读": "根基稳固之事可成，变革创新之事不利"
    },
    "留连": {
        "卦属": "巽", "五行": "木", "方位": "东南",
        "特性": ["停止", "反复", "复杂"],
        "动态吉凶": {"想挽留": "吉", "其他": "凶"},
        "克拜": "文昌",
        "解读": "维持现状需主动争取，消极应对则生变"
    },
    "速喜": {
        "卦属": "离", "五行": "火", "方位": "正南",
        "特性": ["惊喜", "快速", "突然"],
        "动态吉凶": {"突发事件": "吉"},
        "克拜": "雷祖",
        "解读": "意外之喜降临，但需防乐极生悲"
    },
    "赤口": {
        "卦属": "兑", "五行": "金", "方位": "正西",
        "特性": ["争斗", "凶恶", "伤害"],
        "动态吉凶": {"诉讼/冲突": "凶"},
        "克拜": "将帅",
        "解读": "口舌是非易起，谨防血光之灾"
    },
    "小吉": {
        "卦属": "坎", "五行": "水", "方位": "正北",
        "特性": ["起步", "不多", "尚可"],
        "动态吉凶": {"初始阶段": "吉"},
        "克拜": "真武",
        "解读": "小成可期，大谋需慎"
    },
    "空亡": {
        "卦属": "中", "五行": "土", "方位": "内",
        "特性": ["失去", "虚伪", "空想"],
        "动态吉凶": {"金钱事务": "大凶"},
        "克拜": "玉皇",
        "解读": "虚实难辨，宜修心性"
    },
    "病符": {
        "卦属": "坤", "五行": "土", "方位": "西南",
        "特性": ["病态", "异常", "治疗"],
        "动态吉凶": {"已患病": "吉（宜治）", "未病": "凶"},
        "克拜": "后土",
        "解读": "旧疾复发之兆，预防胜于治疗"
    },
    "桃花": {
        "卦属": "艮", "五行": "土", "方位": "东北",
        "特性": ["欲望", "牵绊", "异性"],
        "动态吉凶": {"人际关系": "平"},
        "克拜": "城隍",
        "解读": "情缘纠葛缠身，慎防色欲伤身"
    },
    "天德": {
        "卦属": "乾", "五行": "金", "方位": "西北",
        "特性": ["贵人", "上司", "高远"],
        "动态吉凶": {"求人办事": "吉"},
        "克拜": "紫薇",
        "解读": "贵人暗中相助，把握机缘可成"
    }
        };

        function calculateHexagrams(n1, n2, n3) {
            const elements = Object.keys(HEXAGRAM_DEF);
            const p1 = (n1 - 1 + 9) % 9;
            const p2 = (p1 + n2 + 9) % 9;
            const p3 = (p2 + n3 + 9) % 9;
            return [elements[p1], elements[p2], elements[p3]];
        }

        function calculate() {
            const n1 = parseInt(document.getElementById('num1').value) || 0;
            const n2 = parseInt(document.getElementById('num2').value) || 0;
            const n3 = parseInt(document.getElementById('num3').value) || 0;

            const hexagrams = calculateHexagrams(n1, n2, n3);

            const resultHTML = hexagrams.map((h, i) => {
                const data = HEXAGRAM_DEF[h];
                return `
                <div class="hexagram-item">
                    <div class="hexagram-name">第${i+1}卦「${h}」</div>
                    <div class="hexagram-props">
                        <span>卦属：${data.卦属}</span>
                        <span>特性：${data.特性.join('、')}</span>
                    </div>
                    <div class="hexagram-dynamic">
                        ${Object.entries(data.动态吉凶).map(([k,v]) => `${k}：${v}`).join('，')}
                    </div>
                    <div class="hexagram-desc">${data.解读}</div>
                </div>`;
            }).join('');

            document.getElementById('result').innerHTML = resultHTML;
        }
    </script>
</body>
</html>
'''

# 计算器工具
CALCULATOR_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>赛博计算器</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --primary-color: rgba(255, 255, 255, 0.15);
            --text-color: #333;
        }

        body {
            min-height: 100vh;
            margin: 0;
            padding: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            background: linear-gradient(45deg, #f3f4f6, #f9fafb);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        .container {
            width: 100%;
            max-width: 400px;
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        h1 {
            color: var(--text-color);
            text-align: center;
            margin-bottom: 1.5rem;
            font-weight: 500;
        }

        .display {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            text-align: right;
            font-size: 2em;
            border: 1px solid rgba(0, 0, 0, 0.1);
            overflow-x: auto;
        }

        .grid-container {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 0.8rem;
        }

        button {
            background: #4F46E5;
            color: white;
            padding: 1rem;
            border: none;
            border-radius: 8px;
            font-size: 1.2em;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        button:hover {
            background: #4338CA;
        }

        .operator {
            background: #6366f1;
        }

        .clear {
            background: #ef4444;
        }

        .clear:hover {
            background: #dc2626;
        }

        .equals {
            background: #10b981;
        }

        .equals:hover {
            background: #059669;
        }

        .disclaimer {
            margin-top: 2rem;
            text-align: center;
            color: rgba(0, 0, 0, 0.6);
            font-size: 14px;
            line-height: 1.8;
            padding: 1rem;
            border-top: 1px solid rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>赛博计算器</h1>
        <div class="display" id="display">0</div>

        <div class="grid-container">
            <button class="clear" onclick="clearDisplay()">C</button>
            <button class="operator" onclick="appendOperator('/')">/</button>
            <button class="operator" onclick="appendOperator('*')">×</button>
            <button class="operator" onclick="appendOperator('-')">-</button>

            <button onclick="appendNumber(7)">7</button>
            <button onclick="appendNumber(8)">8</button>
            <button onclick="appendNumber(9)">9</button>
            <button class="operator" onclick="appendOperator('+')">+</button>

            <button onclick="appendNumber(4)">4</button>
            <button onclick="appendNumber(5)">5</button>
            <button onclick="appendNumber(6)">6</button>
            <button onclick="appendDecimal()">.</button>

            <button onclick="appendNumber(1)">1</button>
            <button onclick="appendNumber(2)">2</button>
            <button onclick="appendNumber(3)">3</button>
            <button class="equals" onclick="calculate()">=</button>

            <button onclick="appendNumber(0)" style="grid-column: span 2;">0</button>
            <button onclick="toggleSign()">±</button>
        </div>

        <div class="disclaimer">
            <p>基于现代数学原理的电子计算工具</p>
            <p>精确计算，理性决策</p>
        </div>
    </div>

    <script>
        let currentInput = '0';
        let previousInput = null;
        let operation = null;

        function updateDisplay() {
            const display = document.getElementById('display');
            display.textContent = currentInput;
        }

        function appendNumber(num) {
            if (currentInput === '0') {
                currentInput = num.toString();
            } else {
                currentInput += num.toString();
            }
            updateDisplay();
        }

        function appendDecimal() {
            if (!currentInput.includes('.')) {
                currentInput += '.';
                updateDisplay();
            }
        }

        function appendOperator(op) {
            previousInput = currentInput;
            currentInput = '0';
            operation = op;
        }

        function clearDisplay() {
            currentInput = '0';
            previousInput = null;
            operation = null;
            updateDisplay();
        }

        function toggleSign() {
            currentInput = (parseFloat(currentInput) * -1).toString();
            updateDisplay();
        }

        function calculate() {
            if (!previousInput || !operation) return;

            const prev = parseFloat(previousInput);
            const current = parseFloat(currentInput);
            let result;

            switch(operation) {
                case '+':
                    result = prev + current;
                    break;
                case '-':
                    result = prev - current;
                    break;
                case '*':
                    result = prev * current;
                    break;
                case '/':
                    result = current === 0 ? '错误' : prev / current;
                    break;
                default:
                    return;
            }

            currentInput = result.toString();
            previousInput = null;
            operation = null;
            updateDisplay();
        }
    </script>
</body>
</html>
'''

# 路由配置
@app.route('/')
def index():
    return render_template_string(NAV_HTML)

@app.route('/divination')
def divination():
    return render_template_string(DIVINATION_HTML)

@app.route('/calculator')
def calculator():
    return render_template_string(CALCULATOR_HTML)

if __name__ == '__main__':
    app.run(debug=True)