import os
import shutil
import sys
import re
from unidecode import unidecode
import zipfile
import tarfile
import gzip


def normalize(filename):
    # Транслітерація літер
    filename = unidecode(filename)

    # Заміна всіх символів, крім літер і цифр, на "_"
    filename = re.sub(r"[^\w.]", "_", filename)

    return filename


def sort_files_by_type(folder_path):
    extensions = {
        'image': ('.jpeg', '.jpg', '.png', '.svg'),
        'video': ('.avi', '.mp4', '.mov', '.mkv'),
        'document': ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
        'audio': ('.mp3', '.ogg', '.wav', '.amr'),
        'archive': ('.zip', '.tar', '.gz')
    }

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[-1].lower()
            file_type = 'unknown'

            for key, exts in extensions.items():
                if file_extension in exts:
                    file_type = key
                    break

            if file_type == 'unknown':
                destination_folder = os.path.join(folder_path, 'unknown')
                os.makedirs(destination_folder, exist_ok=True)
                destination_path = os.path.join(
                    destination_folder, file)
                shutil.copy2(file_path, destination_path)
                os.remove(file_path)
            else:
                destination_folder = os.path.join(folder_path, file_type)
                os.makedirs(destination_folder, exist_ok=True)

                normalized_filename = normalize(file)

                if file_extension == '.zip':
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(destination_folder)
                elif file_extension in ('.tar', '.gz'):
                    with tarfile.open(file_path, 'r') as tar_ref:
                        tar_ref.extractall(destination_folder)
                else:
                    destination_path = os.path.join(
                        destination_folder, normalized_filename)
                    shutil.move(file_path, destination_path)

            print(
                f"Переміщено файл '{file}' до папки '{destination_folder}' з нормалізованим ім'ям '{normalized_filename}'")

    print("Сортування файлів за типом та нормалізація імен завершено")

    remove_empty_folders(folder_path)


def remove_empty_folders(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"Видалено пусту папку '{dir_path}'")

    print("Видалення пустих папок завершено")


def main():
    if len(sys.argv) < 2:
        print("Потрібно вказати шлях до папки")
        sys.exit(1)

    folder_path = sys.argv[1]
    sort_files_by_type(folder_path)


if __name__ == '__main__':
    main()
