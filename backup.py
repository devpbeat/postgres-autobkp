import os
import subprocess
import logging
from dotenv import load_dotenv

class DatabaseManager:
    """
    A class to manage the backup, transfer, and restoration of a PostgreSQL database.
    """

    def __init__(self, backup_path, local_path):
        """
        Constructs all the necessary attributes for the DatabaseManager object.

        :param backup_path: str, path where the database dump will be saved
        :param local_path: str, path where the database dump will be loaded on the local machine
        """
        load_dotenv()
        self.backup_path = backup_path
        self.local_path = local_path
        self.db_username = os.getenv("DB_USERNAME")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_NAME")
        self.local_username = os.getenv("LOCAL_USERNAME")
        self.local_dbname = os.getenv("LOCAL_DBNAME")
        self.remote_host = os.getenv("REMOTE_HOST") # The IP address or domain of the remote host
        logging.basicConfig(level=logging.INFO)
        
    def backup_db(self):
        """
        Backs up the PostgreSQL database using the pg_dump command on the remote machine.
        """
        logging.info("Starting the database backup process")
        try:
            subprocess.run(["ssh", self.remote_host, "pg_dump", "-U", self.db_username, "-W", self.db_password, "-F", "c", "-b", "-v", "-f", self.backup_path, self.db_name], check=True)
            logging.info("Database backup was successful")
        except subprocess.CalledProcessError as e:
            logging.error(f"Process error during backup: {e}")
        except Exception as e:
            logging.error(f"Unexpected error during backup: {e}")
    
    def transfer_db_dump(self):
        """
        Transfers the database dump from the remote machine to the local machine using the scp command.
        """
        logging.info("Starting the database dump transfer process")
        try:
            subprocess.run(["scp", self.remote_host + ":" + self.backup_path, self.local_path], check=True)
            logging.info("Database dump transfer was successful")
        except subprocess.CalledProcessError as e:
            logging.error(f"Process error during dump transfer: {e}")
        except Exception as e:
            logging.error(f"Unexpected error during dump transfer: {e}")
            
    def apply_db_dump(self):
        """
        Applies the database dump to the local PostgreSQL database using the pg_restore command.
        """
        logging.info("Starting the database dump application process")
        try:
            subprocess.run(["pg_restore", "-U", self.local_username, "-d", self.local_dbname, "-1", self.local_path], check=True)
            logging.info("Database dump application was successful")
        except subprocess.CalledProcessError as e:
            logging.error(f"Process error during dump application: {e}")
        except Exception as e:
            logging.error(f"Unexpected error during dump application: {e}")
    
    def perform_all(self):
        """
        Performs the backup, transfer, and application of the database dump.
        """
        self.backup_db()
        self.transfer_db_dump()
        self.apply_db_dump()

if __name__ == "__main__":
    manager = DatabaseManager("/path/to/dump/file.sql", "/path/to/local/directory/file.sql")
    manager.perform_all()
