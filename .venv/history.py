import json
import os
from rich.prompt import Prompt
from rich.table import Table


class histoty_ai:

    def __init__(self):
        self.history_dict = {}
        self.my_console = None
        self.prompt_response_list = None
        pass

    def load_history(self):
        if not os.path.exists('history.json'):
            print("\n[bold yellow underline2]history file is not exist\n")
        else:
            with open('history.json', 'r') as r_file:
                self.history_dict = dict(json.load(r_file))

    def show_history(self):
        # now we have to display that do you want to see history if yes show it
        if (Prompt.ask("do you want to see your chat history", choices=['y', 'n'], default='n')) != 'n':
            #     here we will show table
            table = Table(title="chat history", show_lines=True, header_style="bold blue")
            table.add_column("prompt", no_wrap=False, header_style="bold blue")
            table.add_column("response", no_wrap=False, justify='center', width=100, header_style='red', style='green')

            for i in range(len((list(self.history_dict.values())))):
                table.add_row(f"{list(self.history_dict.values())[i][0]}"
                              , f"{list(self.history_dict.values())[i][1]}")

            self.my_console.print(table, justify='center')
            pass
        pass

    def dump_history(self):
        """
        to create file if not exist enter the prompt that user wrote and dump in json file
        :return:
        """
        if Prompt.ask("do you want to save this chat into history", choices=['y', 'n'], default='n') == 'y':
            # add to history
            if os.path.exists('history.json'):
                last_key_p_r_dict = int(list(self.history_dict.keys())[-1])
                last_key_p_r_dict += 1  # atleast while updating history we add up on the writen one

                for i in range(len(self.prompt_response_list)):
                    # this will add [[prompt1,response1], [[prompt2, response2]] into hist_dict after its element
                    self.history_dict.update({last_key_p_r_dict + i: self.prompt_response_list[i]})

                with open('history.json', 'w') as file:
                    json.dump(self.history_dict, file, indent=4)
            else:
                last_key_p_r_dict = 1

                for i in range(len(self.prompt_response_list)):
                    self.history_dict.update({last_key_p_r_dict + i: self.prompt_response_list[i]})

                with open('history.json', 'w') as file:
                    json.dump(self.history_dict, file, indent=4)
            print("history has been saved")
            pass
