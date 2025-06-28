# 🚀 VS Code Setup Guide for Sign Language Learning Platform

## Prerequisites

Before running the project, ensure you have:

- ✅ **Python 3.8+** installed
- ✅ **VS Code** installed
- ✅ **Git** installed (optional but recommended)
- ✅ **Webcam** connected (for real-time features)
- ✅ **4GB+ RAM** for optimal performance

## 📁 Project Setup in VS Code

### Step 1: Open Project in VS Code

1. **Open VS Code**
2. **File → Open Folder**
3. Navigate to: `E:\SL Learning Platform`
4. Click **Select Folder**

### Step 2: Install Required VS Code Extensions

Install these recommended extensions for the best development experience:

1. **Python** (by Microsoft) - Essential for Python development
2. **Python Debugger** (by Microsoft) - For debugging support
3. **Pylance** (by Microsoft) - Enhanced Python language support
4. **autoDocstring** (by Nils Werner) - For generating docstrings
5. **Better Comments** (by Aaron Bond) - Enhanced comment styling
6. **GitLens** (by GitKraken) - Enhanced Git capabilities

To install extensions:
- Press `Ctrl+Shift+X` to open Extensions
- Search for each extension and click **Install**

## 🐍 Python Environment Setup

### Step 3: Verify Python Installation

Open VS Code terminal (`Ctrl+`` ` or **Terminal → New Terminal**):

```powershell
python --version
```

Should show Python 3.8+ (e.g., `Python 3.11.5`)

### Step 4: Activate Virtual Environment

The project already has a virtual environment. Activate it:

```powershell
# Navigate to project directory (if not already there)
cd "E:\SL Learning Platform"

# Activate virtual environment
.\venv\Scripts\activate
```

You should see `(venv)` appear in your terminal prompt.

### Step 5: Select Python Interpreter in VS Code

1. Press `Ctrl+Shift+P` to open Command Palette
2. Type: `Python: Select Interpreter`
3. Choose the interpreter from the virtual environment:
   ```
   .\venv\Scripts\python.exe
   ```

## 📦 Install Dependencies

### Step 6: Install Required Packages

With the virtual environment activated:

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# If you encounter compatibility issues, try the compatible requirements
pip install -r requirements-compatible.txt
```

### Step 7: Verify Installation

Check if key packages are installed:

```powershell
pip list | findstr -i "streamlit opencv mediapipe tensorflow"
```

## 🚀 Running the Application

### Method 1: Using VS Code Terminal (Recommended)

1. **Open VS Code Terminal** (`Ctrl+`` `)
2. **Ensure virtual environment is activated** (you should see `(venv)`)
3. **Run the application**:

```powershell
streamlit run app.py
```

### Method 2: Using VS Code Debug Configuration

1. **Create `.vscode/launch.json`** (if not exists):

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run Streamlit App",
            "type": "python",
            "request": "launch",
            "module": "streamlit",
            "args": ["run", "app.py"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

2. **Press `F5`** or go to **Run → Start Debugging**

### Method 3: Using Run Script

```powershell
python run.py
```

## 🌐 Accessing the Application

After running, you'll see output like:

```
Local URL: http://localhost:8501
Network URL: http://192.168.1.xxx:8501
```

1. **Open your browser**
2. **Navigate to**: `http://localhost:8501`
3. **The Sign Language Learning Platform should load**

## 🛠️ VS Code Configuration Tips

### Terminal Configuration

Add this to VS Code settings (`Ctrl+,` → search "terminal"):

```json
{
    "terminal.integrated.defaultProfile.windows": "PowerShell",
    "terminal.integrated.profiles.windows": {
        "PowerShell": {
            "source": "PowerShell",
            "icon": "terminal-powershell",
            "args": ["-ExecutionPolicy", "Bypass"]
        }
    }
}
```

### Python Linting and Formatting

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "88"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

## 📊 Running API Server (Optional)

If you want to run the API server alongside the Streamlit app:

### Terminal 1 (Streamlit Frontend):
```powershell
streamlit run app.py
```

### Terminal 2 (FastAPI Backend):
```powershell
uvicorn api_server:app --reload --port 8000
```

Access API at: `http://localhost:8000/docs`

## 🧪 Running Tests

To run the test suite:

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_hand_tracker.py -v
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. **Virtual Environment Not Activating**
```powershell
# If activation fails, recreate the environment
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. **Camera Permission Issues**
- Grant camera access to your browser
- Check Windows camera privacy settings
- Restart VS Code and browser

#### 3. **Module Import Errors**
```powershell
# Add project root to Python path
$env:PYTHONPATH = "E:\SL Learning Platform"
```

#### 4. **Streamlit Not Found**
```powershell
# Reinstall streamlit
pip uninstall streamlit
pip install streamlit==1.29.0
```

#### 5. **TensorFlow Issues**
```powershell
# For Windows, install specific version
pip install tensorflow==2.15.0
```

#### 6. **OpenCV Camera Issues**
```powershell
# Reinstall opencv
pip uninstall opencv-python
pip install opencv-python==4.8.1.78
```

## 📝 Development Workflow

### Recommended VS Code Workflow:

1. **Open integrated terminal** (`Ctrl+`` `)
2. **Activate virtual environment**
3. **Make code changes** in the editor
4. **Run application** to test changes
5. **Use debugger** (`F5`) for troubleshooting
6. **Run tests** before committing

### Hot Reload

Streamlit automatically reloads when you save files. You'll see:
```
File modified: src/core/hand_tracker.py
Please rerun the script for changes to take effect.
```

Click **"Rerun"** in the browser to see changes.

## ⚡ Performance Tips

1. **Close unnecessary browser tabs**
2. **Use Chrome** for best performance
3. **Ensure good lighting** for camera features
4. **Close other applications** using camera
5. **Use USB 3.0** camera for better performance

## 🎯 Quick Commands Reference

```powershell
# Activate environment
.\venv\Scripts\activate

# Run main app
streamlit run app.py

# Run API server
uvicorn api_server:app --reload

# Run tests
pytest

# Check Python packages
pip list

# Update requirements
pip freeze > requirements.txt
```

## 🆘 Getting Help

If you encounter issues:

1. **Check the VS Code terminal** for error messages
2. **Review the browser console** (F12) for frontend errors
3. **Check camera permissions** in browser settings
4. **Verify all dependencies** are installed correctly
5. **Restart VS Code** and try again

## 🎉 Success!

Once everything is set up correctly, you should see:

- ✅ VS Code with project loaded
- ✅ Virtual environment activated
- ✅ All dependencies installed
- ✅ Streamlit app running at `localhost:8501`
- ✅ Camera working for real-time features
- ✅ All 20+ sign languages available

You're now ready to develop and use the Sign Language Learning Platform! 🤟

---

**Happy Learning and Coding!** 🚀
