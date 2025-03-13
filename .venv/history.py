import sys

import sqlite3

import json
import os
from rich.prompt import Prompt
from rich.table import Table
from login import LoginAI


class chat_history():



    def __init__(self):
        self.history_list = []
        self.my_console = None
        self.prompt_response_list = None
        self.login_obj = LoginAI()
        pass

    def dump_history(self):
        if Prompt.ask("do you want to save this chat into history", choices=['y', 'n'], default='n') == 'n':
            sys.exit()
        if self.login_obj.get_username() == None:
            self.my_console.print("\n[bold yellow underline2]user is not logged in\n")

        with sqlite3.connect(self.login_obj.db_path) as conn:
            cursor = conn.cursor()
            for p_n_r in self.prompt_response_list:
                cursor.execute(
                    """
                    INSERT INTO chat_history(username, prompt, response) VALUES(?, ?, ?)
                    """, (self.login_obj.get_username(), p_n_r[0], p_n_r[1])
                )
                print(f"{p_n_r[0], " \n\n" , p_n_r[1]} \n\n")
            print(self.prompt_response_list)
            conn.commit()

        self.my_console.print("\n[bold green underline2]history has been saved\n", p_n_r)
        pass

    def load_history(self):
        if self.login_obj.get_username() == None:
            self.my_console.print("\n[bold yellow underline2]user is not logged in\n", self.login_obj.get_current_user())
            sys.exit()
        else:
            with sqlite3.connect(self.login_obj.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT prompt, response FROM chat_history WHERE username = ?
                    """, (self.login_obj.get_username(),)
                )
            rows = cursor.fetchall()
            for row in rows:  # now every prompt and response is in the form of [[prompt1, response1], [prompt2, response2]]
                self.history_list.append(row)

    def show_history(self):
        if Prompt.ask("do you want to see your chat history", choices=['y', 'n'], default='n') != 'n':
            if self.login_obj.get_username() == None:
                self.my_console.print("\n[bold yellow underline2]user is not logged in\n")
                sys.exit()
            else:
                table = Table(title="chat history", show_lines=True, header_style="bold blue")
                table.add_column("prompt", no_wrap=False, header_style="bold blue")
                table.add_column("response", no_wrap=False, justify='center', width=100, header_style='red',
                                 style='green')

                for i in range(len(self.history_list)):
                    table.add_row(f"{self.history_list[i][0]}"
                                  , f"{self.history_list[i][1]}")
                self.my_console.print(table, justify='center')

    pass
