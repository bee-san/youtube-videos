import random
import click

# Define the number of times to run the simulation
num_trials = 10000


def one_run(money, kelly=False):
    # Define the probability of getting a head
    prob_head = 0.5

    # Define the number of times we get a head
    num_heads = 0

    # Define the number of times we get a tail
    num_tails = 0

    # The amount of money we start with
    # TODO show how if we start with more money, we are more likely to get more money
    money = money

    # How many months do we run this experiment for?
    # 240 months = 20 years
    months = 240

    # How much money we take out of our bank account each month
    # Only activated on Kelly's Formula
    savings = 0

    # Define the number of times we get a head
    for trial in range(months):

        # Flip the coin
        if random.uniform(0, 1) <= prob_head:

            # We got a head
            num_heads += 1

            # Double the money
            money = money * 2
        else:

            # We got a tail
            num_tails += 1

            # Halve the money
            money = money / 2

        if kelly:
            total = money + savings
            savings = total / 2
            money = total / 2

    # Return the amount of money at the end of the experiment
    deposit = money + savings
    return deposit


import click


@click.command()
@click.option(
    "--kelly",
    is_flag=True,
    default=False,
    help="Run the simulation with kelly formula",
)
@click.option(
    "--money",
    help="Run the simulation with the amount of money",
    default=0.1,
    type=float,
)
def main(kelly, money):
    returns = []
    returns_kelly = []
    if kelly:
        for i in range(0, num_trials):
            counter = one_run(kelly=True, money=money)
            returns_kelly.append(counter)

    for i in range(0, num_trials):
        returns.append(one_run(money))

    boundaries = sort_boundaries(returns)

    if kelly:
        boundaries_kelly = sort_boundaries(returns_kelly)

    if kelly:
        make_table(boundaries, kelly=True, boundaries_kelly=boundaries_kelly)
    else:
        make_table(boundaries)


def sort_boundaries(returns):
    boundaries = {
        "<= £0.01": 0,
        "£0.01 to £0.10": 0,
        "£0.10 to £1": 0,
        "£1 to £10": 0,
        "£10 to £100": 0,
        "£100 to £1000": 0,
        "£1000 to £10,000": 0,
        "£10,000 to £100,000": 0,
        "£100,000 to £1 million": 0,
        "£1 million to £10 million": 0,
        "£10 million to £100 million": 0,
        "£100 million to £1 billion": 0,
        "> £1 billion": 0,
    }
    for i in returns:
        if i <= 0.01:
            boundaries["<= £0.01"] += 1
        elif i > 0.01 and i <= 0.10:
            boundaries["£0.01 to £0.10"] += 1
        elif i > 0.10 and i <= 1:
            boundaries["£0.10 to £1"] += 1
        elif i > 1 and i <= 10:
            boundaries["£1 to £10"] += 1
        elif i > 10 and i <= 100:
            boundaries["£10 to £100"] += 1
        elif i > 100 and i <= 1000:
            boundaries["£100 to £1000"] += 1
        elif i > 1000 and i <= 10000:
            boundaries["£1000 to £10,000"] += 1
        elif i > 10000 and i <= 100000:
            boundaries["£10,000 to £100,000"] += 1
        elif i > 100000 and i <= 1000000:
            boundaries["£100,000 to £1 million"] += 1
        elif i > 1000000 and i <= 10000000:
            boundaries["£1 million to £10 million"] += 1
        elif i > 10000000 and i <= 100000000:
            boundaries["£10 million to £100 million"] += 1
        elif i > 100000000 and i <= 1000000000:
            boundaries["£100 million to £1 billion"] += 1
        elif i > 100_000_0000:
            boundaries["> £1 billion"] += 1
    return boundaries


def make_table(boundaries, kelly=False, boundaries_kelly=None):
    from rich.console import Console
    from rich.table import Table

    console = Console()

    # Create the table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Wealth")
    table.add_column("Chance you'll get this")
    if kelly:
        table.add_column("Chance you'll get this (Kelly Formula)")

    for key, value in boundaries.items():
        if kelly:
            table.add_row(
                key, gen_row_percent(value), gen_row_percent(boundaries_kelly[key])
            )
        else:
            table.add_row(key, gen_row_percent(value))

    # Print the table
    console.print(table)


def gen_row_percent(value):
    return str(round((value / num_trials) * 100)) + "%"


if __name__ == "__main__":
    main()
