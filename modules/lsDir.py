import os

def lsDir(folder_path):
  try:
    files = os.listdir(folder_path)
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f)) and f != '.donttouch']
    return files
  
  except FileNotFoundError:
    return []
  except Exception as e:
      print(f"An error occurred: {e}")
      return []
  
if __name__ == "__main__":
    print(lsDir(input("Enter directory path: ")))