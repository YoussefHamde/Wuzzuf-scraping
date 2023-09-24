import requests
from bs4 import BeautifulSoup 
import pandas as pd
from tkinter import *
from tkinter import scrolledtext, messagebox
import sys

def Enter(event):
    search_button.invoke()

def stop_processing():
    global stop_flag
    stop_flag = True

def search():
    global stop_flag
    keyword = entry.get()
    search_keyword = keyword.replace(" ", "+")
    
    try:
        df = pd.DataFrame({'Job title':[], 'Company':[], 'Location':[], 'Skills':[]})
        row = 0
        page_num = 0

        while True:
            if stop_flag:
                messagebox.showwarning("Stop", "Processing stopped by user.")
                stop_flag = False
                break
            
            print(f'https://wuzzuf.net/search/jobs/?a=navbl&q={search_keyword}&start={page_num}')
            url = requests.get(f'https://wuzzuf.net/search/jobs/?a=navbl&q={search_keyword}&start={page_num}')

            src = url.content
            soup = BeautifulSoup(src, 'lxml')
            page_limit = int(soup.find('strong').text.replace(',' , ''))
            
            if page_num > page_limit // 15:
                break
            
            job_titles = soup.find_all('h2',{'class':'css-m604qf'})
            companies = soup.find_all('a',{'class':'css-17s97q8'})
            locations = soup.find_all('span',{'class':'css-5wys0k'})
            skills = soup.find_all('div',{'class':'css-y4udm8'})

            job_details = []

            for job in range(len(job_titles)):
                job_title = job_titles[job].text.strip()
                company = companies[job].text.strip().replace(' -','')
                location = locations[job].text.strip()
                skill  = skills[job].text.strip()
                
                job_details.append([job_title, company, location, skill])

                df.loc[row + 2] = job_details[0]
                df.reset_index(drop=True, inplace=True)
                row += 1
                root.update()
                job_details = []
            
            row += 15
            page_num += 1

        df.to_excel(f'D:/wuzzuf/wuzzuf_{search_keyword}.xlsx' , index=False)
        messagebox.showinfo("Done", "Done", parent=root)
        
    except requests.exceptions.RequestException:
            messagebox.showerror("Error", "No internet connection.")

stop_flag = False

class RedirectedText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(END, string)
        self.text_widget.see(END)

root = Tk()
root.title('WSC')
root.geometry('680x460')
root.resizable(False , False)
entry = Entry(root)
entry.place(x=190, y=10, width=200)
search_button = Button(root, text='Search', command=search)
search_button.place(x=400, y=5, width=80)
stop_button = Button(root, text='Stop', command=stop_processing)
stop_button.place(x=490, y=5, width=80)

output_text = scrolledtext.ScrolledText(root)
output_text.place(x=10, y=40)

entry.bind('<Return>', Enter)

sys.stdout = RedirectedText(output_text)

root.mainloop()