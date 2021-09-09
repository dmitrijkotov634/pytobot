from typing import Callable, Any, Dict

import requests
import argparse
import builtins
import runpy
import sys
import os
import re

parser = argparse.ArgumentParser(description="Run script as Telegram bot")

parser.add_argument("file")
parser.add_argument("-t", "--token", help="set bot token")
parser.add_argument("-a", "--ansi", action="store_true", help="replace all ANSI escape codes")
parser.add_argument("-", "--args", action="store", nargs=argparse.REMAINDER, help="arguments passed to the script")

class BotError(Exception):
    def __init__(self, error_code, description):
        self.error_code = error_code
        self.description = description

        Exception.__init__(self, "[%s] %s" % (error_code, description))
        
class Bot:
    def __init__(self, token: str, replace_ansi: bool = False):
        self.base = "https://api.telegram.org/bot" + token + "/"
        self.replace_ansi = replace_ansi
        self.last_chat_id = None

        updates = self._get_updates(-1, wait=False)
        self.last_update_id = updates[-1]["update_id"] if updates else -1
        
    def _call(self, name: str, **args) -> Dict[str, Any]:
        response = requests.get(self.base + name, data=args).json()
        if response["ok"]:
            return response["result"]
        else:
            raise BotError(response["error_code"], response["description"])
            
    def _get_updates(self, offset: int, wait: bool = True) -> Dict[str, Any]:
        response = None
        while not response and wait:
            response = self._call("getUpdates", offset=offset)
        return response
    
    @property
    def input(self) -> Callable:
        def input_(promt: Any = None) -> str:
            if promt:
                self.print(promt)
            
            update = {}
            while not ("message" in update and
                "text" in update["message"]):
                update = self._get_updates(self.last_update_id + 1)[-1]
                self.last_update_id = update["update_id"]
            
            self.last_chat_id = update["message"]["chat"]["id"]
            return update["message"]["text"]
        return input_
    
    @property
    def print(self) -> Callable:
        def print_(*values: Any, sep: str = " ", end: str = "") -> None:
            if not values:
                return

            message = sep.join(map(str, values)) + end
            
            if not message:
                return
                
            if self.replace_ansi:
                message = re.sub(r"\x1B[@-_][0-?]*[ -/]*[@-~]", "", message)
                
            if not self.last_chat_id:
                update = self._get_updates(self.last_update_id + 1)[-1]
                self.last_update_id = update["update_id"]
                
                self.last_chat_id = update["message"]["chat"]["id"]
            
            self._call("sendMessage", text=message, chat_id=self.last_chat_id)
        return print_
    
def main() -> None:
    args = parser.parse_args()
    
    if not args.token:
        if "BOT_TOKEN" in os.environ:
            args.token = os.environ["BOT_TOKEN"]
        else:
            args.token = input("Bot token: ")
        
    bot = Bot(args.token, args.ansi)

    builtins.print = bot.print
    builtins.input = bot.input
    
    sys.path.append(os.getcwd())
    sys.argv = [args.file]
    if args.args:
        sys.argv.extend(args.args)
    
    runpy.run_path(args.file, run_name=args.file)