from flask import Flask, request, render_template_string

app = Flask(__name__)


HEXAGRAM_DEF = {
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
}


def calculate_hexagrams(n1, n2, n3):
    elements = list(HEXAGRAM_DEF.keys())
    p1 = (n1 - 1) % 9
    p2 = (p1 + n2) % 9
    p3 = (p2 + n3) % 9
    return [elements[p1], elements[p2], elements[p3]]

# 网页模板
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>六壬占卜</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
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
        }
        
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

        <form method="POST">
            <div class="input-group">
                <input type="number" name="num1" placeholder="输入第一个数字" required>
                <input type="number" name="num2" placeholder="输入第二个数字" required>
                <input type="number" name="num3" placeholder="输入第三个数字" required>
            </div>
            <button type="submit">开始解读</button>
        </form>

        {% if result %}
        <div class="result-card">
            {% for item in result %}
            <div class="hexagram-item">
                <div class="hexagram-name">{{ item.name }}</div>
                <div class="hexagram-props">
                    <span>卦属：{{ item.attribute }}</span>
                    <span>特性：{{ item.features }}</span>
                </div>
                <div class="hexagram-dynamic">动态：{{ item.dynamic }}</div>
                <div class="hexagram-desc">{{ item.desc }}</div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
         <div class="disclaimer">
            <p>作者：钱一一</p>
            <p>上述工具是基于传统周易文化的数字娱乐，解读结果仅供娱乐参考</p>
            <p>拒绝封建迷信，倡导科学理性</p>
        </div>
    </div>
</body>
</html>
'''


# 修改返回结果的处理逻辑
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            n1 = int(request.form['num1'])
            n2 = int(request.form['num2'])
            n3 = int(request.form['num3'])
            hexagrams = calculate_hexagrams(n1, n2, n3)

            # 新增数据处理逻辑
            result = []
            for i, h in enumerate(hexagrams):
                data = HEXAGRAM_DEF[h]
                result.append({
                    "name": f"第{i + 1}卦「{h}」",
                    "attribute": data["卦属"],
                    "features": "、".join(data["特性"]),
                    "dynamic": "，".join([f"{k}：{v}" for k, v in data["动态吉凶"].items()]),
                    "desc": data["解读"]
                })

        except Exception as e:
            print(f"Error: {e}")
            result = None

        return render_template_string(HTML_TEMPLATE, result=result)
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)