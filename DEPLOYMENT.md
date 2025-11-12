# Deployment Guide - FastAPI Expense Tracker

This guide will help you set up the FastAPI Expense Tracker to run automatically on your Windows computer and access it anytime.

## Prerequisites

- Python 3.13 installed
- Git installed
- This project cloned to your computer

## Quick Start

### Option 1: Manual Start (Easiest)

1. **Double-click** `start_server.bat` in the project folder
2. The server will start and show you the URLs:
   - Application: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`
3. Keep the window open while using the application
4. Press `Ctrl+C` to stop the server

### Option 2: Run in Background

Open PowerShell in the project directory and run:
```powershell
Start-Process python -ArgumentList "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" -WindowStyle Hidden
```

To stop it, find the process in Task Manager and end it.

## Automatic Startup on Windows Boot

### Method 1: Task Scheduler (Recommended)

1. **Create a startup script:**
   - The `start_server.bat` file is already created in your project

2. **Open Task Scheduler:**
   - Press `Win + R`
   - Type `taskschd.msc` and press Enter

3. **Create a new task:**
   - Click "Create Task" (not "Create Basic Task")
   - Name: `FastAPI Expense Tracker`
   - Description: `Auto-start FastAPI expense tracking application`
   - Check "Run with highest privileges"
   - Configure for: Windows 10/11

4. **Triggers tab:**
   - Click "New..."
   - Begin the task: "At startup"
   - Click OK

5. **Actions tab:**
   - Click "New..."
   - Action: "Start a program"
   - Program/script: `C:\Windows\System32\cmd.exe`
   - Add arguments: `/c "cd /d C:\Users\AprilJohnMaraat\source\repos\personal\python-basic && start_server.bat"`
   - (Replace the path with your actual project path)
   - Click OK

6. **Conditions tab:**
   - Uncheck "Start the task only if the computer is on AC power"

7. **Settings tab:**
   - Check "Allow task to be run on demand"
   - Check "If the task fails, restart every: 1 minute"
   - Attempt to restart up to: 3 times

8. **Click OK** to save the task

### Method 2: Startup Folder (Simpler but visible)

1. **Create a shortcut:**
   - Right-click on `start_server.bat`
   - Select "Create shortcut"

2. **Move to Startup folder:**
   - Press `Win + R`
   - Type `shell:startup` and press Enter
   - Move the shortcut to this folder

3. **Restart your computer** - the app will start automatically

### Method 3: Windows Service (Advanced)

For running as a true Windows service, you can use NSSM (Non-Sucking Service Manager):

1. **Download NSSM:**
   - Visit: https://nssm.cc/download
   - Extract to a folder (e.g., `C:\nssm`)

2. **Install as service:**
   ```powershell
   # Run PowerShell as Administrator
   cd C:\nssm\win64
   .\nssm.exe install FastAPIExpenseTracker "C:\Users\AprilJohnMaraat\AppData\Local\Programs\Python\Python313\python.exe" "-m uvicorn main:app --host 0.0.0.0 --port 8000"
   .\nssm.exe set FastAPIExpenseTracker AppDirectory "C:\Users\AprilJohnMaraat\source\repos\personal\python-basic"
   .\nssm.exe set FastAPIExpenseTracker DisplayName "FastAPI Expense Tracker"
   .\nssm.exe set FastAPIExpenseTracker Description "Expense tracking API service"
   .\nssm.exe set FastAPIExpenseTracker Start SERVICE_AUTO_START
   ```

3. **Start the service:**
   ```powershell
   .\nssm.exe start FastAPIExpenseTracker
   ```

4. **Manage the service:**
   ```powershell
   # Stop service
   .\nssm.exe stop FastAPIExpenseTracker
   
   # Restart service
   .\nssm.exe restart FastAPIExpenseTracker
   
   # Remove service
   .\nssm.exe remove FastAPIExpenseTracker confirm
   ```

## Accessing Your Application

### On Your Computer

- **API Endpoint:** `http://localhost:8000`
- **Interactive API Docs:** `http://localhost:8000/docs`
- **Alternative API Docs:** `http://localhost:8000/redoc`

### From Other Devices on Your Network

1. **Find your computer's IP address:**
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address" (usually starts with 192.168.x.x)

2. **Access from other devices:**
   - `http://YOUR_IP_ADDRESS:8000`
   - Example: `http://192.168.1.100:8000`

3. **Configure Windows Firewall:**
   ```powershell
   # Run as Administrator
   New-NetFirewallRule -DisplayName "FastAPI Expense Tracker" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
   ```

### Making It Accessible from the Internet (Optional)

⚠️ **Security Warning:** Only do this if you understand the security implications.

1. **Port Forwarding on Router:**
   - Access your router settings (usually `192.168.1.1` or `192.168.0.1`)
   - Set up port forwarding for port 8000 to your computer's local IP
   - Use your public IP address to access from outside

2. **Use Ngrok (Easier):**
   ```powershell
   # Download ngrok from https://ngrok.com
   ngrok http 8000
   ```
   This gives you a temporary public URL.

## Troubleshooting

### Server won't start
- Check if port 8000 is already in use:
  ```powershell
  netstat -ano | findstr :8000
  ```
- Kill the process if needed:
  ```powershell
  taskkill /PID <process_id> /F
  ```

### Can't access from other devices
- Make sure Windows Firewall allows the connection
- Check if both devices are on the same network
- Verify the server is listening on `0.0.0.0` not just `127.0.0.1`

### Database errors
- Make sure `fastapi.db` exists in the project folder
- Check file permissions
- Run database migrations if needed

### Service won't start on boot
- Check Task Scheduler logs: Event Viewer > Windows Logs > Application
- Verify the path in the scheduled task is correct
- Ensure Python is in the system PATH

## Maintenance

### Update the application
```powershell
cd C:\Users\AprilJohnMaraat\source\repos\personal\python-basic
git pull origin main
```

### Backup database
```powershell
python scripts/backup_database.py
```

### View logs
- Console window (if running manually)
- Task Scheduler History (if using Task Scheduler)
- Windows Event Viewer (if running as service)

## Performance Tips

1. **Disable reload in production:**
   - Edit `start_server.bat` and remove `--reload` flag

2. **Use production ASGI server:**
   - Install: `pip install gunicorn`
   - For Windows, use `waitress` instead:
     ```powershell
     pip install waitress
     waitress-serve --host=0.0.0.0 --port=8000 main:app
     ```

3. **Set environment to production:**
   ```powershell
   $env:ENVIRONMENT="production"
   ```

## Security Recommendations

1. **Change default credentials** if any
2. **Use HTTPS** for production (consider using Caddy or nginx as reverse proxy)
3. **Implement authentication** for API endpoints
4. **Regular backups** of the database
5. **Keep Python and dependencies updated**
6. **Don't expose to internet** without proper security measures

## Support

For issues or questions:
- Check the API documentation: `http://localhost:8000/docs`
- Review application logs
- Check GitHub repository: https://github.com/aprilmaraat/python-basic
