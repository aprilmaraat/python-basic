# 🚀 Quick Start Guide - FastAPI Expense Tracker

Get your expense tracking application running in 3 easy steps!

## 📋 First Time Setup

1. **Run the setup script:**
   ```
   Double-click: setup.bat
   ```
   This will install all dependencies and set up the database.

2. **Start the server:**
   ```
   Double-click: start_server.bat
   ```

3. **Access the application:**
   - Open your browser: http://localhost:8000/docs
   - You'll see the interactive API documentation

That's it! 🎉

---

## 🔄 Daily Usage

### Start the Server
**Option A: With Console Window**
- Double-click `start_server.bat`
- Keep window open while using the app

**Option B: Background Mode**
- Right-click `start_background.ps1` → Run with PowerShell
- Server runs hidden in background

### Stop the Server
**Option A: Console Window**
- Press `Ctrl+C` in the console window

**Option B: Background Mode**
- Right-click `stop_server.ps1` → Run with PowerShell

---

## 🌐 Access Points

| What | URL | Description |
|------|-----|-------------|
| **API Docs** | http://localhost:8000/docs | Interactive API testing |
| **API Base** | http://localhost:8000 | REST API endpoint |
| **ReDoc** | http://localhost:8000/redoc | Alternative docs |

### From Other Devices
1. Find your computer's IP: Run `ipconfig` in Command Prompt
2. Look for IPv4 Address (e.g., 192.168.1.100)
3. Access from phone/tablet: `http://YOUR_IP:8000/docs`

---

## ⚙️ Auto-Start on Computer Boot

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on:
- Task Scheduler setup (recommended)
- Startup folder method
- Windows Service setup

**Quick Method:**
1. Press `Win + R`
2. Type `shell:startup` and press Enter
3. Create a shortcut to `start_server.bat` in that folder
4. Restart computer - app starts automatically!

---

## 📊 API Features

### Available Endpoints

#### Users
- `GET /users/` - List all users
- `POST /users/` - Create new user
- `GET /users/{id}` - Get user details

#### Categories
- `GET /categories/` - List all categories
- `POST /categories/` - Create new category

#### Weights
- `GET /weights/` - List all weight units
- `POST /weights/` - Create new weight

#### Inventory
- `GET /inventory/` - List all inventory items
- `POST /inventory/` - Add new item
- `PUT /inventory/{id}` - Update item
- `DELETE /inventory/{id}` - Delete item

#### Transactions
- `GET /transactions/` - List all transactions
- `POST /transactions/` - Create new transaction
- `GET /transactions/summary` - Get transaction summary
- `PUT /transactions/{id}` - Update transaction
- `DELETE /transactions/{id}` - Delete transaction

---

## 🔧 Troubleshooting

### "Port already in use"
The server is already running. Stop it first:
```powershell
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

### "Module not found"
Run the setup script again:
```
setup.bat
```

### Can't access from other devices
Allow firewall access:
```powershell
# Run PowerShell as Administrator
New-NetFirewallRule -DisplayName "FastAPI Expense Tracker" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
```

### Database errors
Backup and reset:
```
python scripts/backup_database.py
del fastapi.db
python -c "from app.db.session import Base, engine; Base.metadata.create_all(bind=engine)"
```

---

## 🛠️ Maintenance

### Backup Database
```
python scripts/backup_database.py
```
Backups saved to: `backups/`

### Seed Sample Data
```
python scripts/seed_transactions.py
```

### Update Application
```
git pull origin main
pip install -r requirements.txt
```

---

## 📱 Mobile Access Tips

1. **Keep computer running** - Server must be active
2. **Use same WiFi network** - Phone and computer on same network
3. **Use your computer's IP** - Not localhost
4. **Bookmark it** - Save `http://YOUR_IP:8000/docs` on phone
5. **Create web app shortcut** (Android/iOS):
   - Open the URL in browser
   - Use "Add to Home Screen" option

---

## 🔐 Security Notes

- Default setup is for local network use only
- Don't expose to internet without authentication
- Backup database regularly
- See [DEPLOYMENT.md](DEPLOYMENT.md) for security recommendations

---

## 📚 Documentation Files

- `QUICKSTART.md` - This file
- `DEPLOYMENT.md` - Advanced deployment options
- `CONTRIBUTING.md` - Development guidelines
- `README.md` - Full project documentation
- `scripts/SEED_DATA_README.md` - Database seeding info

---

## 💡 Tips & Tricks

1. **Keep the API docs page bookmarked** - It's your main interface
2. **Use "Try it out" buttons** - Test API calls directly from docs
3. **Check the Schemas section** - See data models and field types
4. **Monitor the console** - Watch for errors and requests
5. **Set up auto-start** - Never manually start the server again!

---

## 🆘 Need Help?

1. Check the error message in the console window
2. Review [DEPLOYMENT.md](DEPLOYMENT.md) for detailed setup
3. Check GitHub Issues: https://github.com/aprilmaraat/python-basic/issues
4. Review logs in Task Scheduler (if using auto-start)

---

**Enjoy tracking your expenses! 📈💰**
