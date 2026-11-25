# 🎓 Student Management Project (FastAPI + MySQL + HTML/JS)

একটা সহজ প্রজেক্ট, যেখানে **Frontend (HTML/CSS/JS) → Backend (FastAPI) → Database (MySQL)** একসাথে কাজ করে।

---

## 📁 ফোল্ডার গঠন

```
fast-api-project/
├── main.py                  ← প্রজেক্ট এখান থেকে চালু হয়
├── db.py                    ← MySQL এর সাথে connection
├── requirements.txt         ← যে library গুলো লাগবে
├── model/                   ← Database এর table
│   ├── student.py           (students table)
│   └── subjects.py          (subjects table - নম্বর)
├── utils/schema.py          ← API তে কী data আসবে/যাবে (Pydantic)
├── repository/              ← শুধু database query
├── service/                 ← হিসাব আর নিয়ম (average, comment, error)
├── routers/                 ← API এর URL গুলো
└── frontend/                ← ব্রাউজারে যা দেখা যায়
    ├── index.html
    ├── style.css
    └── script.js
```

### Data কীভাবে চলে?

```
Browser (script.js)
   │  fetch("/students")
   ▼
Router  (routers/student_controller.py)   → কোন URL এ request এলো
   ▼
Service (service/student_service.py)      → হিসাব, check, error
   ▼
Repository (repository/*.py)              → database query
   ▼
MySQL Database (students, subjects table)
```

---

## ▶️ চালানোর ধাপ

### ১. XAMPP এ MySQL চালু করো
XAMPP Control Panel খুলে **MySQL** এর পাশে **Start** চাপো (Apache লাগবে না)।
> Database (`alchemyBD`) আর table গুলো প্রজেক্ট চালু হলে নিজেই বানাবে।

### ২. (দরকার হলে) `db.py` তে username/password ঠিক করো
```python
SERVER_URL = "mysql+pymysql://root:@localhost:3306"   # XAMPP: password খালি
DB_NAME = "alchemyBD"
```

### ৩. প্রজেক্ট চালাও
প্রজেক্ট ফোল্ডারে **`run.bat`** এ double-click করো। এটা নিজেই:
- কম্পিউটারের Python খুঁজে নেয়
- প্রথমবার `venv` ফোল্ডার বানায় আর library install করে (ইন্টারনেট লাগবে)
- server চালু করে

> কালো window বন্ধ করবে না, ওটাই server।

### ৪. ব্রাউজারে খোলো
| কী দেখবে | লিংক |
|---|---|
| 🖥️ Frontend (website) | http://127.0.0.1:8000 |
| 📘 API Docs (Swagger) | http://127.0.0.1:8000/docs |

---

## 🔗 API গুলো

| কাজ | Method | URL |
|---|---|---|
| সব student দেখা | GET | `/students` |
| একজন student দেখা | GET | `/students/{roll}` |
| নতুন student যোগ | POST | `/students` |
| student update | PATCH | `/students/{roll}` |
| student delete | DELETE | `/students/{roll}` |

### POST এর জন্য JSON উদাহরণ
```json
{
  "name": "Rahim",
  "age": 20,
  "email": "rahim@gmail.com",
  "roll": 1,
  "session": "2024-25",
  "english_score": 85,
  "math_score": 90,
  "history_score": 78
}
```

### নিয়ম
- বয়স ১৮ থেকে ৩০
- নম্বর ০ থেকে ১০০
- একই roll দুইবার দেওয়া যাবে না
- গড় নম্বর দেখে comment: ৯০+ Excellent, ৮০+ Very Good, ৭০+ Good, বাকি Need Improvement

---

## ❗ সাধারণ সমস্যা ও সমাধান

| Error | কারণ | সমাধান |
|---|---|---|
| `Can't connect to MySQL server` | MySQL চালু নেই | XAMPP / MySQL service চালু করো |
| `Access denied for user 'root'` | পাসওয়ার্ড ভুল | `db.py` তে ঠিক পাসওয়ার্ড দাও |
| `cryptography package is required` | library নেই | `pip install cryptography` |
| `No module named 'fastapi'` | install হয়নি | `pip install -r requirements.txt` |
| পেজ খোলে কিন্তু টেবিল খালি / error | server বন্ধ | terminal এ `uvicorn main:app --reload` চালু আছে কিনা দেখো |

---

## 🧑‍🏫 ক্লাসে পড়ানোর ক্রম (পরামর্শ)

1. **db.py** — database connection আর `get_db()` কী করে
2. **model/** — Python class কীভাবে MySQL table হয়
3. **utils/schema.py** — Pydantic দিয়ে input check (age 40 দিয়ে error দেখাও)
4. **repository → service → router** — একটা request কীভাবে ভেতরে যায়
5. **/docs** এ গিয়ে API test করো
6. **frontend/script.js** — `fetch()` দিয়ে কীভাবে API call হয়
7. ব্রাউজারে add/edit/delete করে MySQL table এ পরিবর্তন দেখাও

## 🏋️ ছাত্রদের জন্য অনুশীলন
- নতুন একটা subject যোগ করো (যেমন `science_score`)
- নাম দিয়ে search এর একটা API বানাও
- Frontend এ "Excellent" student দের সবুজ রঙে দেখাও
