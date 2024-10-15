# Bike Sharing Data Analysis

## Setup Guide

### Prerequisites
- **Python 3.7+** must be installed.

### Steps to Run the Project

1. **Create a Virtual Environment**:
   Start by creating the virtual environment:
   ```bash
   python -m venv venv
   ```

2. **Move Project Files into the Virtual Environment Directory**:
   Place all project files, including `requirements.txt` and `dashboard.py`, inside the virtual environment folder (`venv`).

3. **Navigate to the Virtual Environment Directory**:
   Ensure you're inside the virtual environment's directory:
   ```bash
   cd venv
   ```

4. **Activate the Virtual Environment**:
   Once inside the virtual environment directory, activate it.

   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```

   - **macOS/Linux**:
     ```bash
     source ./venv/Scripts/activate
     ```

5. **Install Dependencies**:
   With the virtual environment activated, install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. **Navigate to the "Dashboard" Directory**:
   Change into the "Dashboard" directory within the virtual environment:
   ```bash
   cd Dashboard
   ```

7. **Run the Streamlit App**:
   Now, run the Streamlit app using the following command:
   ```bash
   streamlit run dashboard.py
   ```

8. **Deactivate the Virtual Environment**:
   After you’re done, you can deactivate the virtual environment by running:
   ```bash
   deactivate
   ```
