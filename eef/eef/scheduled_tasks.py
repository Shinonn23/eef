import logging
import os
import shutil
import subprocess
import time
import zipfile
from datetime import datetime
from pathlib import Path

import boto3

# import frappe
import schedule
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from frappe.commands.site import backup

from eef import ROOT_PATH
from eef.utils.discord_hooks import send_discord_webhook

TEMP_PATH = ROOT_PATH / "temp"
dotenv_path = ROOT_PATH / ".env"

MAX_RETRIES = 10

load_dotenv(dotenv_path=dotenv_path)

if (
    "aws_access_key_id" not in os.environ
    or "aws_secret_access_key" not in os.environ
    or "endpoint_url" not in os.environ
    or "aws_bucket_name" not in os.environ
):
    raise OSError("Missing required AWS environment variables in .env file")

# Remove frappe logger and set up Python logging to console
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def upload_to_storage(zip_path: Path) -> bool:
    log_prefix = "UPLOAD_TO_STORAGE"
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("aws_access_key_id"),
            aws_secret_access_key=os.getenv("aws_secret_access_key"),
            endpoint_url=os.getenv("endpoint_url"),
        )

        bucket_name = os.getenv("aws_bucket_name")
        s3_key = os.path.basename(zip_path)

        logger.info(f"[{log_prefix}:INFO]: Uploading {s3_key} to bucket {bucket_name}...")

        s3.upload_file(str(zip_path), bucket_name, s3_key)

        logger.info(f"[{log_prefix}:INFO]: Upload successful: {s3_key}")
        return True

    except ClientError as e:
        logger.error(
            f"[{log_prefix}:ERROR]: Upload failed due to client error: {e}",
            exc_info=True,
        )
        return False
    except FileNotFoundError:
        logger.error(f"[{log_prefix}:ERROR]: The file {zip_path} was not found.", exc_info=True)
        return False
    except Exception as e:
        logger.error(
            f"[{log_prefix}:ERROR]: An unexpected error occurred during upload: {e}",
            exc_info=True,
        )
        return False


def backup_daily():
    log_prefix = "BACKUP_DAILY"
    logger.info(f"[{log_prefix}:INFO]: Backup process started.")

    # Send a test message to Discord webhook for debugging
    send_discord_webhook(
        source="backup_daily", message=f"Sent @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # ตรวจสอบว่า env vars โหลดมาครบหรือไม่ก่อนเริ่ม
    if "aws_access_key_id" not in os.environ:
        logger.error(f"[{log_prefix}:ERROR]: Cannot start backup, AWS credentials are not configured.")
        return

    for attempt in range(1, MAX_RETRIES + 1):
        logger.info(f"[{log_prefix}:INFO]: Backup attempt {attempt}/{MAX_RETRIES}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(TEMP_PATH, exist_ok=True)

        db_path = TEMP_PATH / f"{timestamp}-database.sql.gz"
        conf_path = TEMP_PATH / f"{timestamp}-site_config.json"
        files_path = TEMP_PATH / f"{timestamp}-public-files"
        private_path = TEMP_PATH / f"{timestamp}-private-files"

        try:
            # Use Frappe's programmatic backup command instead of invoking bench via subprocess.
            # The CLI command signature is: backup(context, with_files=..., backup_path=..., backup_path_db=..., ...)
            # Pass a None context since we're calling it programmatically from code.
            backup(
                None,
                with_files=True,
                backup_path_db=str(db_path),
                backup_path_conf=str(conf_path),
                backup_path_files=str(files_path),
                backup_path_private_files=str(private_path),
                compress=True,
            )

            # บีบอัดไฟล์ทั้งหมดเป็น zip เดียว
            zip_filename = TEMP_PATH / f"{timestamp}-backup.zip"
            with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
                for f in [db_path, conf_path, files_path, private_path]:
                    if os.path.exists(f):
                        if os.path.isdir(f):
                            for root, _dirs, files in os.walk(f):
                                for file in files:
                                    full_path = Path(root) / file
                                    arcname = full_path.relative_to(TEMP_PATH)
                                    zipf.write(full_path, arcname)
                        else:
                            zipf.write(f, os.path.basename(f))

            # อัปโหลดไฟล์
            success = upload_to_storage(zip_filename)

            if success:
                logger.info(f"[{log_prefix}:INFO]: Backup and upload successful!")
                break
            else:
                logger.warning(f"[{log_prefix}:WARNING]: Upload failed on attempt {attempt}, retrying...")

        except subprocess.CalledProcessError as e:
            logger.error(
                f"[{log_prefix}:ERROR]: Backup command failed on attempt {attempt}: {e.stderr}",
                exc_info=True,
            )
        except Exception as e:
            logger.error(
                f"[{log_prefix}:ERROR]: An unexpected error occurred on attempt {attempt}: {e}",
                exc_info=True,
            )

        finally:
            logger.info(f"[{log_prefix}:INFO]: Cleaning up temp files for attempt {attempt}.")
            shutil.rmtree(TEMP_PATH, ignore_errors=True)
            if attempt < MAX_RETRIES:
                time.sleep(5)
    else:
        logger.error(f"[{log_prefix}:CRITICAL]: Backup failed after {MAX_RETRIES} attempts.")


def run_scheduled_backup():
    """Callback function that runs the backup process at scheduled time"""
    log_prefix = "SCHEDULED_BACKUP"
    logger.info(f"[{log_prefix}:INFO]: Scheduled backup triggered at {datetime.now()}")
    backup_daily()


def start_scheduler():
    """Start the scheduler to run backup at midnight every day"""
    log_prefix = "SCHEDULER"
    logger.info(f"[{log_prefix}:INFO]: Starting backup scheduler...")

    # Schedule backup to run at midnight (00:00) every day
    schedule.every().day.at("00:00").do(run_scheduled_backup)

    logger.info(f"[{log_prefix}:INFO]: Backup scheduled to run at 00:00 every day")

    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    # backup_daily()
    start_scheduler()
