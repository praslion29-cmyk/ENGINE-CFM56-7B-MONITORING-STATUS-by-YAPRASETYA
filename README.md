# ENGINE-CFM56-7B-MONITORING-STATUS-by-YAPRASETYA
# ✈️ CFM56-7B Engine Health Monitoring Dashboard

**CFM56-7B Engine Health Monitoring** adalah dashboard berbasis Python yang dibuat untuk memonitor kondisi mesin pesawat Boeing 737 menggunakan konsep **Engine Health Monitoring (EHM)** seperti pada sistem **Airbus Skywise atau Boeing AHM**.

Dashboard ini dibuat menggunakan **Streamlit** sehingga dapat dijalankan sebagai aplikasi web interaktif untuk memantau parameter performa engine.

Created by  
**Y.A. Prasetya**

---

# 🚀 Features

### 1. Aircraft Information Input
User dapat memasukkan informasi dasar penerbangan:

- Date
- Aircraft Registration
- Engine Number
- Route

---

### 2. Engine Start Monitoring
Sistem memonitor **EGT saat engine start**.

Limit:

EGT Start Limit = **725°C**

Jika nilai melebihi limit maka sistem akan memberikan peringatan:

HOT START – Maintenance Required

---

### 3. Takeoff Engine Parameter Monitoring

Parameter yang dimonitor:

| Parameter | Maximum Limit |
|-----------|---------------|
| N1 | 102 % |
| N2 | 105 % |
| EGT | 950 °C |
| Fuel Flow | 5200 pph |
| Oil Pressure | 60 psi |
| Oil Temperature | 150 °C |
| Vibration | 4 ips |

Status parameter:

| Status | Condition |
|------|------|
| 🟢 NORMAL | < 95% dari limit |
| 🟡 CAUTION | ≥ 95% dari limit |
| 🔴 WARNING | > limit |

---

### 4. Engine Health Score

Dashboard menghitung **Health Score Engine (0–100)** berdasarkan kondisi parameter.

Contoh interpretasi:

| Score | Condition |
|------|------|
| 85 – 100 | Excellent |
| 70 – 84 | Monitor |
| < 70 | Maintenance Required |

---

### 5. EGT Margin Monitoring

EGT Margin dihitung dengan rumus:

EGT Margin = EGT Limit − Actual EGT

EGT Margin penting untuk memonitor **degradasi performa engine**.

---

### 6. Fleet Monitoring

Dashboard dapat menyimpan data beberapa pesawat untuk monitoring fleet.

Data yang disimpan:

- Aircraft
- Engine
- Route
- EGT
- Fuel Flow
- Vibration
- EGT Margin
- Health Score

---

### 7. Engine Trend Monitoring

Dashboard menampilkan grafik tren parameter:

- EGT Trend
- Fuel Flow Trend
- Vibration Trend

Grafik digunakan untuk memonitor perubahan performa engine dari waktu ke waktu.

---

### 8. Maintenance Recommendation

Jika parameter melewati batas limit, sistem akan memberikan:

- Possible Cause
- Maintenance Recommendation

Contoh:

High EGT  
Possible Cause: Turbine deterioration  
Recommendation: Inspect hot section

---

### 9. Data Export

Data monitoring dapat disimpan sebagai file:

CSV

Dashboard juga menyediakan fitur:

Print Report (CTRL + P)

---

# 🛠️ Installation

Install Python terlebih dahulu.

Clone atau download repository ini.

Install dependencies:

```bash
pip install -r requirements.txt
