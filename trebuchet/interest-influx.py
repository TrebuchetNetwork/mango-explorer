#!/usr/bin/env python3

import argparse
import os.path
import sys
import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import mango  # nopep8

parser = argparse.ArgumentParser(
    description="Shows the current interest rates for a token in a Mango Markets Group."
)
mango.ContextBuilder.add_command_line_parameters(parser)
args: argparse.Namespace = mango.parse_args(parser)

#while true restart logic
while True:
    try:
        with mango.ContextBuilder.from_command_line_parameters(args) as context:
            group = mango.Group.load(context)

            #TOKEN SYMBOLS
            token_symbols = []
            token_symbols.append("SOL")
            token_symbols.append("BTC")
            token_symbols.append("ETH")
            token_symbols.append("GMT")
            token_symbols.append("SRM")
            token_symbols.append("MNGO")
            token_symbols.append("RAY")
            token_symbols.append("AVAX")
            token_symbols.append("BNB")
            token_symbols.append("FTT")
            token_symbols.append("USDC")
            token_symbols.append("USDT")
            token_symbols.append("MSOL")
            token_symbols.append("COPE")





            token = mango.token(context, "SOL")
            token_bank = group.token_bank_by_instrument(token)
            interest_rates = token_bank.fetch_interest_rates(context)
            mango.output(interest_rates)


            client = InfluxDBClient(url="http://localhost:8086", token="my-super-secret-auth-token", org="my-org")
            write_api = client.write_api(write_options=SYNCHRONOUS)
            bucket = "my-bucket"

            token_banks=[]
            for token_b in token_symbols:
                token = mango.token(context, token_b)
                token_banka = group.token_bank_by_instrument(token)
                interest_rates = token_banka.fetch_interest_rates(context)
                token_banks.append(token_banka)
                #mango.output(interest_rates)

            while(True):
                time.sleep(5)
                print("Sleeping 5 Seconds heartbeat")
                interest_rates = token_bank.fetch_interest_rates(context)
                for banka in token_banks:
                    rates = banka.fetch_interest_rates(context)
                    p = Point("interest-rates").tag("symbol", banka.token.symbol)
                    p.field("borrow", rates.borrow)
                    p.field("deposit", rates.deposit)
                    p.field("optimal_rate", banka.loaded_root_bank.optimal_rate)
                    p.field("max_rate", banka.loaded_root_bank.max_rate)
                    p.field("optimal_util", banka.loaded_root_bank.optimal_util)
                    write_api.write(bucket=bucket, record=p)

                mango.output(interest_rates)
    except Exception as ex:
        print(str(ex))

    finally:
        # this block is always executed
        # regardless of exception generation.
        print('Restarting the service - something went wrong , wait for 10 sec')
        time.sleep(10)




