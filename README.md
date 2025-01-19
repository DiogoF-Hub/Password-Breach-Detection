# **Password Breach Detection**

A **Python-based tool** designed to help users determine if their passwords have been compromised in data breaches. It utilizes a local database of hashed passwords to ensure privacy and efficiency.

---

## **Project Context**

This project is part of my schoolwork for the **first semester** of the **first year** in the class **PYTWO1** as I pursue a **BTS in CyberSecurity** at **Lycée Guillaume Kroll (LGK)** in Luxembourg during the year **2024**.

The tool is developed to demonstrate practical programming skills, data handling, and secure password management techniques.

The password database used in this project was sourced from the public repository of [Have I Been Pwned](https://haveibeenpwned.com/) using the commands provided in their GitHub project ([PwnedPasswordsDownloader](https://github.com/HaveIBeenPwned/PwnedPasswordsDownloader)).

### **Available Databases:**
- **OneDrive Database**: A 9GB file containing approximately **200 million SHA-1 hashed passwords** and their breach counts. Hosted on **my personal OneDrive** for easy access (valid until **January 11 2026**).
- **PwnedPasswordsDownloader Database**: A ~40GB file containing around **900 million SHA-1 hashed passwords**. If downloaded, the file **must be named** `pwnedpasswords.txt` and placed in the **root** of the project folder.

> **Note**: In the future, I plan to move the hosting to a platform better suited for public data sharing.

---

## **Features**

- **Password Hashing**: Converts user passwords into SHA-1 hashes for secure comparison.
- **Breach Count Tracking**: Records the number of times a password has appeared in breaches.
- **Local Database**: Operates without the need for internet access, ensuring user privacy.
- **Extensible Design**: Integration with a Streamlit interface for enhanced user interaction.
- **Download Database from OneDrive**: Provides a streamlined option to download a 9GB database directly from OneDrive via the GUI.
- **Top Passwords Analysis**: Identifies the most frequently breached passwords from the database, giving users insights into commonly used weak passwords.
- **Add Passwords**: Allows users to add new password hashes to the database, either at the end or at a random position within the file.
- **Clear Cache**: Provides a feature to clear cached files, such as top passwords or previously searched hashes, to reset or refresh stored data.

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
Simply run the following command to launch the **Streamlit interface**, which manages all interactions:

```
streamlit run Home.py
```

- If the required password database is missing or incomplete, the interface will guide you to download it.
- Choose between the **9GB OneDrive database** or the **40GB PwnedPasswordsDownloader** database.
- Once the database is ready, use the interface to search for compromised passwords, analyze data, or add new entries.

> **Note:** If the database already exists or is incomplete and you wish to redownload it, just click the download button again. This will delete the existing file and download a fresh copy.

---

## **Future Features**

- **Random Line Insertion**: Functionality to insert entries at random positions within the database file for testing purposes. ✅
- **Top hashes**: Find the top hashes that have been seen the most in breaches from the txt file. ✅
- **Streamlit Interface**: A user-friendly web interface for easier interaction. ✅
- **Random Line Insertion but more efficient**: Make the process of adding a random line more efficient by not loading the whole file to the RAM. ✅
- **Decrypt Top Password Hashes**: Add functionality to decrypt top password hashes using the [Hashes.com API](https://hashes.com/en/docs) (paid). This will provide insights into the plaintext values of the most commonly breached hashes.
- **Database Selection in GUI**: Implement a feature where users can easily switch between multiple databases (e.g., the 9GB and 40GB options) directly in the interface, catering to performance needs and testing requirements.
- **Better Hosting Solutions**: Host both the 9GB (smaller) and 40GB (full) databases, allowing users to download and store both. Provide an option to select the preferred database from the GUI.
- **Advanced Hash Support**: Expand functionality to include additional hashing algorithms like MD5 and SHA-256 from other databases, making the tool more versatile.
