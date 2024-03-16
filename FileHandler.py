import os
import shutil

class FileHandler:
    def __init__(self, source_folder, destination_folder, current_sample_ID):
        self.src = source_folder
        self.dsc = destination_folder
        self.curr = current_sample_ID

    def rename_and_move(self, suffix):
        # Get the list of files in the source folder
        files = os.listdir(self.src)

        # Get the path of the file in the source folder
        file_name = files[0]
        source_path = os.path.join(self.src, file_name)

        # Construct the new file name based on the current sample ID and suffix
        new_file_name = self.curr + '_' + suffix
        destination_path = os.path.join(self.dsc, new_file_name)

        # Rename and move the file
        try:
            shutil.move(source_path, destination_path)
            print(f"File successfully renamed and moved to {destination_path}")
        except Exception as e:
            print(f"Error: {e}")
