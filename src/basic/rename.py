import os 
  
#rename file name
def main(): 
    i = 1
    path = "/Users/sergiorodrigo/Documents/images/"
    for filename in os.listdir(path): 
        dst = path + "g" + str(i) + ".png"
        src = path + filename 
        os.rename(src, dst) 
        i += 1
  
if __name__ == '__main__': 
    main() 