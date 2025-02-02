import atexit
import ctypes
import ollama
import os
import psutil
import signal
import subprocess
import sys
import time
from rich import pretty, traceback, console


class Artificial():

    def __init__(self):
        self.ollama_server = None
        self.client = None
        self.messages_ollama = []

        self.temp = 0.5
        self.top_p = 0.5
        self.max_tockens = 200
        self.alive = '0'

        self._cleaned_up_flag = False

        self.start_time = None

        self.tocken_generated = 0

        self.ollama_server_pid_ram = 0

        self.my_console = console.Console()
        pretty.install()
        traceback.install()

        self.connection()
        pass

    def cpu_utilization(self, utilization):
        # get system information <cores/thread(logical cores)>
        cores = psutil.cpu_count(logical=False)  # this is for core (logical+True=threads)
        threads = psutil.cpu_count(logical=True)

        ollama_server_pid = psutil.Process(self.ollama_server.pid)
        if utilization:
            ollama_server_pid.nice(psutil.REALTIME_PRIORITY_CLASS)  # set as realtime maxed high priority process

            ollama_server_pid.cpu_affinity(
                list(range(threads)))  # bind with no of cores/threads   max thread are fastest
            # server_process.ionice(ioclass=psutil.IOPRIO_CLASS_RT)  # realtime max i/o priority

            print(f"current process status is :- {ollama_server_pid.nice()}")
            self.my_console.print(f"current process "
                                  f"[yellow][bold o][u]STATUS[/bold o][/u][/yellow] is :- "
                                  f"[green blink]{ollama_server_pid.nice()}[/green blink]", ":warning:")
        pass

    def get_tocken(self, time_tacken):
        # we can use no of words / time taken  = tocken generated
        if time_tacken == 0:
            return 0
        else:
            return self.tocken_generated / time_tacken
        # average of tockens
        pass

    def connection(self):
        try:
            # this for not printing the log of webserver of ollama server
            self.ollama_server = subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL,
                                                  stderr=subprocess.DEVNULL)

            # print the log of webserver
            # self.ollama_server = subprocess.Popen(["ollama", "serve"])

            self.cpu_utilization(True)

            # time.sleep(2)

            # setting client

            self.client = ollama.Client()

        except Exception as e:
            print(e)
        pass

    def set_system_txt(self, content):
        self.messages_ollama.append({'role': 'system', 'content': content})

    def set_user_message(self, query, autoRun=False):
        self.messages_ollama.append({'role': 'user', 'content': query})

        if autoRun:
            self.run_connect()
            #         run the connect get output from the ollama deep seek

    def options_change(self, temperature: float, top_p: float, max_tocken: int, alive: str):
        self.temp = temperature
        self.top_p = top_p
        self.max_tockens = max_tocken
        self.alive = alive

    def run_connect(self):
        opt = {
            "temperature": self.temp,
            "keep_alive": self.alive,
            "top_p": self.top_p,
            "num_predict": self.max_tockens
        }
        self.start_time = time.perf_counter()
        try:
            response = self.client.chat(model='deepseek-r1:7b', messages=self.messages_ollama, options=opt, stream=True)
            for chunk in response:
                print(chunk['message']['content'], end='', flush=True)
                self.tocken_generated += 1

            self.ollama_server_pid_ram = psutil.Process(self.ollama_server.pid).memory_info().rss
            parent = psutil.Process(self.ollama_server.pid)
            for child in parent.children(recursive=True):
                if child.is_running():
                    self.ollama_server_pid_ram += child.memory_info().rss

        except (KeyboardInterrupt, TypeError, psutil.NoSuchProcess, psutil.AccessDenied) as e:
            self.my_console.print(f"[bold red]error[/bold red] while streaming {e}")

    pass

    def log_out(self):
        end_time = time.perf_counter()
        total_time_tacken = end_time - self.start_time

        python_script_pid_ram = psutil.Process(os.getpid()).memory_info().rss

        total_ram = self.ollama_server_pid_ram + python_script_pid_ram

        self.my_console.print(f"\ntime taken to generate response:- {total_time_tacken:.4f}\n"
                              f"ram consumed by this is :- {total_ram / (1024 ** 3):.2f} GB\n"
                              f"tockens per second we got {self.get_tocken(total_time_tacken):.2f}", justify='center')

        self.ollama_server.terminate()
        self.ollama_server.wait()

        if os.name == "nt":  # windows
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.name() == "ollama_llama_server.exe":
                    try:
                        result = subprocess.run(["taskkill", "/F", "/IM", "ollama_llama_server.exe"], check=True,
                                                capture_output=True)

                time.sleep(5)
                print(result.stdout, result.stderr)
            except subprocess.CalledProcessError as e:
                if e.returncode == 128:
                    print("server is already killed")
                print(e)

        else:
            os.system("pkill -f ollama")

        pass

    def cleanUp(self):
        if self._cleaned_up_flag:
            pass
        else:
            self.log_out()
            self._cleaned_up_flag = True
        pass

    def handel_intrupt(self, signum, frame):
        print(f"\n🛑 Received signal {signum}. Exiting gracefully...")
        self.cleanUp()
        exit()
        pass

    def welcome(self):
        # here i have to tell that this is chat bot plz enter your desired settings and then after setting up
        """
        like :-
        "temperature": self.temp,
            "keep_alive": self.alive,
            "top_p": self.top_p,
            "num_predict": self.max_tockens
        :return:
        """
        # you can chat with this bot
        pad = Padding("[blink red] welcome to smart AI", (1, 1, 1, 10))
        self.my_console.rule("[blink red] welcome to smart AI",
                             style="green", align='center')

        self.my_console.rule("please set up your AI assistance personality", style="bold ")

        choice_get = [
            ["random", "strict", "entermediate"],
            ["short", "long", "extreme"],
            ["yes", "no"]
        ]

        choice_set = [
            [1, 0, 0.5],
            [200, 1500, 2000],
            [True, False]
        ]

        temprature = Prompt.ask("Enter the desired output type", choices=choice_get[0], default="strict")

        output_length = Prompt.ask("Enter the preferred length of output", choices=choice_get[1], default="short")

        history = Prompt.ask("would you like to maintain history", choices=choice_get[2], default="no")

        self.temp = choice_set[0][choice_get[0].index(temprature)]
        self.max_tockens = choice_set[1][choice_get[1].index(output_length)]
        # no feature related history
        # now set it to options
        pass

    def handle_running(self):
        # maintaining chatting loop till user wants to exit
        prompt = Prompt.ask("enter your query :- {[bold yellow]for exit type exit(0)[/bold yellow]}", default="exit(0)",
                            show_default=False)
        panel_prompt = Panel.fit(f"[bold yellow]{prompt}", style='red')
        print(panel_prompt, ":backhand_index_pointing_down:")
        if prompt == "exit(0)":
            self.cleanUp()
        else:
            while (True):
                self.set_user_message(prompt, True)
                self.response_information()

                self.handle_running()
        pass


def main():
    ai = Artificial()

    try:
        signal.signal(signal.SIGINT, ai.handel_intrupt)
        signal.signal(signal.SIGTERM, ai.handel_intrupt)
    except KeyboardInterrupt as e:
        print(e)
    pass

    atexit.register(ai.cleanUp)

    try:
        user_query = """
        want to buy pc for me can you suggest me which requirement is suitable for me
        dont use basic term i know i am computer science student  
        suggest me terms that i should keep in mind 
        i have to do heavy AI ML programming task like running/researching about dee[p seek model locally and   
        android studio and using my pc to web scrap even use heavy application like unity and visual studio
        """
        ai.set_system_txt("you are technical support assistance")
        ai.set_user_message(user_query)
        ai.options_change(0.5, 0.8, 100, '0')

        prompt = ("""
        
        """)

        ai.set_user_message(prompt, True)
    except Exception as e:
        print(e)


def check_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("checking up priority :- ")
        time.sleep(3)
        ctypes.windll.shell32.ShellExecuteW(
            None,  # Parent window handle
            "runas",  # Verb (e.g., "runas" for admin)
            sys.executable,  # Python executable
            " ".join(sys.argv),  # Script arguments
            None,  # Working directory
            1  # Show window
        )
        sys.exit()
        pass
    pass


if __name__ == '__main__':
    # check_admin()
    main()
