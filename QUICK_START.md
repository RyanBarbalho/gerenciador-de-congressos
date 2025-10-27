# 🚀 Quick Start Guide

## ▶️ Run the App

### Option 1: Double-click the batch file
```
run_streamlit.bat
```

### Option 2: Command line
```bash
python -m streamlit run streamlit_app.py
```

### Option 3: Alternative
```bash
py -m streamlit run streamlit_app.py
```

---

## 🌐 Access the App

The app will automatically open in your browser at:
```
http://localhost:8501
```

If it doesn't open automatically, copy the URL from the terminal.

---

## 📖 First Time Usage

### Step 1: Load Data
1. Go to the **Home** page
2. Click **"📁 Carregar Dados Padrão"**
3. Wait for confirmation (✅ messages)

### Step 2: Execute Allocation
1. Navigate to **"⚙️ Alocação"** page
2. Select strategy: **"Programação Linear (Ótimo)"**
3. Check both: ☑ CC and ☑ EC
4. Click **"🚀 Executar Alocação"**
5. Wait for results (with 🎈 animation)

### Step 3: View Results
1. Go to **"📈 Resultados"** page
2. Explore different tabs:
   - **Por Sala**: See allocations by room
   - **Por Horário**: See allocations by schedule
   - **Por Matéria**: See all courses (with download button)
   - **Por Local**: See geographic distribution

### Step 4: Analyze
1. Go to **"📉 Análises"** page
2. Explore tabs:
   - **Gráficos**: Visual charts
   - **Otimização**: Efficiency metrics
   - **Comparações**: Comparative analysis

---

## 🎯 Key Features

### 🏠 Home
- Overview and quick actions
- Usage guide

### 📊 Dashboard
- Statistics and charts
- Data distribution

### 📁 Dados
- Upload CSV files
- View tables
- Export data

### ⚙️ Alocação
- Choose strategy
- Configure options
- Execute optimization

### 📈 Resultados
- View by room
- View by time
- View by course
- **Download CSV**

### 📉 Análises
- Interactive charts
- Optimization metrics
- Comparisons

---

## 💡 Tips

### Search
- Use the 🔍 search boxes to find specific courses
- Searches are instant (no need to press Enter)

### Download
- Go to **Resultados** → **Por Matéria** tab
- Click **"📥 Download Resultados (CSV)"**

### Compare Strategies
1. Run with "Linear" strategy
2. Note the results
3. Run again with "Guloso" strategy
4. Compare metrics

### Best Practices
- Load data before executing allocation
- Check Dashboard before allocation to see if data is correct
- Review Análises → Otimização for efficiency insights
- Export results for reporting

---

## ❓ Troubleshooting

### App won't start
```bash
pip install -r requirements_streamlit.txt
python -m streamlit run streamlit_app.py
```

### Data not loading
- Make sure `oferta_cc_2025_1.csv` and `oferta_ec_2025_1.csv` exist
- Check file format (columns: codigo, nome, matriculados, horario, capacidade, material)

### Error during allocation
- Check if total inscritos < total capacity
- Make sure both data and rooms are loaded

### Blank page
- Refresh browser (F5 or Ctrl+R)
- Check terminal for error messages

---

## 🔄 Stop the App

Press `Ctrl + C` in the terminal where the app is running.

---

## 📁 Files Created

```
streamlit_app.py              # Main app (~1,200 lines)
requirements_streamlit.txt    # Dependencies
README_STREAMLIT.md          # Full documentation
STREAMLIT_FEATURES.md        # Features guide
FRONTEND_SUMMARY.md          # Executive summary
VISUAL_GUIDE.md              # Visual mockups
QUICK_START.md               # This file
run_streamlit.bat            # Windows launcher
run_streamlit.sh             # Linux/Mac launcher
```

---

## 📚 Full Documentation

- **`README_STREAMLIT.md`**: Installation and detailed usage
- **`STREAMLIT_FEATURES.md`**: Complete features list
- **`FRONTEND_SUMMARY.md`**: Technical summary
- **`VISUAL_GUIDE.md`**: UI mockups and design

---

## 🎉 Enjoy!

Your classroom allocation system now has a beautiful, modern web interface! 

**Happy allocating! 🏫**

