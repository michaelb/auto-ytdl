import os


def embed_mp3(temp_dir_path, filename):
    # convert webp thumbnail to jpg
    if os.path.isfile(temp_dir_path + "/"+filename[:-4]+".webp"):
        os.system("ffmpeg -i \"" + temp_dir_path + "/" +
                  filename[:-4] + ".webp\"" + " \"" + temp_dir_path + "/" + filename[:-4] + ".jpg\"  -v 0 -y")

    if os.path.isfile(temp_dir_path + "/"+filename[:-4]+".jpg"):
        # create temp file as ffmpeg cannot add thmbnail in-place
        os.system("mv \"" + temp_dir_path + "/"+filename +
                  "\" \"" + temp_dir_path + "/"+filename[:-4]+".temp.mp3\"")
        os.system("ffmpeg -i \"" + temp_dir_path + "/" + filename[:-4]+".temp.mp3" + "\" -i \"" + temp_dir_path + "/" +
                  filename[:-4]+".jpg\"" + " -v 0 -y -map 0:0 -map 1:0 -codec copy -id3v2_version 3 -metadata:s:v title=\"Album cover\" -metadata:s:v comment=\"Cover (front)\" \"" + temp_dir_path + "/" + filename + "\"")

        os.system("rm -f \"" + temp_dir_path +
                  "/"+filename[:-4]+".temp.mp3\"")


def embed_opus(temp_dir_path, filename):
    # convert webp to jpg
    if os.path.isfile(temp_dir_path + "/"+filename[:-5]+".webp"):
        os.system("ffmpeg -i \"" + temp_dir_path + "/" +
                  filename[:-5] + ".webp\"" + " \"" + temp_dir_path + "/" + filename[:-5] + ".jpg\"  -v 0 -y")
    # if there is a jpg file, embed it
    if os.path.isfile(temp_dir_path + "/"+filename[:-5]+".jpg"):
        # problem if ' in filename so temp move
        os.system("mv \""+temp_dir_path + "/" +
                  filename[:-5] + ".jpg\""+" "+temp_dir_path + "/" + "in.jpg")
        os.system("mv \""+temp_dir_path + "/" +
                  filename + "\" " + temp_dir_path + "/" + "in.opus")
        os.system("kid3-cli -c 'set picture:\"in.jpg\"" +
                  " \"desc\"' \"" + temp_dir_path + "/" + "in.opus\"")
        os.system("mv  "+temp_dir_path + "/" + "in.opus \""+temp_dir_path +
                  "/" + filename + "\"")
