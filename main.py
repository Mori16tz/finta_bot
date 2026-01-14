import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from database import Vorlesung, add_entry, delete_entry, get_entry
import datetime

bot = commands.Bot(command_prefix="",
                   intents=discord.Intents.all(), help_command=None)


@bot.event
async def on_ready() -> None:
    await bot.tree.sync()


@bot.tree.command(name="eintrag", description="Einen neuen Eintrag hinzufügen")
@app_commands.describe(optionen="Fach", gesamt="Gesamtanzahl Teilnehmer", finta="FINTA-Teilnehmer", num="1. oder 2. Vorlesung der Woche")
async def eintrag(interaction: discord.Interaction, optionen: Vorlesung, gesamt: str, finta: str, num: str):
    if get_entry(optionen, datetime.date.today()) is not None:
        await interaction.response.send_message("Der Eintrag für heute existiert bereits")
        return
    add_entry(optionen, gesamt, finta, num)
    await interaction.response.send_message(f"Der Eintrag\nFach:{optionen}\nDatum: {datetime.date.today()}\nGesamt: {gesamt}\nFINTA: {finta}\nNummer: {num}\nwurde angelegt.")


@bot.tree.command(name="nachtrag", description="Einen Eintrag nachtragen")
@app_commands.describe(optionen="Fach", gesamt="Gesamtanzahl Teilnehmer", finta="FINTA-Teilnehmer", date="Datum", num="1. oder 2. Vorlesung der Woche")
async def nachtrag(interaction: discord.Interaction, date: str, optionen: Vorlesung, gesamt: str, finta: str, num: str):
    date_ = convert(date)
    if get_entry(optionen, date_) is not None:
        await interaction.response.send_message("Dieser Eintrag existiert bereits")
        return
    add_entry(optionen, gesamt, finta, num, date_)
    await interaction.response.send_message(f"Der Eintrag\nFach:{optionen}\nDatum: {date}\nGesamt: {gesamt}\nFINTA: {finta}\nNummer: {num}\nwurde angelegt.")


@bot.tree.command(name="löschen", description="Einen Eintrag löschen")
@app_commands.describe(optionen="Fach", date="Datum")
async def löschen(interaction: discord.Interaction, date: str, optionen: Vorlesung):
    date_ = convert(date)
    if get_entry(optionen, date_) is None:
        await interaction.response.send_message("Dieser Eintrag existiert nicht")
        return
    delete_entry(optionen, date_)
    await interaction.response.send_message(f"Der Eintrag für {optionen} vom {date} wurde gelöscht")


def convert(date: str) -> datetime.date:
    full = date.split(".")
    return datetime.date(int(full[2])+2000, int(full[1]), int(full[0]))


load_dotenv()
TOKEN = os.getenv("TOKEN", "no Token set")

bot.run(TOKEN)
