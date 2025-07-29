from pynput import keyboard
import subprocess
import os
import signal
import time

scrcpy_process = None
agent_process = None

def kill_process(proc):
    if proc and proc.poll() is None:
        try:
            if hasattr(os, "killpg"):
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            else:
                proc.terminate()
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            if hasattr(os, "killpg"):
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            else:
                proc.kill()
            proc.wait()

def start_processes():
    global scrcpy_process, agent_process
    if scrcpy_process is None and agent_process is None:
        scrcpy_process = subprocess.Popen([
            "scrcpy", "--fullscreen", "--window-borderless", "--crop=980:2160:100:115"
        ], preexec_fn=os.setsid, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        agent_process = subprocess.Popen([
            "/home/uliancam/cam/bin/python3", "auto_gambiarra.py"
        ], preexec_fn=os.setsid, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("scrcpy e agente iniciados.")

def stop_processes():
    global scrcpy_process, agent_process
    kill_process(scrcpy_process)
    kill_process(agent_process)
    scrcpy_process = None
    agent_process = None
    print("scrcpy e agente encerrados.")

def on_press(key):
    try:
        if key == keyboard.Key.up:
            start_processes()
        elif key == keyboard.Key.down:
            stop_processes()
        elif key.char == 'q':
            # Encerra tudo e para o listener
            stop_processes()
            return False
    except AttributeError:
        pass

def main():
    print("Programa iniciado. Use as setas para cima (↑) para ativar e para baixo (↓) para desativar. 'q' para sair.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
