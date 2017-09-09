#!/usr/bin/env python
#coding:utf-8

import os
import sys
from datetime import datetime
import time
import shutil
import subprocess
import threading
import multiprocessing

try:
   import classify_nsfw
except:
    print("In order to use the classifier, you have to run on the dokcer")

__author__ = "kihaya"


def calc_all_scores(dir):
    """
       List up all mvs
       for mv in mvs:
          Create tmp_dir named mv
          Run gen_ss in tmp_dir
          calculate all scores in tmp_dir 
          delete tmp_dir
    """
    fp = open("./scores.csv","w")
    mvs = os.listdir(dir)

    myscores = []

    for mv in mvs:
      if mv != ".DS_Store":
        #os.mkdir(dir + "/" + mv)
        print("Creating dir " + dir + "/" + mv)
        try:
           os.mkdir(dir + "/tmp_" + mv)
        except:
           pass

        print("Generating ss in " + dir + "/" + mv)
	try:
          gen_ss2(dir + "/" + mv, dir + "/tmp_" + mv)

          print("Calculate scores in " + dir + "/" + mv)

          sss = os.listdir(dir + "/tmp_" + mv)

          for ss in sss:
             myscores.append(calc_nsfw_score_file(dir + "/tmp_" + mv + "/" + ss))

          print("delete tmp dis " + dir + "/" + mv)
          shutil.rmtree(dir + "/tmp_" + mv + "/")

          o = open(dir + "/" + mv + "_scores.csv","w")
          for i in myscores:
             o.write(str(i) + "\n")
          o.close()

          # output scores to the file
          # format is like this
          # username,liveid,date,avg_nsfw_score
          nsfw_average = sum(myscores) / len(myscores)
          username = dir.split("/")[1]
          line =  username + "," + mv + "," + str(nsfw_average)
          print(line)
          fp.write(line + "\n")

          print(myscores)

          myscores = []
        except:
	  print("error when handling movie file")
    fp.close()
	   

def clone_dir(target_dir,where_to_clone):
    """
      Clone the target directory structure 
      in the appointed path.
      Including movie file, create the directory using
      the name of (movie) file.
    """
    print target_dir.split("/")
    #
    print "Creating dir " + where_to_clone +  "/" +  target_dir.split("/")[-1]

    os.mkdir(where_to_clone + "/" +  target_dir.split("/")[-1])

    #  for all first dir
    #print os.listdir(target_dir)
    for i in os.listdir(target_dir):
      # os.mkdir(where_to_clone + target_dir.split("/")[-2] + "/" + i)
         
       if os.path.isdir(target_dir + "/" + i):
          print "creating dir " + i
          os.mkdir(where_to_clone + "/" + target_dir.split("/")[-1] + "/" + i)
          for j in os.listdir(target_dir + "/" + i):
              if os.path.isfile(target_dir + "/" + i + "/" + j):
                 print "creating dir " + j
                 os.mkdir(where_to_clone + "/" + target_dir.split("/")[-1] + "/" + i + "/" + j)

def gen_all_ss_in_prj(prj_dir,save_dir):
    dirs_in_prj = os.listdir(prj_dir)
    for d in dirs_in_prj:
        gen_all_ss_in_dir(prj_dir + "/" + d, save_dir)

    print "finished..."

def gen_all_ss_in_dir(target_dir,save_dir):
    files_in_dir = os.listdir(target_dir)
    for f in files_in_dir:
       # gene all ss to the directory
       gen_ss(target_dir + "/" + f, save_dir + "/" + target_dir.split("/")[-1] + "/" + f )
    
def gen_ss(target_dir,where_to_save):
    """
      Genrate the screeshots of the movie file
      beyond frames using ffmpeg.
      e.g,
        gen_ss("/Users/Kihaya/flower.mp4","/Users/Kihaya/myframes/")
    """
    output_dir = where_to_save + "/" + "%04d.jpg"
    cmd = "ffmpeg -i %s -filter:v fps=fps=1:round=down %s" % (target_dir,output_dir)
    subprocess.call(cmd,shell=True)

def gen_ss2(target_dir,where_to_save):
    """
      Genrate the screeshots of the movie file
      beyond frames using ffmpeg.
      e.g,
        gen_ss("/Users/Kihaya/flower.mp4","/Users/Kihaya/myframes/")
    """
    output_dir = where_to_save + "/" + "%04d.jpg"
    cmd = "ffmpeg -i %s -filter:v fps=fps=1/90:round=down %s" % (target_dir,output_dir)
    subprocess.call(cmd,shell=True)

def calc_nsfw_score_file(target):
    """
      Calculate all nsfw score of the image files
      in the target_dir.
      where to save the result
    """
    myargv =  ['classify_nsfw.py', '--model_def', 'nsfw_model/deploy.prototxt', '--pretrained_model', 'nsfw_model/resnet_50_1by2_nsfw.caffemodel', target]
    sys.argv = myargv
    res = classify_nsfw.main(sys.argv)
    #print res
    #assert type(res) == "str", "res is not str"
    return res

def getFileTimeStamp(target_file):
   ctime = os.path.getctime(target_file)
   print datetime(*time.localtime(os.path.getctime(target_file))[:6])

if __name__ == "__main__":
   
   #calc_all_scores("Movies/something")
   #calc_all_scores("Movies/something")

   #result_table = open("./scores.csv","w")

   users = os.listdir("test_movies")
   done = []
   for user in users:
      print("Currently processing: " + user)

      calc_all_scores("test_movies/" + user)
      done.append(user)

      print(str(len(done)) + " / " + str(len(users)) + " completed.")
      print((len(done) / len(users)) * 100)

   print(len(users))
  
