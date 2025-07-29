import time
import pyautogui
import subprocess
import numpy as np
import random

button_image_path = '/home/uliancam/Desktop/reconnect_button.png'
playbutton_image_path = '/home/uliancam/Desktop/play_button.png'
pyautogui.FAILSAFE = False

def is_scrcpy_window_open():
    try:
        result = subprocess.run(['xdotool', 'search', '--name', 'Redmi Note 8'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        window_ids = result.stdout.decode('utf-8').splitlines()
        
        if window_ids:
            print("Janela do scrcpy encontrada!")
            return True
        else:
            print("Janela do scrcpy não encontrada.")
            exit()
    except Exception as e:
        print(f"Erro ao verificar a janela: {e}")
        exit()
    
def capture_screen(region=None):
    screen_width, screen_height = 1600, 900
    region_width, region_height = 1000, 450
    
    region_x = (screen_width - region_width) // 2
    region_y = (screen_height - region_height) // 2
    
    screenshot = pyautogui.screenshot()
    
    return screenshot

def dummy_click_for_trigger_events():
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2

    # Gera deslocamentos aleatórios entre -200 e +200 pixels
    random_offset_x = random.randint(-200, 200)
    random_offset_y = random.randint(-200, 200)

    # Calcula as novas coordenadas
    random_x = center_x + random_offset_x
    random_y = center_y + random_offset_y

    # Realiza o clique nas coordenadas aleatórias
    pyautogui.click(random_x, random_y)
    print(f"Clique em ({random_x}, {random_y})")

    time.sleep(1.5)
    
def is_screen_majorly_black(screenshot):
    # Converte a captura de tela para um array NumPy
    image_np = np.array(screenshot)
    
    # Verifica a porcentagem de pixels próximos de preto (valores RGB baixos)
    black_pixels = np.sum(np.all(image_np[:, :, :3] < 50, axis=-1))  # Pixels com valores RGB menores que 50
    total_pixels = image_np.shape[0] * image_np.shape[1]
    
    # Define o limite de pixels pretos para considerar a tela majoritariamente preta
    black_percentage = black_pixels / total_pixels
    print('Tela Preta:', black_percentage > 0.8) 
    return black_percentage > 0.8  # Considera mais de 80% da tela preta

def click_on_reconnect_button(button_image_path):
    count = 0
    while True:
        try:
            # Tenta localizar o botão na tela com uma nova captura a cada iteração
            dummy_click_for_trigger_events()
            button_location = pyautogui.locateCenterOnScreen(
                button_image_path, confidence=0.7
            )

            # Se encontrou o botão, converte para inteiros nativos (caso necessário)
            if button_location is not None:
                button_x = int(button_location.x)
                button_y = int(button_location.y)
                
                print(f"Botão encontrado! Clicando no centro... ({button_x}, {button_y})")
                pyautogui.click(button_x, button_y)
                print("Esperando reconexão...")
                break
            else:
                if(count > 3):
                    break
                print("Botão não encontrado, tentando novamente...")
                count = count + 1
                time.sleep(2)  # Aguarde um pouco antes de tentar novamente

        except Exception as e:
            print(f"Erro ao localizar botão: {e}")
            time.sleep(1)

while True:
    if is_scrcpy_window_open():
        screenshot = capture_screen()
        
        if(is_screen_majorly_black(screenshot)):
            click_on_reconnect_button(button_image_path)

        time.sleep(1)
            
    else:
        print("Esperando a janela do scrcpy abrir...")

