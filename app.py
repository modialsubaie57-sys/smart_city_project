from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "modi_secret_key"

# ✅ الأنشطة الذكية
activities = {
    "1": {
        "title": "🚕 الذهاب للعمل",
        "description": "سيارة ذاتية القيادة اختارت لك الطريق الأسرع،"
                       " وتجنبت الزحام باستخدام الذكاء الاصطناعي.",
        "points": 10,
        "image": "work.jpg"
    },

    "2": {
        "title": "🩺 زيارة المستشفى",
        "description": "حجزت موعدك عبر تطبيق صحي،"
                       " وتم تشخيصك باستخدام نظام ذكي يعتمد على بياناتك الحيوية،"
                       " سلامتك ماتشوفين شر ❤️.",
        "points": 8,
        "image": "hos.jpg"
    },
    "3": {
        "title": "🛒 التسوق الذكي",
        "description": "دخلت متجر بدون كاشير، والدفع تم تلقائيًا عبر التعرف على الوجه وتقنية NFC،"
                       " تسوق ممتع يا ملكة 🫶.",
        "points": 7,
        "image": "shop.jpg"
    },
    "4": {
        "title": "🎨 نشاط ترفيهي",
        "description": "حضرت فعالية فنية مقترحة حسب اهتماماتك،"
                       " وحجزت تذكرتك عبر تطبيق ترفيهي ذكي.",
        "points": 6,
        "image": "entr.jpg"
    },
    "5": {
        "title": "📚 التعليم الذكي",
        "description": "شاركت في دورة تدريبية عبر منصة تعليمية تعتمد على الذكاء الاصطناعي لتخصيص المحتوى، "
                       "بالتوفيق يا بطلة ✨.",
        "points": 9,
        "image": "edec.jpg"
    }
}

# ✅ دالة لتحديث النقاط في لوحة الشرف
def update_leaderboard(name, points):
    path = "leaderboard.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    # جمع النقاط وليس استبدالها
    data[name] = data.get(name, 0) + points

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ✅ صفحة الترحيب
@app.route("/", methods=["GET", "POST"])
def welcome():
    if request.method == "POST":
        name = request.form.get("username")
        session["username"] = name
        session["points"] = 0
        return redirect(url_for("home"))
    return render_template("welcome.html")

# ✅ الصفحة الرئيسية
@app.route("/home")
def home():
    username = session.get("username", "زائر")
    return render_template("index.html", username=username)

# ✅ صفحة النشاط
@app.route("/نشاط/<id>")
def activity(id):
    data = activities.get(id)
    if data:
        username = session.get("username", "زائر")
        session["points"] += data["points"]
        update_leaderboard(username, data["points"])
        return render_template("activity.html", activity=data)
    else:
        return "<h1>النشاط غير موجود</h1>"

# ✅ صفحة التقرير
@app.route("/تقرير")
def report():
    username = session.get("username", "ضيف")
    points = session.get("points", 0)

    if os.path.exists("leaderboard.json"):
        with open("leaderboard.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    sorted_users = sorted(data.items(), key=lambda x: x[1], reverse=True)
    rank = next((i+1 for i, (user, _) in enumerate(sorted_users) if user == username), "غير محدد")

    return render_template("report.html", username=username, points=points, users=sorted_users, rank=rank)

# ✅ صفحة إنهاء اليوم
@app.route("/نهاية")
def end_day():
    username = session.get("username", "زائر")
    points = session.get("points", 0)
    update_leaderboard(username, points)

    if os.path.exists("leaderboard.json"):
        with open("leaderboard.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        sorted_users = sorted(data.items(), key=lambda x: x[1], reverse=True)
        rank = next((i+1 for i, (user, _) in enumerate(sorted_users) if user == username), "غير محدد")
    else:
        rank = "غير محدد"

    return render_template("end.html", username=username, points=points, rank=rank)

# ✅ صفحة لوحة الشرف
@app.route("/لوحة_الشرف")
def leaderboard():
    if os.path.exists("leaderboard.json"):
        with open("leaderboard.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        sorted_users = sorted(data.items(), key=lambda x: x[1], reverse=True)
    else:
        sorted_users = []
    return render_template("leaderboard.html", users=sorted_users)
@app.route("/تصفير_لوحة_الشرف")
def reset_leaderboard():
    path = "leaderboard.json"
    if os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        return "<h2>✅ تم تصفير لوحة الشرف بنجاح</h2>"
    else:
        return "<h2>⚠️ ملف لوحة الشرف غير موجود</h2>"


# ✅ تشغيل التطبيق
if __name__ == "__main__":
    app.run(debug=True)
