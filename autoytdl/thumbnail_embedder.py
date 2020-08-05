import os
from pathlib import Path


def embed_mp3(temp_dir_path, filename):
    # convert webp thumbnail to jpg
    if Path(temp_dir_path + "/"+filename[:-4]+".webp").exists():
        os.system("ffmpeg -i \"" + temp_dir_path + "/" +
                  filename[:-4] + ".webp\"" + " \"" + temp_dir_path + "/" + filename[:-4] + ".jpg\"  -v 0 -y")

    if Path(temp_dir_path + "/"+filename[:-4]+".jpg").exists():
        # create temp file as ffmpeg cannot add thmbnail in-place
        Path(temp_dir_path + "/"+filename).replace(Path(temp_dir_path +
                                                        "/"+filename[:-4]+".temp.mp3"))
        os.system("ffmpeg -i \"" + temp_dir_path + "/" + filename[:-4]+".temp.mp3" + "\" -i \"" + temp_dir_path + "/" +
                  filename[:-4]+".jpg\"" + " -v 0 -y -map 0:0 -map 1:0 -codec copy -id3v2_version 3 -metadata:s:v title=\"Album cover\" -metadata:s:v comment=\"Cover (front)\" \"" + temp_dir_path + "/" + filename + "\"")

        if Path(temp_dir_path + "/"+filename[:-4]+".temp.mp3").exists():
            Path(temp_dir_path + "/"+filename[:-4]+".temp.mp3").unlink()


def embed_opus(temp_dir_path, filename):
    # convert webp to jpg
    if Path(temp_dir_path + "/"+filename[:-5]+".webp").exists():
        os.system("ffmpeg -i \"" + temp_dir_path + "/" +
                  filename[:-5] + ".webp\"" + " \"" + temp_dir_path + "/" + filename[:-5] + ".jpg\"  -v 0 -y")
    # if there is a jpg file, embed it
    if Path(temp_dir_path + "/"+filename[:-5]+".jpg").exists():
        # problem if ' in filename so temp move
        Path(temp_dir_path + "/" +
             filename[:-5] + ".jpg").replace(Path(temp_dir_path + "/" + "in.jpg"))
        Path(temp_dir_path + "/" +
             filename).replace(Path(temp_dir_path + "/" + "in.opus"))
        os.system("kid3-cli -c 'set picture:\"in.jpg\"" +
                  " \"desc\"' \"" + temp_dir_path + "/" + "in.opus\"")
        Path(temp_dir_path + "/" +
             "in.opus").replace(Path(temp_dir_path + "/" + filename))
