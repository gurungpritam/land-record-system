# Land Record Search System (भू-उपयोग क्षेत्र वर्गीकरण खोज प्रणाली)

A simple tool to search land records in Nepal. It connects to a Google Sheet and lets you filter data by VDC, Ward, Plot, and Land Use type.

## 📂 Project Files Explained
- **`app.py`**: The "Brain" of the project. It contains all the Python code that fetches data and creates the website.
- **`requirements.txt`**: The "Shopping List". It tells your computer which Python tools (libraries) are needed to run the app.
- **`index.html`**: The "Magic Ticket" for GitHub Pages. It lets this Python app run directly in a web browser without a server.

---

## 🚀 How to Run Locally (On Your Computer)

Use this method to test changes before sharing them.

### Step 1: Install Python
Make sure you have Python installed. You can check by typing `python --version` in your terminal.

### Step 2: Setup Virtual Environment
Linux systems usually prevent installing packages globally. Use a virtual environment:

1. **Activate the environment**:
   ```bash
   source venv/bin/activate
   ```
   *(You should see `(venv)` at the start of your command line)*

2. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```
   *What this does:* It downloads `streamlit` and `pandas` into your isolated `venv` folder.

### Step 3: Run the App
With the environment activated:
```bash
streamlit run app.py
```
*What this does:* It starts a local web server on your machine. A tab should automatically open in your browser at `http://localhost:8501`.

---

## 🌐 How to Deploy to the Web (Free)

You can put this on the internet for free using **GitHub Pages**.

### Step 1: Create a GitHub Repository
1. Go to [github.com](https://github.com) and create a new repository.
2. Name it something like `land-record-system`.

### Step 2: Upload Files
Upload these 3 files to your new repository:
- `app.py`
- `requirements.txt`
- `index.html`

### Step 3: Enable GitHub Pages
1. Go to your repository's **Settings**.
2. Click **Pages** on the left sidebar.
3. Under **Branch**, select `main` (or `master`) and click **Save**.

**That's it!** Wait about 1-2 minutes. GitHub will verify `index.html` and give you a website link (e.g., `https://yourname.github.io/land-record-system/`).

---

## 📊 Data Source
This app pulls live data from this Google Sheet:
[View Data Source](https://docs.google.com/spreadsheets/d/1YQmkQzvpoFUBxXLuc9QWsgRqmRn3YZOBED6UmCuqsXk/export?format=csv)
