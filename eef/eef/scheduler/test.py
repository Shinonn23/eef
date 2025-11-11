import getpass
import logging
import os
import shutil
import subprocess
import time
import zipfile
from datetime import datetime
from pathlib import Path

import boto3
import frappe

# import frappe
import schedule
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from frappe.commands.site import backup

from eef import ROOT_PATH

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
        s3 = boto3.client(  # type: ignore
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


def test_env():
    log_prefix = "TEST_ENV"

    # พยายามโหลด .env จาก root ของ bench
    # แก้ path ให้ตรงกับของคุณ เช่น "/home/frappe/frappe-bench/.env"
    root_env = ROOT_PATH / ".env"
    if root_env.exists():
        load_dotenv(dotenv_path=root_env)
        frappe.logger().info(f"[{log_prefix}]: Loaded .env from {root_env}")

        # Save to Test doctype
        frappe.get_doc(
            {"doctype": "Test", "test_type": "ENV_LOADED", "message": f"Loaded .env from {root_env}"}
        ).insert(ignore_permissions=True)
    else:
        frappe.logger().warning(f"[{log_prefix}]: .env not found at {root_env}")

        # Save to Test doctype
        frappe.get_doc(
            {"doctype": "Test", "test_type": "ENV_NOT_FOUND", "message": f".env not found at {root_env}"}
        ).insert(ignore_permissions=True)

    env_sample = {
        "aws_access_key_id": os.getenv("aws_access_key_id"),
        "aws_secret_access_key": os.getenv("aws_secret_access_key"),
        "aws_bucket_name": os.getenv("aws_bucket_name"),
        "endpoint_url": os.getenv("endpoint_url"),
    }

    # Save debug info to Test doctype
    debug_message = (
        f"Current working dir: {os.getcwd()}\n"
        f"Running as user: {getpass.getuser()}\n"
        f"TEMP PATH: {Path('/tmp').resolve()}\n"
        f"ENV SAMPLE: {env_sample}"
    )

    frappe.get_doc({"doctype": "Test", "test_type": "ENV_DEBUG", "message": debug_message}).insert(
        ignore_permissions=True
    )

    frappe.db.commit()

    frappe.logger().info(f"[{log_prefix}]: ENV TEST completed. Check Test doctype for details.")


def test_backup():
    """Test backup functionality and save all logs to Test doctype"""
    log_prefix = "TEST_BACKUP"
    logs = []
    test_status = "BACKUP_TEST_SUCCESS"  # Default status

    def add_log(message: str):
        """Helper function to add log to both logger and logs list"""
        logger.info(message)
        logs.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")

    try:
        add_log(f"[{log_prefix}:INFO]: Test backup process started.")

        # Check if we're in Frappe context
        if not frappe.db:
            error_msg = (
                f"[{log_prefix}:ERROR]: Not in Frappe context. Please run this function within Frappe."
            )
            add_log(error_msg)
            logger.error(error_msg)
            logger.error("Please run: bench --site <site-name> console")
            logger.error("Then execute: from eef.eef.scheduler.test import test_backup; test_backup()")
            return

        add_log(f"[{log_prefix}:INFO]: Frappe context OK - Site: {frappe.local.site}")
    except Exception as e:
        logger.error(f"[{log_prefix}:ERROR]: Failed to initialize - {e!s}")
        return

    # Check environment variables
    env_vars_status = {}
    required_vars = ["aws_access_key_id", "aws_secret_access_key", "endpoint_url", "aws_bucket_name"]

    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if "key" in var.lower() or "secret" in var.lower():
                env_vars_status[var] = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
            else:
                env_vars_status[var] = value
        else:
            env_vars_status[var] = "NOT SET"

    add_log(f"[{log_prefix}:INFO]: Environment variables status: {env_vars_status}")

    # Check if all required vars are set
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        error_msg = f"[{log_prefix}:ERROR]: Missing required environment variables: {', '.join(missing_vars)}"
        add_log(error_msg)
        test_status = "BACKUP_TEST_FAILED"
        logger.error(error_msg)

        # Save all logs at the end
        frappe.get_doc({"doctype": "Test", "test_type": test_status, "message": "\n".join(logs)}).insert(
            ignore_permissions=True
        )
        frappe.db.commit()
        return

    # Create test backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    add_log(f"[{log_prefix}:INFO]: Creating test backup with timestamp: {timestamp}")

    try:
        # Create temp directory
        os.makedirs(TEMP_PATH, exist_ok=True)
        add_log(f"[{log_prefix}:INFO]: Temp directory created at: {TEMP_PATH}")

        db_path = TEMP_PATH / f"{timestamp}-database.sql.gz"
        conf_path = TEMP_PATH / f"{timestamp}-site_config.json"
        files_path = TEMP_PATH / f"{timestamp}-public-files"
        private_path = TEMP_PATH / f"{timestamp}-private-files"

        add_log(f"[{log_prefix}:INFO]: Running Frappe backup command...")

        # Run backup using frappe.utils.backups
        from frappe.utils.backups import new_backup

        new_backup(
            ignore_files=False,  # False means include files
            backup_path_db=str(db_path),
            backup_path_conf=str(conf_path),
            backup_path_files=str(files_path),
            backup_path_private_files=str(private_path),
            compress=True,
        )

        add_log(f"[{log_prefix}:INFO]: Backup command completed successfully")

        # Check created files
        created_files = []
        for f in [db_path, conf_path, files_path, private_path]:
            if os.path.exists(f):
                if os.path.isdir(f):
                    file_count = sum(1 for _ in Path(f).rglob("*") if _.is_file())
                    size = sum(_.stat().st_size for _ in Path(f).rglob("*") if _.is_file())
                    created_files.append(f"{f.name}: {file_count} files, {size / 1024 / 1024:.2f} MB")
                else:
                    size = os.path.getsize(f)
                    created_files.append(f"{f.name}: {size / 1024 / 1024:.2f} MB")

        add_log(f"[{log_prefix}:INFO]: Created files: {', '.join(created_files)}")

        # Create zip file
        zip_filename = TEMP_PATH / f"{timestamp}-backup.zip"
        add_log(f"[{log_prefix}:INFO]: Creating zip file: {zip_filename.name}")

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

        zip_size = os.path.getsize(zip_filename) / 1024 / 1024
        add_log(f"[{log_prefix}:INFO]: Zip file created successfully, size: {zip_size:.2f} MB")

        # Test S3 connection and upload
        add_log(f"[{log_prefix}:INFO]: Testing S3 connection...")

        try:
            s3 = boto3.client(
                "s3",
                aws_access_key_id=os.getenv("aws_access_key_id"),
                aws_secret_access_key=os.getenv("aws_secret_access_key"),
                endpoint_url=os.getenv("endpoint_url"),
            )

            bucket_name = os.getenv("aws_bucket_name")
            add_log(f"[{log_prefix}:INFO]: S3 client created, target bucket: {bucket_name}")

            # Test upload
            s3_key = os.path.basename(zip_filename)
            add_log(f"[{log_prefix}:INFO]: Uploading {s3_key} to bucket {bucket_name}...")

            s3.upload_file(str(zip_filename), bucket_name, s3_key)

            add_log(f"[{log_prefix}:INFO]: Upload successful!")
            add_log(f"[{log_prefix}:INFO]: File uploaded as: {s3_key}")
            test_status = "BACKUP_TEST_SUCCESS"

        except ClientError as e:
            error_msg = f"[{log_prefix}:ERROR]: S3 upload failed - {e!s}"
            add_log(error_msg)
            test_status = "BACKUP_TEST_S3_ERROR"

    except subprocess.CalledProcessError as e:
        error_msg = f"[{log_prefix}:ERROR]: Backup command failed - {e!s}"
        add_log(error_msg)
        test_status = "BACKUP_TEST_COMMAND_ERROR"

    except Exception as e:
        error_msg = f"[{log_prefix}:ERROR]: Unexpected error - {e!s}"
        add_log(error_msg)
        test_status = "BACKUP_TEST_ERROR"

    finally:
        # Cleanup
        add_log(f"[{log_prefix}:INFO]: Cleaning up temp files...")
        shutil.rmtree(TEMP_PATH, ignore_errors=True)
        add_log(f"[{log_prefix}:INFO]: Test backup completed. Check Test doctype for details.")

        logger.info(f"[{log_prefix}:INFO]: Test completed. Total logs: {len(logs)}")

        # Save all logs to Test doctype in one document
        try:
            # Prepare final message before saving
            final_message = "\n".join(logs)
            log_save_msg = f"[{log_prefix}:INFO]: Saving logs to Test doctype with status: {test_status}"
            logger.info(log_save_msg)

            doc = frappe.get_doc({
                "doctype": "Test",
                "test_type": test_status,
                "message": final_message
            })

            logger.info(f"[{log_prefix}:INFO]: Document created, inserting...")
            doc.insert(ignore_permissions=True)

            logger.info(f"[{log_prefix}:INFO]: Document inserted with name: {doc.name}, committing...")
            frappe.db.commit()

            logger.info(f"[{log_prefix}:SUCCESS]: Logs saved successfully to Test document: {doc.name}")

        except Exception as save_error:
            logger.error(f"[{log_prefix}:ERROR]: Failed to save logs to database: {save_error!s}")
            logger.error(f"[{log_prefix}:ERROR]: Exception type: {type(save_error).__name__}")
            logger.error(f"[{log_prefix}:ERROR]: All logs:\n{final_message}")
            import traceback
            logger.error(f"[{log_prefix}:ERROR]: Traceback:\n{traceback.format_exc()}")
