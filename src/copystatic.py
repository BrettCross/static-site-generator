import os.path
import shutil


def copy_files_recursive(source_dir_path, target_dir_path):

    # does target exist? 
    if not os.path.exists(target_dir_path):
        os.mkdir(target_dir_path)

    # for files in source_dir_path
    # check if file is file
    # if not recurse

    for filename in os.listdir(source_dir_path):
        source_path = os.path.join(source_dir_path, filename)
        target_path = os.path.join(target_dir_path, filename)

        print(f" * {source_path} -> {target_path}")
        # can copy source to target if file
        if os.path.isfile(source_path):
            shutil.copy(source_path, target_path)
        # it's a directory so drill down into it
        else:
            copy_files_recursive(source_path, target_path)