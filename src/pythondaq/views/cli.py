from pythondaq.models.diode_experiment import DiodeExperiment
import csv
from os import listdir, path, mkdir, getcwd
import matplotlib.pyplot as plt
import click


@click.group()
def cmd_group():
    pass


@cmd_group.command("list")
def list_devices():
    pass


@cmd_group.command()
def scan():
    pass


if __name__ == "main":
    cmd_group()
