# 🛡️ Network Sniffer

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![PySide6](https://img.shields.io/badge/PySide6-Qt-green?style=for-the-badge&logo=qt)
![Scapy](https://img.shields.io/badge/Scapy-Network%20Analysis-orange?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

A desktop application for **network traffic monitoring and security analysis** built using **Python** and **PySide6**.

The application captures live packets, analyzes network traffic, scans ports, performs malware reputation checks using the VirusTotal API, and provides an intuitive graphical interface for monitoring network activity.

---

## 📖 Overview

Network Sniffer is an academic project designed to demonstrate fundamental concepts of computer networking and cybersecurity. It combines packet capture, traffic analysis, network scanning, and security monitoring into a single desktop application.

---

## ✨ Features

- 📡 Live Packet Capture
- 🔍 Packet Inspection & Protocol Analysis
- 🌐 Port Scanner
- 🛡️ Vulnerability Scanner
- 🦠 VirusTotal Malware Reputation Lookup
- 💻 Running Process Monitor
- 📊 Live Traffic Visualization
- 📁 Export Captured Data
- ⚙️ Configurable Settings
- 🌙 Modern Dark Theme Interface

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core Programming Language |
| PySide6 (Qt) | Desktop GUI |
| Scapy | Packet Capture & Analysis |
| Nmap | Port Scanning |
| VirusTotal API | Malware Reputation Checks |
| Requests | API Communication |
| PyYAML | Configuration Management |

---

## 📂 Project Structure

```text
network-sniffer/
│
├── config/
├── core/
├── gui/
├── resources/
├── services/
├── utils/
├── main.py
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/axwin-raj/network-sniffer.git
```

Go to the project directory

```bash
cd network-sniffer
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python main.py
```

---

## ⚙️ Configuration

Create a `.env` file in the project directory.

```env
VT_API_KEY=YOUR_VIRUSTOTAL_API_KEY
```

---

## 📸 Screenshots

> Screenshots will be added in a future update.

---

## 🎯 Learning Objectives

This project demonstrates concepts including:

- Network Packet Capture
- TCP/IP Protocol Analysis
- Port Scanning
- Malware Reputation Analysis
- Desktop GUI Development
- API Integration
- Network Security Fundamentals

---

## 📌 Project Status

✅ Academic Project

🛠️ Maintained for learning and portfolio purposes.

---

## 👤 Maintainer

**Aswin Raj**

GitHub: https://github.com/axwin-raj

---

## 🤝 Acknowledgements

This repository contains an academic project developed collaboratively as part of a BSc Computer Science course. It is maintained here for learning and portfolio purposes.

---

## 🔮 Future Improvements

- Intrusion Detection System (IDS)
- Machine Learning Based Threat Detection
- PDF Report Generation
- Geo-IP Visualization
- Cross Platform Support
- Improved Performance

---

## 📄 License

This project is licensed under the MIT License.
