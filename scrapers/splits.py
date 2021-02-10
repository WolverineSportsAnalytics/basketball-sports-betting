import click

@click.command()
@click.option('-c', '--conference', is_flag=True, 
              help='Gets the conference splits.')
@click.option('-d', '--division', is_flag=True, 
              help='Gets the conference splits.')
@click.option('--day', is_flag=True, 
              help='Gets the splits for each day Mon-Sun.')
@click.option('-l', '--location', is_flag=True, 
              help='Gets the home/away splits.')
@click.option('-r', '--rest', is_flag=True, 
              help='Gets the splits for each rest day.')
@click.option('-r', '--team', is_flag=True, 
              help='Gets the team splits.')
def splits(conference, division, day, location, rest, team):
    """Program that gets the splits from basketball reference."""
    if conference:
        get_conf_splits()
    elif division:
        get_div_splits()
        

def get_conf_splits():
    print('Conference splits')
    

def get_div_splits():
    print('Division splits')


if __name__ == '__main__':
    splits()