import os
from kivy.app import App
import kivy.uix.image
import numpy as np
import treatments
import threading
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.logger import Logger
from android.permissions import Permission, request_permissions, check_permission
from android.storage import app_storage_path, primary_external_storage_path, secondary_external_storage_path
import time  

def log(msg):
  Logger.info(msg)

def check_permissions(perms):
  for perm in perms:
      if check_permission(perm) != True:
          return False
  return True

def Analyse():
  perms = [Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE]
    
  if  check_permissions(perms)!= True:
      request_permissions(perms)    # get android permissions     
      exit()  
  declenche =True    # app has to be restarted; permissions will work on 2nd start
  while (declenche):
        fileName = r"/storage/emulated/0/Documents/Khouloud/input.txt"
        if(os.path.exists(fileName)):    # création d'une boucle while qui s'executera tant que True == True
          fin = open(fileName, "rt")
          # the output file which stores result
          fout = open("/storage/emulated/0/Documents/Khouloud/input2.txt", "wt")
          # iteration for each line in the input file
          for line in fin:
              # replacing the string and write to output file
              fout.write(line.replace(',', '.'))
          #closing the input and output files
          fin.close()
          fout.close()
          file_out="/storage/emulated/0/Documents/Khouloud/input2.txt"
          input=open(file_out,"r")
          l=input.readlines()
          input.close()
          s="0 0 0 0"+"\n"
          l.insert(0,s)
          input=open(file_out,"w")
          l = "".join(l)
          input.write(l)
          input.close()
          with open(file_out,'r') as rf:
              lines = rf.readlines()
          line_number=0
          with open(file_out,'w') as write_file:
              for line in lines:
                  line_number =line_number+1
                  if line_number == len(lines):
                      pass
                  else:
                      write_file.write(line)
          m=np.loadtxt(file_out)
          with open('/storage/emulated/0/Documents/Khouloud/expected.txt', 'r') as f:
              expected = f.read() 
          reference="/storage/emulated/0/Documents/Khouloud/ref_"+expected+".inkml"
          ref = treatments.lecture_online(reference) 
          trace = m
          result1=treatments.analyse_penlift(ref,trace)
          result2=treatments.detect_overflow(trace,expected)
          result3=treatments.detect_reverse_direction(trace,expected)
          result4=treatments.detect_invalid_order(ref,trace,expected)
          penlifts =bytes(result1, encoding = "utf-8")
          overflows =bytes(result2, encoding = "utf-8")
          directions =bytes(result3, encoding = "utf-8")
          orders =bytes(result4, encoding = "utf-8")
          try:
              Logger.info('Got requested permissions')    
            
              fname1 = os.path.join( primary_external_storage_path(),'Documents/Khouloud/penlifts.txt')
              log('writing to: %s' %fname1)
            
              with open(fname1, 'wb') as f1:  # write testfile
                  f1.write(penlifts)

              fname2 = os.path.join( primary_external_storage_path(),'Documents/Khouloud/overflows.txt')
              log('writing to: %s' %fname2)
            
              with open(fname2, 'wb') as f2:        # write testfile
                  f2.write(overflows)

              fname3 = os.path.join( primary_external_storage_path(),'Documents/Khouloud/directions.txt')
              log('writing to: %s' %fname3)
            
              with open(fname3, 'wb') as f3:        
                f3.write(directions)
              
              fname4 = os.path.join( primary_external_storage_path(),'Documents/Khouloud/order.txt')
              log('writing to: %s' %fname4)
              
              with open(fname4, 'wb') as f4:        
                f4.write(orders) 

          except:
              log('could not write to external storage ... missing permissions ?')    
          #return "succes"
        else:
          time.sleep(2)
class MyApp(App):
    def build(self):
        return Label(text = 'wrote to: %s' %Analyse() )   # <---- calling testwrite() here  
MyApp().run()
