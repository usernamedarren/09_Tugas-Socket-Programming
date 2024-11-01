import csv
import os

class Storage:
    ARCHIVE_FILE = "archive.csv"

    @staticmethod
    def save_message(room_name, user, message_content):
        """Appends a new message entry to the archive, creating the file if needed."""
        is_new_file = not os.path.isfile(Storage.ARCHIVE_FILE)
        
        with open(Storage.ARCHIVE_FILE, 'a', newline='') as archive:
            writer = csv.writer(archive)
            if is_new_file:
                writer.writerow(["Room", "User", "Message"])  # Initialize headers if the file is new
            writer.writerow([room_name, user, message_content])

    @staticmethod
    def load_messages(room_name):
        """Loads all messages associated with a given room, returning them as a list of entries."""
        if not os.path.exists(Storage.ARCHIVE_FILE):
            return []

        with open(Storage.ARCHIVE_FILE, 'r', newline='') as archive:
            reader = csv.reader(archive)
            next(reader, None)  # Skip header
            return [entry for entry in reader if entry[0] == room_name]
