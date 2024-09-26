import os
from dotenv import load_dotenv
import subprocess
from datetime import datetime, timedelta

# Tải các biến môi trường từ tệp .env
load_dotenv()

# Lấy thông tin kết nối từ các biến môi trường
src_pg_host = os.getenv('SRC_PG_HOST')
src_pg_port = os.getenv('SRC_PG_PORT')
src_pg_user = os.getenv('SRC_PG_USER')
src_pg_password = os.getenv('SRC_PG_PASSWORD')

dest_pg_host = os.getenv('DEST_PG_HOST')
dest_pg_port = os.getenv('DEST_PG_PORT')
dest_pg_user = os.getenv('DEST_PG_USER')
dest_pg_password = os.getenv('DEST_PG_PASSWORD')

pg_database = os.getenv('PG_DATABASE')

# Tạo tên file backup với thời gian hiện tại (UTC+7)
current_time = datetime.utcnow() + timedelta(hours=7)
backup_file = f"./dump/{pg_database}_{current_time.strftime('%Y%m%d_%H%M%S')}.dump"

# Tạo lệnh pg_dump
dump_command = f'pg_dump -h {src_pg_host} -p {src_pg_port} -U {src_pg_user} --no-owner --no-privileges -F c -b -v -f {backup_file} {pg_database}'

# Tạo lệnh pg_restore
restore_command = f'pg_restore -h {dest_pg_host} -p {dest_pg_port} -U {dest_pg_user} -d {pg_database} -v {backup_file}'

# Thiết lập biến môi trường PGPASSWORD cho pg_dump và pg_restore
src_env = os.environ.copy()
src_env['PGPASSWORD'] = src_pg_password

dest_env = os.environ.copy()
dest_env['PGPASSWORD'] = dest_pg_password

# Chạy lệnh pg_dump
try:
    print("Starting database backup...")
    subprocess.run(dump_command, shell=True, check=True, env=src_env)
    print(f"Database backup completed successfully. Backup file: {backup_file}")
except subprocess.CalledProcessError as e:
    print(f"Backup Error: {e}")

# Chạy lệnh pg_restore
try:
    print("Starting database restore...")
    subprocess.run(restore_command, shell=True, check=True, env=dest_env)
    print("Database restore completed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Restore Error: {e}")
