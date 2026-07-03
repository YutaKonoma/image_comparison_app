import os
import imagehash
from PIL import Image
import platform
import subprocess

def find_duplicates(folder_path, threshold=8, progress_callback=None):
    hashes = {}
    duplicates = []
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')

    if not os.path.exists(folder_path):
        return []

    files = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]
    total_files = len(files)

    for i, filename in enumerate(files):
        path = os.path.join(folder_path, filename)

        # 進捗をUI側に伝える（コールバック）
        if progress_callback:
            progress_callback(i + 1, total_files, filename)

        try:
            with Image.open(path) as img:
                h = imagehash.phash(img)
                for existing_hash, existing_path in hashes.items():
                    if h - existing_hash <= threshold:
                        duplicates.append((existing_path, path))
                hashes[h] = path
        except:
            continue

    return duplicates

def open_folder_at_path(path):
    """ファイルが存在するフォルダをFinder/エクスプローラーで開く"""
    folder = os.path.dirname(path)
    if platform.system() == "Windows":
        os.startfile(folder)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", folder])
    else:  # Linux
        subprocess.run(["xdg-open", folder])

def delete_file(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            return True
    except:
        return False
