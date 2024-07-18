import pyautogui
import time
import pandas as pd
import re
import webbrowser


'''
Restrictions:

*You need to set to spanish (Latin America) your OS languague layout if you want to send messages in that language.
*In this implementation you cannot write words with tildes (And others special characters) so, the message must be wrote without tildes.
*While the algorithm is running you cannot interact with your pc, due to the algorithm types in the current page that you are.

'''


message = '''*AUN ESTAS A TIEMPO DE FINALIZAR TU PROCESO DE INSCRIPCION A LA CARRERA ATLETICA "INDESA ESTA DE FIESTA"*  
Buenas tardes! Hemos visto que te registraste en la carrera pero aun no realizaste el pago de inscripcion. Todavia estas a tiempo para que el proceso se complete. Sigue el link de inscripcion para continuar. Animate a correr! *(Hacer caso omiso si ya hiciste el pago)*

'''
'''Url is optional'''
url = 'https://indesa.gov.co/carreras-atleticas/'


'''To set the array of numbers from an excel file'''
file_path = '/home/saiky/Downloads/p2.xlsx'
sheet_name = 'Hoja 1'  



df = pd.read_excel(file_path, sheet_name=sheet_name)
column_name ='Celular'  
column_data = df[column_name].tolist()
no_valid_numbers = []
valid_numbers = []

def format_phone_number(number):
    cleaned_p = re.sub(r'\D', '', str(number))
    
  
    if len(cleaned_p) > 10:
        if cleaned_p[0] == '5' and cleaned_p[1] == '7':
            cleaned_p = f"{cleaned_p[2:]}"
        
    if len(cleaned_p) == 10:        
        if cleaned_p[0] == '3' and cleaned_p not in valid_numbers:
            valid_numbers.append(cleaned_p)
        else:
            no_valid_numbers.append(cleaned_p)    

for phone in column_data:
    format_phone_number(phone)



'''To type urls correctly'''
def type_urls(prefix, url:str):
  
    pyautogui.typewrite(prefix, interval=0.1)
    pyautogui.press('space')
    
    parts = url.split('/')
    
    pyautogui.typewrite(parts[0])
 
    for part in parts[1:]:
        pyautogui.hotkey('shift', '7')  
        pyautogui.typewrite(part)
        
  
''' To type messages efficiently'''          
def write_messages(ms, num_parts):

    length = len(ms)
    part_size = length // num_parts
    
    parts = [
        ms[i*part_size : (i+1)*part_size] for i in range(num_parts - 1)
    ]
    parts.append(ms[(num_parts - 1)*part_size:]) 
    for part in parts:
        pyautogui.typewrite(part, interval=0.04)


def send_whatsapp_message(phone, ms, url, delay=7):
    webbrowser.open(f'https://web.whatsapp.com/send?phone=+57{phone}')
    time.sleep(delay)
    write_messages(ms, 10)
    type_urls('Link de inscripcion: ',url)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'w') 


def massive_sending(list_of_phones:list, ms:str, url=None, speed=7):
    count = 0
    flag = 0
    queue_of_phones = list_of_phones.copy()
    list_of_sent_phones = []
    while len(queue_of_phones) >= 1:
            count +=1
            flag += 1
            phone = queue_of_phones.pop()
            if flag == 400:
                flag = 0
                x = input('Do you want to continue sending messages? y/n: ')
                if x == 'y':
                    print(f'Sending {len(queue_of_phones)} more \n')
                    continue
                else:
                    break

            if flag < 400 and phone not in list_of_sent_phones:
                send_whatsapp_message(phone, ms, url, speed)
                list_of_sent_phones.append(phone)
                print(f'Message was sent successfully to {phone}. {count}/{len(list_of_phones)} *** {len(queue_of_phones)} left.')

            elif phone in list_of_sent_phones:
                print(f'{phone} was declined, message already sent')    
    print('All messages was sent successfully \n')            

test = ['3017388273']      


massive_sending(test, message, url)        

