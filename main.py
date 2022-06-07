#!/usr/bin/env python

"""
MIT License

Copyright (c) 2020-2021 Linus Bartsch

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from discord_interactions.ext import (
    CommandContext, AfterCommandContext,
    ComponentContext, AfterComponentContext
)
from discord_interactions.ext.flask import Interactions
from discord_interactions import (
    Member,
    Button,
    ButtonStyle,
    ActionRow,
    MessageResponse
)
from flask import Flask
import os
import random
from commands import (
    Ping, Echo, RPS, RPSSymbol, Guess,
    Delay, Hug, UserInfo, Generate, Sha1, HelloComponents
)
import time
import hashlib

app = Flask(__name__)
interactions = Interactions(app, os.getenv("CLIENT_PUBLIC_KEY"), os.getenv("CLIENT_ID"))


@interactions.command(Ping.to_application_command())
def ping():
    return "pong"


@interactions.command(Echo.to_application_command())
def echo(_, message: str):
    return message, False


@interactions.command(RPS.to_application_command())
def rps(_, symbol: RPSSymbol):
    choice = random.choice(list(RPSSymbol))

    if symbol == choice:
        msg = "It's a draw!"
    elif symbol == RPSSymbol.ROCK:
        if choice == RPSSymbol.SCISSORS:
            msg = "You crush me and win!"
        else:
            msg = "You get covered and lose!"
    elif symbol == RPSSymbol.PAPER:
        if choice == RPSSymbol.ROCK:
            msg = "You cover me and win!"
        else:
            msg = "You get cut and lose!"
    else:
        if choice == RPSSymbol.ROCK:
            msg = "You get crushed and lose!"
        else:
            msg = "You cut me and win!"

    return f"I took {choice.value}. {msg}"


@interactions.command(Guess.to_application_command())
def guess(_: CommandContext, guessed_num, min_num=None, max_num=None):
    min_val = min_num or 0  # defaults to 0
    max_val = max_num or 10  # defaults to 10

    my_number = random.randint(min_val, max_val)

    if my_number == guessed_num:
        msg = "You are correct! :tada:"
    else:
        msg = "You guessed it wrong. :confused:"

    return f"My number was {my_number}. {msg}"


@interactions.command(Delay.to_application_command())
def delay():
    return None  # deferred response


@delay.after_command
def after_delay(ctx: AfterCommandContext):
    delay_time = ctx.interaction.data.options[0].value
    time.sleep(delay_time)
    ctx.edit_original(f"{delay_time} seconds have passed")


@interactions.command(Hug.to_application_command())
def hug(ctx: CommandContext, cutie: int):
    return f"<@{ctx.interaction.author.id}> *hugs* <@{cutie}>"


@interactions.command(UserInfo.to_application_command())
def user_info(ctx: CommandContext, user_id: int, raw: bool):
    if user_id:
        user = ctx.interaction.get_user(user_id)
    else:
        user = ctx.interaction.author

    if raw:
        return f"```json\n{user.to_dict()}\n```", True  # ephemeral

    info = ""

    if isinstance(user, Member):
        role_info = " ".join(f"<@&{r}>" for r in user.roles)
        info += f"**Member**\nnick: {user.nick}\nroles: {role_info}\n" \
                f"joined at: {user.joined_at.isoformat()}\n" \
                f"premium since: {user.premium_since.isoformat()}\n" \
                f"deaf: {user.deaf}\nmute: {user.mute}\n\n"
        user = user.user

    info += f"**User**\nid: {user.id}\nusername: {user.username}\n" \
            f"discriminator: {user.discriminator}\navatar: {user.avatar}\n" \
            f"public flags: {', '.join(f.name for f in user.public_flags)}"

    return info, True  # ephemeral


@interactions.command(Generate.to_application_command())
def generate():
    pass  # this function gets called before any subcommands or subcommand groups


@generate.subcommand()
def _hash():
    pass  # this function gets called before any subcommands in this group


@_hash.subcommand()
def sha1(_: CommandContext, text: str):
    return f'"{text}"\n=> `{hashlib.sha1(text.encode()).hexdigest()}`', True


@generate.fallback
@_hash.fallback
def generate_fallback(_: CommandContext):
    # called when no callback was registered for incoming subcommand name
    return "error: no subcommand provided", True


@interactions.command(HelloComponents.to_application_command())
def hello_components():
    btn = Button("my_button", style=ButtonStyle.PRIMARY, label="Click me!")

    return MessageResponse("This is a button.", components=[ActionRow(btn)])


@interactions.component("my_button")
def button_handler(ctx: ComponentContext):
    user = ctx.interaction.user
    return f"{user.username} clicked the button"


@button_handler.after_element
def _after_button_handler(ctx: AfterComponentContext):
    print("after button handler called", flush=True)
    ctx.send(
        f"this is a followup message to {ctx.interaction.user.username}'s button click"
    )


if __name__ == "__main__":
    app.run("0.0.0.0", os.getenv("PORT", 80))  # PORT will be set by Cloud Run
