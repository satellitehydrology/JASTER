import sys, os, requests
from ftplib import FTP
import tkinter as tk
from s00_get_system_parameters import window_width, window_height, TEXT
   
data_dir, Username, Password = sys.argv[1], sys.argv[2], sys.argv[3]

Series, Pass, Start, End = int(sys.argv[4]),int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])

def destroy_root():
        root.after(1, root.destroy())
        
def simulate_download(): 
    for cycle in range(Start, End+1):        
        try:
            ftp=FTP('ftp-access.aviso.altimetry.fr')
            ftp.login(user=Username,passwd=Password)  
            if Series == 2:
                ftp.cwd('geophysical-data-record/jason-{}/gdr_d/cycle_{:03d}'.format(Series,cycle))   
                fnbase ='JA{}_GPN_2PdP{:03d}_{:03d}_'.format(Series, cycle, Pass)
            if Series == 3:
                ftp.cwd('geophysical-data-record/jason-{}/gdr_f/cycle_{:03d}'.format(Series,cycle)) 
                fnbase ='JA{}_GPN_2PfP{:03d}_{:03d}_'.format(Series, cycle, Pass)

            save_path = data_dir+'/j{}_{:03d}/cycle_{:03d}/'.format(Series, Pass, cycle)
            flag = 1
            try:
                os.makedirs(os.path.dirname(save_path))
            except:
                result_label.config(text = 'Cycle # {} of Jason-{} series already exists'.format(cycle, Series))
                root.update()
                root.after(10)
                continue
            os.chdir(save_path)
            files=[filename for filename in ftp.nlst() if fnbase in filename]
            for filename in files:
                local_filename=os.path.join(os.getcwd(), filename)
                with open(local_filename, 'wb') as f:
                    ftp.retrbinary('RETR %s' % filename, f.write) 
                result_label.config(text = 'Cycle # {} of Jason-{} series successfully downloaded'.format(cycle, Series))
                root.update()
                root.after(10)
        except: 
            sys.exit(1) 
            
    result_label.config(text = 'Jason-{} data successfully downloaded'.format(Series))
    close_button.place(relx=0.5, rely=0.75, anchor='center')
    root.after(1000, destroy_root) 


root = tk.Tk()
root.geometry('{}x{}'.format(window_width, window_height))
root.configure(background = 'bisque')
root.title('AVISO Download of Jason-{} data'.format(Series))

result_label = tk.Label(root, text='Download of Jason-{} data in progress...'.format(Series), font=('Arial', TEXT),  fg='black', bg='bisque')
result_label.place(relx=0.5, rely=0.35, anchor='center')
root.after(100, simulate_download) 

close_button = tk.Button(root, text="Close", font=('Arial', TEXT), command=destroy_root)

root.mainloop()
sys.exit(0)