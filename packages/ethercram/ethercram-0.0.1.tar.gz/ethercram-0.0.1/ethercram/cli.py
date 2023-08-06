import argparse
from json import load
from typing import Any, Union

from .__version__ import __version__
from . import EtherCrammer


def update_kwargs_from_loop(kwargs: dict[str, Any], param_dict: dict[str, Any]) -> None:
    """Allows function defaults to stay intact when flags are unspecified by
    creating a dict of kwargs for only those that contain set values.

    Args:
        kwargs (dict[str, Any]): A dictionary of output keyword arguments to
            pass to the function that will be updated with set values.
        param_dict (dict[str, Any]): A dictionary of keys and values to
            extract when set obtained by argparse inputs.
    """

    for key, value in param_dict.items():
        if value is not None:
            kwargs.update({key: value})


def load_config_file(config_path: str = 'config.json') -> dict[str, Union[str, int]]:
    """Loads a dictionary of API connection arguments from a config file.

    Args:
        config_path (str, optional): The path to the config json. Defaults to
            'config.json'.

    Returns:
        dict[str, Union[str, int]]: A dictionary of API connection arguments.
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        config = load(f)
    return config


def execute_command(args: object) -> None:
    """Creates a search object and executes a search.

    Args:
        args (object): Parsed arguments object from argparse.
    """

    config = args.config_path if args.config_path else 'config.json'
    config = load_config_file(config)
    kwargs = {}
    update_kwargs_from_loop(
        kwargs,
        {
            'address': args.address,
            'contract': args.contract,
            'startblock': args.startblock,
            'endblock': args.endblock,
            'startperiod': args.startperiod,
            'endperiod': args.endperiod,
        },
    )
    ether_crammer = EtherCrammer(api_key=config['etherscan_key'], **kwargs)
    output = args.output if args.output else ether_crammer.create_filename(args.command)
    ether_crammer.download_eth_history(args.command, output_path=output)


def run_cmd_line() -> None:
    """Runs the argparse CLI functions."""

    parser = argparse.ArgumentParser(
        prog='Ethercram',
        description='A command line interface for extracting full Ethereum transaction history on Etherscan',
    )
    parser.add_argument(
        '--version', version=f'%(prog)s {__version__}', action='version'
    )
    subparsers = parser.add_subparsers(help='Commands', dest='command')

    eth = subparsers.add_parser(
        'eth', help='Downloads standard ethereum transaction history.'
    )
    erc20 = subparsers.add_parser(
        'erc20', help='Downloads erc20 token transaction history.'
    )

    for subparser in [eth, erc20]:
        subparser.add_argument(
            '--config_path',
            '-c',
            help='The path to the config json',
            metavar='FILEPATH',
            type=str,
        )
        subparser.add_argument(
            '--address', '-w', help='The wallet address', metavar='ADDRESS', type=str
        )
        subparser.add_argument(
            '--contract',
            '-x',
            help='Currently does nothing. Will have use in future versions.',
            metavar='CONTRACT ADDRESS',
            type=str,
        )
        subparser.add_argument(
            '--startblock',
            '-b',
            help='The start block for ranges (Choose between block or period)',
            metavar='NUMBER',
            type=int,
        )
        subparser.add_argument(
            '--endblock',
            '-k',
            help='The end block for ranges (Choose between block or period)',
            metavar='NUMBER',
            type=int,
        )
        subparser.add_argument(
            '--startperiod',
            '-p',
            help='The start date (formated YYYY-MM-DD) for ranges (Choose between block or period)',
            metavar='DATE',
            type=str,
        )
        subparser.add_argument(
            '--endperiod',
            '-r',
            help='The end date (formated YYYY-MM-DD) for ranges (Choose between block or period)',
            metavar='DATE',
            type=str,
        )
        subparser.add_argument(
            '--output',
            '-o',
            help='The path to the output csv. (If unspecified, a search based filename will be generated to your current path.)',
            metavar='PATH',
            type=str,
        )

    args = parser.parse_args()

    if args.command in ['eth', 'erc20']:
        execute_command(args)
