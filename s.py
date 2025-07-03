"""
🤖 COMPLETE AUTOMATION TUTORIAL - PYTHON SE AUTOMATION SIKHEIN
================================================================

Is file mein hum different types ke automation dekhenge:
1. File & Folder Automation
2. Web Scraping (bina Selenium ke)
3. System Automation
4. Data Processing Automation
5. Email Automation
6. Database Automation
7. API Automation

Har section mein detailed comments hain Hinglish mein.
"""

import os
import shutil
import time
import requests
import json
import csv
import zipfile
import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import subprocess
import psutil
import schedule
from bs4 import BeautifulSoup
import pandas as pd

# ============================================================================
# 1. FILE & FOLDER AUTOMATION (फाइल और फोल्डर ऑटोमेशन)
# ============================================================================

class FileAutomation:
    """File aur folder related automation ke liye class"""
    
    def __init__(self):
        self.base_folder = "automation_demo"
        self.create_demo_structure()
    
    def create_demo_structure(self):
        """Demo ke liye folder structure banate hain"""
        # Main folder banate hain
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)
            print(f"✅ {self.base_folder} folder create ho gaya")
        
        # Sub folders banate hain
        subfolders = ["documents", "images", "backups", "temp"]
        for folder in subfolders:
            folder_path = os.path.join(self.base_folder, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"✅ {folder} subfolder create ho gaya")
    
    def organize_files_by_extension(self, source_folder):
        """Files ko extension ke hisab se organize karte hain"""
        print(f"\n📁 Files organize kar rahe hain: {source_folder}")
        
        # Har file ko check karte hain
        for filename in os.listdir(source_folder):
            file_path = os.path.join(source_folder, filename)
            
            # Sirf files ko process karte hain, folders ko nahi
            if os.path.isfile(file_path):
                # File ka extension nikalte hain
                file_extension = filename.split('.')[-1].lower()
                
                # Extension ke hisab se destination folder decide karte hain
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    dest_folder = os.path.join(self.base_folder, "images")
                elif file_extension in ['pdf', 'doc', 'docx', 'txt']:
                    dest_folder = os.path.join(self.base_folder, "documents")
                else:
                    dest_folder = os.path.join(self.base_folder, "temp")
                
                # File ko move karte hain
                dest_path = os.path.join(dest_folder, filename)
                shutil.move(file_path, dest_path)
                print(f"📄 {filename} → {dest_folder}")
    
    def backup_files(self, source_folder, backup_name=None):
        """Files ka backup banate hain"""
        if backup_name is None:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_path = os.path.join(self.base_folder, "backups", backup_name)
        
        # Zip file banate hain
        with zipfile.ZipFile(f"{backup_path}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_folder)
                    zipf.write(file_path, arcname)
        
        print(f"💾 Backup create ho gaya: {backup_path}.zip")
        return f"{backup_path}.zip"
    
    def cleanup_old_files(self, folder_path, days_old=30):
        """Purane files ko delete karte hain"""
        print(f"\n🧹 {days_old} din purane files delete kar rahe hain...")
        
        current_time = time.time()
        cutoff_time = current_time - (days_old * 24 * 60 * 60)  # seconds mein convert
        
        deleted_count = 0
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            if os.path.isfile(file_path):
                file_time = os.path.getmtime(file_path)
                if file_time < cutoff_time:
                    os.remove(file_path)
                    deleted_count += 1
                    print(f"🗑️ Deleted: {filename}")
        
        print(f"✅ {deleted_count} purane files delete ho gaye")

# ============================================================================
# 2. WEB SCRAPING AUTOMATION (बिना Selenium के)
# ============================================================================

class WebScrapingAutomation:
    """Web scraping ke liye automation class"""
    
    def __init__(self):
        self.session = requests.Session()
        # Browser jaisa header set karte hain
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_news_headlines(self, url="https://news.ycombinator.com"):
        """News website se headlines scrape karte hain"""
        print(f"\n📰 News headlines scrape kar rahe hain: {url}")
        
        try:
            # Website se data fetch karte hain
            response = self.session.get(url)
            response.raise_for_status()  # Error check karte hain
            
            # HTML parse karte hain
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Headlines extract karte hain (example ke liye)
            headlines = []
            title_elements = soup.find_all('span', class_='titleline')
            
            for i, element in enumerate(title_elements[:10], 1):  # Sirf first 10 headlines
                link = element.find('a')
                if link:
                    headlines.append({
                        'rank': i,
                        'title': link.text.strip(),
                        'url': link.get('href', '')
                    })
            
            # Data ko CSV mein save karte hain
            self.save_to_csv(headlines, 'news_headlines.csv')
            
            print(f"✅ {len(headlines)} headlines scrape ho gaye")
            return headlines
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def scrape_weather_data(self, city="Mumbai"):
        """Weather data scrape karte hain (example API use karke)"""
        print(f"\n🌤️ Weather data fetch kar rahe hain: {city}")
        
        # OpenWeatherMap API (free tier)
        api_key = "YOUR_API_KEY_HERE"  # Aap apna API key use kar sakte hain
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        try:
            response = self.session.get(url)
            data = response.json()
            
            weather_info = {
                'city': city,
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"🌡️ {city}: {weather_info['temperature']}°C, {weather_info['description']}")
            return weather_info
            
        except Exception as e:
            print(f"❌ Weather data fetch nahi ho saka: {e}")
            return None
    
    def save_to_csv(self, data, filename):
        """Data ko CSV file mein save karte hain"""
        if not data:
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        
        print(f"💾 Data save ho gaya: {filename}")

# ============================================================================
# 3. SYSTEM AUTOMATION (सिस्टम ऑटोमेशन)
# ============================================================================

class SystemAutomation:
    """System level automation ke liye class"""
    
    def __init__(self):
        self.system_info = self.get_system_info()
    
    def get_system_info(self):
        """System ki information collect karte hain"""
        info = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
        }
        return info
    
    def monitor_system_resources(self):
        """System resources monitor karte hain"""
        print("\n💻 System Resources Monitor:")
        print(f"🖥️ CPU Usage: {self.system_info['cpu_percent']}%")
        print(f"🧠 Memory Usage: {self.system_info['memory_percent']}%")
        print(f"💾 Disk Usage: {self.system_info['disk_usage']}%")
        print(f"🕐 Boot Time: {self.system_info['boot_time']}")
        
        # Alert system - agar usage high hai
        if self.system_info['cpu_percent'] > 80:
            print("⚠️ WARNING: CPU usage high hai!")
        if self.system_info['memory_percent'] > 80:
            print("⚠️ WARNING: Memory usage high hai!")
    
    def kill_process_by_name(self, process_name):
        """Process ko name se kill karte hain"""
        print(f"\n🔪 Process kill kar rahe hain: {process_name}")
        
        killed_count = 0
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if process_name.lower() in proc.info['name'].lower():
                    proc.kill()
                    killed_count += 1
                    print(f"✅ Killed: {proc.info['name']} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        print(f"🎯 Total {killed_count} processes kill ho gaye")
    
    def run_scheduled_task(self, command, schedule_time="10:00"):
        """Scheduled task run karte hain"""
        print(f"\n⏰ Scheduled task set kar rahe hain: {command} at {schedule_time}")
        
        def task():
            print(f"🚀 Running scheduled task: {command}")
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                print(f"✅ Task completed with output: {result.stdout}")
            except Exception as e:
                print(f"❌ Task failed: {e}")
        
        # Schedule task (daily at specified time)
        schedule.every().day.at(schedule_time).do(task)
        
        # Run scheduler
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

# ============================================================================
# 4. DATA PROCESSING AUTOMATION (डेटा प्रोसेसिंग ऑटोमेशन)
# ============================================================================

class DataProcessingAutomation:
    """Data processing automation ke liye class"""
    
    def __init__(self):
        self.data_folder = "data_files"
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
    
    def create_sample_data(self):
        """Sample data create karte hain processing ke liye"""
        print("\n📊 Sample data create kar rahe hain...")
        
        # Sample CSV data
        sample_data = [
            {'name': 'Rahul', 'age': 25, 'city': 'Mumbai', 'salary': 50000},
            {'name': 'Priya', 'age': 28, 'city': 'Delhi', 'salary': 60000},
            {'name': 'Amit', 'age': 30, 'city': 'Bangalore', 'salary': 70000},
            {'name': 'Neha', 'age': 26, 'city': 'Chennai', 'salary': 55000},
            {'name': 'Vikram', 'age': 32, 'city': 'Pune', 'salary': 65000}
        ]
        
        # CSV file mein save
        df = pd.DataFrame(sample_data)
        df.to_csv(os.path.join(self.data_folder, 'employees.csv'), index=False)
        print("✅ Sample data create ho gaya: employees.csv")
        
        return sample_data
    
    def process_data(self, input_file):
        """Data ko process karte hain"""
        print(f"\n🔄 Data processing kar rahe hain: {input_file}")
        
        try:
            # Data load karte hain
            df = pd.read_csv(input_file)
            
            # Basic statistics
            print(f"📈 Total records: {len(df)}")
            print(f"📊 Average age: {df['age'].mean():.2f}")
            print(f"💰 Average salary: ₹{df['salary'].mean():,.2f}")
            
            # Data analysis
            city_counts = df['city'].value_counts()
            print("\n🏙️ Employees by city:")
            for city, count in city_counts.items():
                print(f"   {city}: {count}")
            
            # High salary employees filter
            high_salary = df[df['salary'] > 60000]
            print(f"\n💎 High salary employees (>₹60k): {len(high_salary)}")
            
            # Processed data save
            output_file = input_file.replace('.csv', '_processed.csv')
            df.to_csv(output_file, index=False)
            print(f"💾 Processed data save ho gaya: {output_file}")
            
            return df
            
        except Exception as e:
            print(f"❌ Data processing error: {e}")
            return None
    
    def generate_report(self, data, report_name="data_report.txt"):
        """Data se report generate karte hain"""
        print(f"\n📋 Report generate kar rahe hain: {report_name}")
        
        report_content = f"""
DATA ANALYSIS REPORT
===================
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY STATISTICS:
- Total Records: {len(data)}
- Average Age: {data['age'].mean():.2f} years
- Average Salary: ₹{data['salary'].mean():,.2f}
- Youngest Employee: {data['age'].min()} years
- Oldest Employee: {data['age'].max()} years

CITY DISTRIBUTION:
{data['city'].value_counts().to_string()}

SALARY ANALYSIS:
- Highest Salary: ₹{data['salary'].max():,.2f}
- Lowest Salary: ₹{data['salary'].min():,.2f}
- Salary Range: ₹{data['salary'].max() - data['salary'].min():,.2f}

TOP 3 HIGHEST PAID EMPLOYEES:
{data.nlargest(3, 'salary')[['name', 'city', 'salary']].to_string(index=False)}
"""
        
        # Report save karte hain
        with open(report_name, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ Report save ho gaya: {report_name}")

# ============================================================================
# 5. EMAIL AUTOMATION (ईमेल ऑटोमेशन)
# ============================================================================

class EmailAutomation:
    """Email automation ke liye class"""
    
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_email(self, to_email, subject, body, attachment_path=None):
        """Email send karte hain"""
        print(f"\n📧 Email send kar rahe hain: {to_email}")
        
        try:
            # Email message create karte hain
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Email body add karte hain
            msg.attach(MIMEText(body, 'plain'))
            
            # Attachment add karte hain (agar hai to)
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}'
                )
                msg.attach(part)
                print(f"📎 Attachment added: {attachment_path}")
            
            # SMTP server se connect karte hain
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            
            # Email send karte hain
            text = msg.as_string()
            server.sendmail(self.email, to_email, text)
            server.quit()
            
            print("✅ Email successfully send ho gaya!")
            return True
            
        except Exception as e:
            print(f"❌ Email send nahi ho saka: {e}")
            return False
    
    def send_automated_report(self, recipient_email, report_file):
        """Automated report email karte hain"""
        subject = f"Automated Report - {datetime.now().strftime('%Y-%m-%d')}"
        body = f"""
Namaste!

Ye automated report hai jo {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ko generate hui hai.

Report attachment mein attached hai.

Best regards,
Automation Bot 🤖
"""
        
        return self.send_email(recipient_email, subject, body, report_file)

# ============================================================================
# 6. DATABASE AUTOMATION (डेटाबेस ऑटोमेशन)
# ============================================================================

class DatabaseAutomation:
    """Database automation ke liye class"""
    
    def __init__(self, db_name="automation.db"):
        self.db_name = db_name
        self.conn = None
        self.setup_database()
    
    def setup_database(self):
        """Database setup karte hain"""
        print(f"\n🗄️ Database setup kar rahe hain: {self.db_name}")
        
        try:
            self.conn = sqlite3.connect(self.db_name)
            cursor = self.conn.cursor()
            
            # Users table create karte hain
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    age INTEGER,
                    city TEXT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Logs table create karte hain
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS automation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT NOT NULL,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            print("✅ Database tables create ho gaye")
            
        except Exception as e:
            print(f"❌ Database setup error: {e}")
    
    def add_user(self, name, email, age, city):
        """User add karte hain database mein"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO users (name, email, age, city)
                VALUES (?, ?, ?, ?)
            ''', (name, email, age, city))
            
            self.conn.commit()
            print(f"✅ User add ho gaya: {name}")
            
            # Log entry add karte hain
            self.log_action("ADD_USER", f"Added user: {name} ({email})")
            
        except sqlite3.IntegrityError:
            print(f"❌ User already exists: {email}")
        except Exception as e:
            print(f"❌ Error adding user: {e}")
    
    def get_users_by_city(self, city):
        """City ke hisab se users get karte hain"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM users WHERE city = ?', (city,))
            users = cursor.fetchall()
            
            print(f"\n👥 Users in {city}: {len(users)}")
            for user in users:
                print(f"   - {user[1]} ({user[2]}) - Age: {user[3]}")
            
            return users
            
        except Exception as e:
            print(f"❌ Error fetching users: {e}")
            return []
    
    def log_action(self, action, details):
        """Automation actions ko log karte hain"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO automation_logs (action, details)
                VALUES (?, ?)
            ''', (action, details))
            
            self.conn.commit()
            
        except Exception as e:
            print(f"❌ Logging error: {e}")
    
    def get_recent_logs(self, limit=10):
        """Recent logs get karte hain"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT action, details, timestamp 
                FROM automation_logs 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            logs = cursor.fetchall()
            
            print(f"\n📋 Recent Automation Logs (Last {limit}):")
            for log in logs:
                print(f"   [{log[2]}] {log[0]}: {log[1]}")
            
            return logs
            
        except Exception as e:
            print(f"❌ Error fetching logs: {e}")
            return []
    
    def close_connection(self):
        """Database connection close karte hain"""
        if self.conn:
            self.conn.close()
            print("🔒 Database connection closed")

# ============================================================================
# 7. API AUTOMATION (API ऑटोमेशन)
# ============================================================================

class APIAutomation:
    """API automation ke liye class"""
    
    def __init__(self):
        self.base_url = "https://jsonplaceholder.typicode.com"  # Free test API
        self.session = requests.Session()
    
    def get_posts(self, limit=5):
        """Posts fetch karte hain API se"""
        print(f"\n📡 API se posts fetch kar rahe hain (limit: {limit})")
        
        try:
            response = self.session.get(f"{self.base_url}/posts?_limit={limit}")
            response.raise_for_status()
            
            posts = response.json()
            
            print(f"✅ {len(posts)} posts fetch ho gaye")
            for i, post in enumerate(posts, 1):
                print(f"   {i}. {post['title'][:50]}...")
            
            return posts
            
        except Exception as e:
            print(f"❌ API error: {e}")
            return []
    
    def create_post(self, title, body, user_id=1):
        """Naya post create karte hain API se"""
        print(f"\n📝 Naya post create kar rahe hain: {title[:30]}...")
        
        try:
            post_data = {
                'title': title,
                'body': body,
                'userId': user_id
            }
            
            response = self.session.post(
                f"{self.base_url}/posts",
                json=post_data
            )
            response.raise_for_status()
            
            created_post = response.json()
            print(f"✅ Post create ho gaya! ID: {created_post['id']}")
            
            return created_post
            
        except Exception as e:
            print(f"❌ Post creation error: {e}")
            return None
    
    def update_post(self, post_id, new_title, new_body):
        """Existing post update karte hain"""
        print(f"\n✏️ Post update kar rahe hain (ID: {post_id})")
        
        try:
            update_data = {
                'title': new_title,
                'body': new_body
            }
            
            response = self.session.put(
                f"{self.base_url}/posts/{post_id}",
                json=update_data
            )
            response.raise_for_status()
            
            updated_post = response.json()
            print(f"✅ Post update ho gaya!")
            
            return updated_post
            
        except Exception as e:
            print(f"❌ Post update error: {e}")
            return None
    
    def delete_post(self, post_id):
        """Post delete karte hain"""
        print(f"\n🗑️ Post delete kar rahe hain (ID: {post_id})")
        
        try:
            response = self.session.delete(f"{self.base_url}/posts/{post_id}")
            response.raise_for_status()
            
            print(f"✅ Post delete ho gaya!")
            return True
            
        except Exception as e:
            print(f"❌ Post deletion error: {e}")
            return False

# ============================================================================
# MAIN AUTOMATION DEMO FUNCTION
# ============================================================================

def run_automation_demo():
    """Complete automation demo run karte hain"""
    print("🚀 AUTOMATION TUTORIAL STARTING...")
    print("=" * 50)
    
    # 1. File Automation Demo
    print("\n📁 1. FILE AUTOMATION DEMO")
    print("-" * 30)
    file_auto = FileAutomation()
    
    # Sample files create karte hain
    sample_files = [
        ("document1.pdf", "documents"),
        ("image1.jpg", "images"),
        ("data.txt", "temp"),
        ("report.docx", "documents")
    ]
    
    for filename, folder in sample_files:
        file_path = os.path.join(file_auto.base_folder, folder, filename)
        with open(file_path, 'w') as f:
            f.write(f"This is a sample {filename} file")
    
    print("✅ Sample files create ho gaye")
    
    # Files organize karte hain
    file_auto.organize_files_by_extension(file_auto.base_folder)
    
    # Backup banate hain
    backup_file = file_auto.backup_files(file_auto.base_folder)
    
    # 2. Web Scraping Demo
    print("\n🌐 2. WEB SCRAPING DEMO")
    print("-" * 30)
    web_auto = WebScrapingAutomation()
    
    # News headlines scrape karte hain
    headlines = web_auto.scrape_news_headlines()
    
    # 3. System Automation Demo
    print("\n💻 3. SYSTEM AUTOMATION DEMO")
    print("-" * 30)
    system_auto = SystemAutomation()
    system_auto.monitor_system_resources()
    
    # 4. Data Processing Demo
    print("\n📊 4. DATA PROCESSING DEMO")
    print("-" * 30)
    data_auto = DataProcessingAutomation()
    
    # Sample data create karte hain
    sample_data = data_auto.create_sample_data()
    
    # Data process karte hain
    input_file = os.path.join(data_auto.data_folder, 'employees.csv')
    processed_data = data_auto.process_data(input_file)
    
    # Report generate karte hain
    if processed_data is not None:
        data_auto.generate_report(processed_data)
    
    # 5. Database Automation Demo
    print("\n🗄️ 5. DATABASE AUTOMATION DEMO")
    print("-" * 30)
    db_auto = DatabaseAutomation()
    
    # Users add karte hain
    users_to_add = [
        ("Rahul Kumar", "rahul@example.com", 25, "Mumbai"),
        ("Priya Singh", "priya@example.com", 28, "Delhi"),
        ("Amit Patel", "amit@example.com", 30, "Bangalore")
    ]
    
    for user in users_to_add:
        db_auto.add_user(*user)
    
    # Users by city get karte hain
    db_auto.get_users_by_city("Mumbai")
    
    # Recent logs dekhte hain
    db_auto.get_recent_logs()
    
    # 6. API Automation Demo
    print("\n📡 6. API AUTOMATION DEMO")
    print("-" * 30)
    api_auto = APIAutomation()
    
    # Posts fetch karte hain
    posts = api_auto.get_posts(3)
    
    # Naya post create karte hain
    if posts:
        new_post = api_auto.create_post(
            "Automation Test Post",
            "Ye automated post hai Python automation se banaya gaya hai!"
        )
        
        if new_post:
            # Post update karte hain
            api_auto.update_post(
                new_post['id'],
                "Updated Automation Test Post",
                "Ye updated automated post hai!"
            )
    
    # Database connection close karte hain
    db_auto.close_connection()
    
    print("\n🎉 AUTOMATION TUTORIAL COMPLETE!")
    print("=" * 50)
    print("Aapne successfully different types ke automation dekhe:")
    print("✅ File & Folder Automation")
    print("✅ Web Scraping (bina Selenium ke)")
    print("✅ System Automation")
    print("✅ Data Processing")
    print("✅ Database Automation")
    print("✅ API Automation")
    print("\nAb aap in sab techniques ko apne projects mein use kar sakte hain!")

# ============================================================================
# SCHEDULED AUTOMATION EXAMPLE
# ============================================================================

def scheduled_automation_example():
    """Scheduled automation ka example"""
    print("\n⏰ SCHEDULED AUTOMATION EXAMPLE")
    print("-" * 30)
    
    def daily_backup():
        """Daily backup task"""
        print("🔄 Daily backup starting...")
        file_auto = FileAutomation()
        backup_file = file_auto.backup_files(file_auto.base_folder)
        print(f"✅ Daily backup complete: {backup_file}")
    
    def weekly_cleanup():
        """Weekly cleanup task"""
        print("🧹 Weekly cleanup starting...")
        file_auto = FileAutomation()
        file_auto.cleanup_old_files(file_auto.base_folder, days_old=7)
        print("✅ Weekly cleanup complete")
    
    def hourly_monitoring():
        """Hourly system monitoring"""
        print("💻 System monitoring...")
        system_auto = SystemAutomation()
        system_auto.monitor_system_resources()
    
    # Schedule tasks
    schedule.every().day.at("02:00").do(daily_backup)
    schedule.every().sunday.at("03:00").do(weekly_cleanup)
    schedule.every().hour.do(hourly_monitoring)
    
    print("📅 Scheduled tasks set ho gaye:")
    print("   - Daily backup: 2:00 AM")
    print("   - Weekly cleanup: Sunday 3:00 AM")
    print("   - Hourly monitoring: Every hour")
    
    # Run scheduler (demo ke liye sirf 1 minute)
    print("\n⏳ Scheduler running for 1 minute (demo)...")
    start_time = time.time()
    while time.time() - start_time < 60:
        schedule.run_pending()
        time.sleep(10)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Main automation demo run karte hain
    run_automation_demo()
    
    # Optional: Scheduled automation demo
    # scheduled_automation_example()
    
    print("\n🎓 AUTOMATION LEARNING COMPLETE!")
    print("Aap ab automation expert ban gaye hain! 🚀") 
