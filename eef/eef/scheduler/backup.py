import logging
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from frappe.utils.backups import new_backup

from eef import ROOT_PATH
from eef.utils.discord_hooks import send_discord_webhook

TEMP_PATH = ROOT_PATH / "temp"
dotenv_path = ROOT_PATH / ".env"
MAX_RETRIES = 10

load_dotenv(dotenv_path=dotenv_path)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def upload_to_storage(zip_path: Path) -> bool:
    """Upload backup file to S3 storage"""
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
        logger.error(f"[{log_prefix}:ERROR]: Upload failed due to client error: {e}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"[{log_prefix}:ERROR]: Unexpected upload error: {e}", exc_info=True)
        return False


def check_file_exists_in_storage(filename: str) -> bool:
    """Check if a specific file exists in S3 storage

    Args:
        filename (str): The filename to check (just the filename, not full path)

    Returns:
        bool: True if file exists, False otherwise
    """
    log_prefix = "CHECK_FILE_EXISTS"
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("aws_access_key_id"),
            aws_secret_access_key=os.getenv("aws_secret_access_key"),
            endpoint_url=os.getenv("endpoint_url"),
        )

        bucket_name = os.getenv("aws_bucket_name")
        logger.info(f"[{log_prefix}:INFO]: Checking if {filename} exists in bucket {bucket_name}...")

        # Use head_object to check if file exists without downloading it
        s3.head_object(Bucket=bucket_name, Key=filename)

        logger.info(f"[{log_prefix}:INFO]: File {filename} exists in storage")
        return True

    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            logger.info(f"[{log_prefix}:INFO]: File {filename} does not exist in storage")
        else:
            logger.error(f"[{log_prefix}:ERROR]: Error checking file: {e}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"[{log_prefix}:ERROR]: Unexpected error: {e}", exc_info=True)
        return False


def backup_daily():
    """Daily backup function - creates backup and uploads to S3"""
    log_prefix = "BACKUP_DAILY"
    logger.info(f"[{log_prefix}:INFO]: Backup process started.")

    send_discord_webhook(
        source="backup_daily",
        message=f"@ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Starting backup process",
    )

    # Check environment variables
    required_vars = ["aws_access_key_id", "aws_secret_access_key", "endpoint_url", "aws_bucket_name"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        logger.error(f"[{log_prefix}:ERROR]: Missing environment variables: {', '.join(missing_vars)}")
        send_discord_webhook(
            source="backup_daily",
            message=f"@ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:❌ Backup failed: Missing environment variables: {', '.join(missing_vars)}",
        )
        return

    backup_success = False
    for attempt in range(1, MAX_RETRIES + 1):
        logger.info(f"[{log_prefix}:INFO]: Backup attempt {attempt}/{MAX_RETRIES}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(TEMP_PATH, exist_ok=True)

        db_path = TEMP_PATH / f"{timestamp}-database.sql.gz"
        conf_path = TEMP_PATH / f"{timestamp}-site_config.json"
        files_path = TEMP_PATH / f"{timestamp}-public-files"
        private_path = TEMP_PATH / f"{timestamp}-private-files"

        try:
            # Create backup using Frappe's backup utility
            logger.info(f"[{log_prefix}:INFO]: Running Frappe backup...")
            new_backup(
                ignore_files=False,
                backup_path_db=str(db_path),
                backup_path_conf=str(conf_path),
                backup_path_files=str(files_path),
                backup_path_private_files=str(private_path),
                compress=True,
            )
            logger.info(f"[{log_prefix}:INFO]: Backup command completed")

            # Create zip file
            zip_filename = TEMP_PATH / f"{timestamp}-backup.zip"
            logger.info(f"[{log_prefix}:INFO]: Creating zip: {zip_filename.name}")

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
            logger.info(f"[{log_prefix}:INFO]: Zip created: {zip_size:.2f} MB")

            # Upload to S3
            success = upload_to_storage(zip_filename)

            if success:
                # Verify file exists in storage
                logger.info(f"[{log_prefix}:INFO]: Verifying backup file in storage...")
                file_exists = check_file_exists_in_storage(zip_filename.name)

                if file_exists:
                    logger.info(
                        f"[{log_prefix}:INFO]: Backup and upload successful! File verified in storage."
                    )
                    backup_success = True
                    break
                else:
                    logger.warning(
                        f"[{log_prefix}:WARNING]: File verification failed on attempt {attempt}, retrying..."
                    )
            else:
                logger.warning(f"[{log_prefix}:WARNING]: Upload failed on attempt {attempt}, retrying...")

        except Exception as e:
            logger.error(f"[{log_prefix}:ERROR]: Backup failed on attempt {attempt}: {e}", exc_info=True)

        finally:
            logger.info(f"[{log_prefix}:INFO]: Cleaning up temp files for attempt {attempt}.")
            shutil.rmtree(TEMP_PATH, ignore_errors=True)
            if attempt < MAX_RETRIES:
                import time

                time.sleep(5)
    else:
        logger.error(f"[{log_prefix}:CRITICAL]: Backup failed after {MAX_RETRIES} attempts")

    # Send final result notification
    if backup_success:
        send_discord_webhook(
            source="backup_daily",
            message=f"@ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:✅ Backup completed successfully @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        )
    else:
        send_discord_webhook(
            source="backup_daily",
            message=f"@ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:❌ Backup failed after {MAX_RETRIES} attempts @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        )


if __name__ == "__main__":
    backup_daily()
