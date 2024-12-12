# **Password Breach Detection**

A **Python-based tool** designed to help users determine if their passwords have been compromised in data breaches. It utilizes a local database of hashed passwords to ensure privacy and efficiency.

---

## **Project Context**

This project is part of my schoolwork for the **first semester** of the **first year** in the class **PYTWO1** as I pursue a **BTS in CyberSecurity** at **Lycée Guillaume Kroll (LGK)** in Luxembourg during the year **2024**. 

The tool is developed to demonstrate practical programming skills, data handling, and secure password management techniques.

The password database used in this project was sourced from the public repository of [Have I Been Pwned](https://haveibeenpwned.com/) using the commands provided in their GitHub project ([PwnedPasswordsDownloader](https://github.com/HaveIBeenPwned/PwnedPasswordsDownloader)). The database, a 9GB file containing approximately 200 million SHA-1 hashed passwords and their breach counts, is currently hosted on **my personal OneDrive** for ease of access.

> **Note**: In the future, I plan to move the hosting to a platform better suited for public data sharing.

---

## **Features**

- **Password Hashing**: Converts user passwords into SHA-1 hashes for secure comparison.
- **Breach Count Tracking**: Records the number of times a password has appeared in breaches.
- **Local Database**: Operates without the need for internet access, ensuring user privacy.
- **Extensible Design**: Planned integration with a Streamlit interface for enhanced user interaction.

---

## **Installation**

### **1. Clone the Repository**
```
git clone https://github.com/DiogoF-Hub/Password-Breach-Detection.git
```

### **2. Navigate to the Project Directory**
```
cd Password-Breach-Detection
```

### **3. Install Dependencies**
```
pip install -r requirements.txt
```
> **Note**: Ensure you have Python installed on your system.

---

## **Usage**

### **Run the Tool**
Simply run the `main.py` file, and it will handle everything automatically:
- If the required password database is missing, it will download it automatically.
- The tool will fetch the 9GB database file hosted on my personal OneDrive.
- Once the database is downloaded, the tool will prompt you to input a password to check if it has been compromised.

Run the following command:
```
python main.py
```

---

## **Planned Features**

- **Streamlit Interface**: A user-friendly web interface for easier interaction.
- **Random Line Insertion**: Functionality to insert entries at random positions within the database file for testing purposes.
