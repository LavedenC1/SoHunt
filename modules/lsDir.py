import os

def lsDir(folder_path):
  try:
    files = os.listdir(folder_path)
    return [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
  except FileNotFoundError:
    return []
  except Exception as e:
      print(f"An error occurred: {e}")
      return []