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

from discord_interactions.ocm import Command, Option, OptionChoices
from discord_interactions import ApplicationCommandOptionType


class Ping(Command):
    """ simple ping command """


class Echo(Command):
    """ what goes around comes around """

    message: str = Option("This will be echoed.", required=True)


class RPSSymbol(OptionChoices):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


class RPS(Command):
    """ Play Rock, Paper, Scissors! """

    symbol: RPSSymbol = Option("rock, paper or scissors", required=True)


class Guess(Command):
    """ Guess my number! """

    number: int = Option("what do you guess?", required=True)
    min_num: int = Option("smallest possible number (default: 0)")
    max_num: int = Option("biggest possible number (default: 10)")


class Delay(Command):
    """ Responds after a given time. """

    seconds: int = Option("The time to wait", required=True)


class Hug(Command):
    """ Hug someone nice. """

    cutie: ApplicationCommandOptionType.USER = Option("hug this person", required=True)


class UserInfo(Command):
    """ Retrieve info about a specific user. """

    user: ApplicationCommandOptionType.USER = Option("user to get info about")
    raw: bool = Option("return the raw JSON data received from Discord")
