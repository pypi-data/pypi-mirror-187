"""Module containing the classes to get data from the Etherscan API."""

import datetime as dt
import functools
from typing import Callable, Any

from etherscan import Etherscan
import numpy as np
import pandas as pd


class EtherCrammer:
    """A class that handles efficient and complete Etherscan data downloads."""

    def __init__(
        self,
        api_key: str,
        address: str = None,
        contract: str = None,
        startperiod: str = None,
        endperiod: str = None,
        startblock: int = None,
        endblock: int = None,
    ) -> None:
        """Initializes the EtherCrammer class.

        Args:
            api_key (str): The key to the Etherscan api
            address (str, optional): The Ethereum address to use in history
                search. Defaults to None.
            contract (str, optional): The contract address to use in history
                search. Defaults to None.
            startperiod (str, optional): Time string (formatted YYYY-MM-DD) to
                start the period. Defaults to None.
            endperiod (str, optional): Time string (formatted YYYY-MM-DD) to
                start the period. Defaults to None.
            startblock (int, optional): The block to start the search interval.
                Defaults to None.
            endblock (int, optional): The block to end the search interval.
                    Defaults to None.
        """
        self._api = Etherscan(api_key)
        self._datetime_format = '%Y-%m-%d'
        self._address = None
        self._contract = None
        self._startblock = None
        self._endblock = None
        self.set_address_and_contract(address, contract)
        self.set_period(startperiod, endperiod, startblock, endblock)

    def _test_has_results(
        self, method: Callable, endblock: int, startblock: int, page: int
    ) -> bool:
        """A quick search with only one result to check transaction counts"""
        try:
            method(
                address=self._address,
                endblock=endblock,
                startblock=startblock,
                sort='desc',
                offset=1,
                page=page,
            )
            return True
        except AssertionError as e:
            if str(e) == '[] -- No transactions found':
                return False
            raise e

    def _convert_datetime_to_block(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            timestamp = func(self, *args, **kwargs).timestamp()
            block = self._api.get_block_number_by_timestamp(
                round(timestamp), closest='before'
            )
            return int(block)

        return wrapper

    @_convert_datetime_to_block
    def _get_block_at_date_start(self, datestring: str):
        return dt.datetime.strptime(datestring, self._datetime_format)

    @_convert_datetime_to_block
    def _get_current_block(self):
        return dt.datetime.now()

    def _recursive_transaction_download(
        self, search: str = 'eth'
    ) -> list[dict[str:Any]]:
        def _recursion(endblock: int, increment: int):
            # The startblock can never be less than 0.
            increment = increment if endblock > increment else endblock
            startblock = endblock - increment
            # If there are no results, nothing is added.
            if not self._test_has_results(method_paginated, endblock, startblock, 1):
                return
            # Etherscan has a maximum amount of results it will return. If the max is hit, it will try again after cutting the period in half.
            if self._test_has_results(method_paginated, endblock, startblock, 10000):
                increment = increment // 2
                _recursion(endblock, increment)
                endblock = endblock - increment
                increment = endblock - startblock
                _recursion(endblock, increment)
                return
            transactions = method(
                address=self._address,
                startblock=startblock,
                endblock=endblock,
                sort='desc',
            )
            all_transactions.extend(transactions)

        all_transactions = []
        if search == 'eth':
            method = self._api.get_normal_txs_by_address
            method_paginated = self._api.get_normal_txs_by_address_paginated
        elif search == 'erc20':
            method = self._api.get_erc20_token_transfer_events_by_address
            method_paginated = (
                self._api.get_erc20_token_transfer_events_by_address_paginated
            )
        else:
            raise ValueError('Choose between "eth" or "erc20" for "search"')
        _recursion(self._endblock, self._endblock - self._startblock)
        return all_transactions

    def _simplify_erc20_value(self, df: object) -> object:
        """ERC20 Token amounts are expressed using two columns. This function
        consolidates them to their numerical values"""
        decimal_column = 'tokenDecimal'
        value_column = 'value'
        df[decimal_column] = df[decimal_column].replace('', np.nan)
        df[decimal_column] = 10 ** df[decimal_column].astype(float)
        df[value_column] = df[value_column].astype(float) / df[decimal_column]
        return df.drop(columns=[decimal_column])

    def _convert_wei_to_eth(self, df: object) -> object:
        """All results from API are expressed in wei. Converts to human
        readable eth units."""
        value_column = 'value'
        df[value_column] = df[value_column].astype(float) / 10**18
        return df

    def _add_direction_column(self, df: object) -> object:
        if not self._address:
            return df
        direction_column = 'direction'
        direction_values = ['SELF', 'IN', 'OUT']
        incoming = df['to'] == self._address
        outgoing = df['from'] == self._address
        conditions = pd.concat(
            [incoming & outgoing, incoming & ~outgoing, ~incoming & outgoing], axis=1
        )
        conditions.columns = direction_values
        df[direction_column] = conditions.idxmax(axis=1)
        return df

    def _results_to_dataframe(
        self, transactions: list[dict[str:Any]], search: str = 'eth'
    ) -> object:
        timestamp_column = 'timeStamp'
        time_column = 'time'
        df = pd.DataFrame(transactions)
        df[timestamp_column] = pd.to_datetime(
            df[timestamp_column].astype(int), unit='s'
        )
        if search == 'eth':
            df = self._convert_wei_to_eth(df)
        elif search == 'erc20':
            df = self._simplify_erc20_value(df)
        df = self._add_direction_column(df)
        return df.rename(columns={timestamp_column: time_column})

    def create_filename(self, search: str) -> str:
        """ "Generates a filename based on search.

        Args:
            search (str): The search type (will go at the start of the filename)

        Returns:
            str: A string for a filename based on search.
        """
        s = f"{search}_"
        if self._address:
            s += "a_" + self._address + "_"
        if self._contract:
            s += "c_" + self._contract + "_"
        return f"{s}{self._startblock}-{self._endblock}.csv"

    def set_address_and_contract(
        self, address: str = None, contract: str = None
    ) -> None:
        """Sets the instance variables for address and contract for ethereum
        searches.

        Args:
            address (str, optional): An ethereum address hash. Defaults to None.
            contract (str, optional): An ethereum contract hash. Defaults to
                None.

        Raises:
            ValueError: If anything other than address is used.
        """
        if contract or not address:
            raise ValueError(
                'Only address supported at this time. Must choose an address without specifying contract'
            )
        self._address = address.lower()

    def set_period(
        self,
        startperiod: str = None,
        endperiod: str = None,
        startblock: int = None,
        endblock: int = None,
    ) -> None:
        """Sets the objects startblock and enblock variables to manage the
        search interval.

        Args:
            startperiod (str, optional): Time string (formatted YYYY-MM-DD) to
                start the period. Defaults to None.
            endperiod (str, optional): Time string (formatted YYYY-MM-DD) to
                start the period. Defaults to None.
            startblock (int, optional): The block to start the search interval.
                Defaults to None.
            endblock (int, optional): The block to end the search interval.
                    Defaults to None.

        Raises:
            ValueError: When there is an overlap between setting by period and
                setting by block.
        """
        if (startperiod is not None and startblock is not None) or (
            endperiod is not None and endblock is not None
        ):
            raise ValueError(
                'Must start or end cannot have both a value for block and period.'
            )
        if startblock is not None:
            self._startblock = startblock
        elif startperiod:
            self._startblock = self._get_block_at_date_start(startperiod)
        elif self._startblock is None:
            self._startblock = 0
        if endblock is not None:
            self._endblock = endblock
        elif endperiod:
            self._endblock = self._get_block_at_date_start(endperiod)
        elif self._endblock is None:
            self._endblock = self._get_current_block()
        if self._endblock < self._startblock or self._startblock < 0:
            raise ValueError(
                'Value for startblock must be less than endblock and nonzero'
            )

    def download_eth_history(
        self, search: str = 'eth', output_path: str = None
    ) -> object:
        """Downloads ethereum history according to the objects configuration to
        a pandas DataFrame.

        Args:
            search (str, optional): The search type. Currently must choose
                between "eth" (normal ethereum transactions) and "erc20"
                (ERC-20 transactions) Defaults to 'eth'.

        Returns:
            object: A Pandas DataFrame containing the downloaded data.
        """
        print("Scraping transactions. May take a while for very large amounts.")
        transactions = self._recursive_transaction_download(search=search)
        if len(transactions) == 0:
            print('No results found')
            return
        df = self._results_to_dataframe(transactions, search)
        if output_path:
            df.to_csv(output_path, index=False)
            print(f"Output saved to {output_path}")
        return df


def main():
    api_key = ''
    address = ''
    eth = EtherCrammer(
        api_key, address, startperiod='2022-01-01', endperiod='2023-01-01'
    )
    hist = eth.download_eth_history(search='eth', output_path='test.csv')
    print(hist)


if __name__ == '__main__':
    main()
