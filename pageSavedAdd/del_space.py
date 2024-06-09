import os  
import shutil  
  
def remove_spaces_in_filenames(directory):  
    for root, dirs, files in os.walk(directory):  
        for file in files:  
            # 构造文件的完整路径  
            file_path = os.path.join(root, file)  
            print(f"file_path:{file_path}")
            # 替换" ."和" &"前紧跟的空格  
            new_name = file.replace(' .', '.').replace(' &', '').replace('&', '')
              
            # 如果文件名发生了改变，则重命名文件  
            if new_name != file:  
                new_file_path = os.path.join(root, new_name)  
                  
                # 检查新的文件名是否已经存在  
                if os.path.exists(new_file_path):  
                    # 如果存在，则覆盖它（请确保这是你想要的行为）  
                    print(f"Overwriting file: {new_file_path}")  
                    shutil.move(file_path, new_file_path)  
                else:  
                    # 如果不存在，则重命名  
                    os.rename(file_path, new_file_path)  
                    print(f"Renamed file: {file_path} to {new_file_path}")  
  
# 调用函数，传入当前目录（'.'表示当前脚本所在目录）  
remove_spaces_in_filenames('.')