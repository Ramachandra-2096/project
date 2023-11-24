import os

def delete_photos(directory_path):
    try:
        # Ensure the specified path exists
        if not os.path.exists(directory_path):
            print(f"The specified directory '{directory_path}' does not exist.")
            return

        # Iterate over files in the directory and delete photos
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            try:
                if os.path.isfile(file_path) and file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    os.remove(file_path)
                    print(f"Deleted photo: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {str(e)}")

        print("Photos deleted successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Specify the directory path where photos should be deleted
    target_directory = "static/payment"

    # Call the function to delete photos
    delete_photos(target_directory)
    target_directory = "static\Qr_code"

    # Call the function to delete photos
    delete_photos(target_directory)
