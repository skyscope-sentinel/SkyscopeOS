import os
import shutil
import hashlib
import json
import datetime

class RollbackManager:
    """
    Manages snapshots and rollbacks for critical system files.
    """

    def __init__(self, snapshot_dir: str = os.path.expanduser("~/.skyscope_unified/snapshots")):
        self.snapshot_dir = snapshot_dir
        os.makedirs(self.snapshot_dir, exist_ok=True)

    def _get_file_hash(self, filepath: str) -> str:
        """Calculates the SHA256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def create_snapshot(self, filepaths: list[str], metadata: dict = None) -> (str, str):
        """
        Creates a snapshot of a list of files.
        Returns the snapshot ID and an error message, if any.
        """
        snapshot_id = f"snapshot_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        snapshot_path = os.path.join(self.snapshot_dir, snapshot_id)

        try:
            os.makedirs(snapshot_path, exist_ok=True)
            snapshot_metadata = {
                "snapshot_id": snapshot_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "files": {},
                "user_metadata": metadata or {}
            }

            for filepath in filepaths:
                if not os.path.exists(filepath):
                    continue # Or raise an error, depending on desired behavior

                backup_path = os.path.join(snapshot_path, os.path.basename(filepath))
                shutil.copy2(filepath, backup_path)

                snapshot_metadata["files"][filepath] = {
                    "original_path": filepath,
                    "backup_path": backup_path,
                    "original_hash": self._get_file_hash(filepath)
                }

            with open(os.path.join(snapshot_path, "metadata.json"), "w") as f:
                json.dump(snapshot_metadata, f, indent=4)

            return (snapshot_id, None)

        except Exception as e:
            # Clean up a partially created snapshot
            if os.path.exists(snapshot_path):
                shutil.rmtree(snapshot_path)
            return (None, f"Failed to create snapshot: {str(e)}")

    def rollback(self, snapshot_id: str) -> (bool, str):
        """
        Rolls back the system to a specified snapshot.
        """
        snapshot_path = os.path.join(self.snapshot_dir, snapshot_id)
        metadata_path = os.path.join(snapshot_path, "metadata.json")

        if not os.path.exists(metadata_path):
            return (False, f"Snapshot '{snapshot_id}' not found.")

        try:
            with open(metadata_path, "r") as f:
                metadata = json.load(f)

            for original_path, file_info in metadata["files"].items():
                backup_path = file_info["backup_path"]
                if os.path.exists(backup_path):
                    shutil.copy2(backup_path, original_path)

            return (True, f"Successfully rolled back to snapshot '{snapshot_id}'.")

        except Exception as e:
            return (False, f"Failed to rollback snapshot: {str(e)}")

# Example Usage:
if __name__ == '__main__':
    manager = RollbackManager()

    # Create a dummy file to snapshot
    with open("testfile.txt", "w") as f:
        f.write("This is the original content.")

    # Create a snapshot
    snapshot_id, error = manager.create_snapshot(["testfile.txt"], {"description": "Test snapshot"})
    if error:
        print(error)
    else:
        print(f"Created snapshot: {snapshot_id}")

    # Modify the file
    with open("testfile.txt", "w") as f:
        f.write("This is the modified content.")

    print("File modified.")
    with open("testfile.txt", "r") as f:
        print(f"Current content: {f.read()}")

    # Rollback the change
    success, message = manager.rollback(snapshot_id)
    print(message)

    if success:
        with open("testfile.txt", "r") as f:
            print(f"Content after rollback: {f.read()}")

    # Clean up
    os.remove("testfile.txt")
    shutil.rmtree(os.path.expanduser("~/.skyscope_unified/snapshots"))
