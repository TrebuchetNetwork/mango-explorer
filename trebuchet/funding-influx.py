#!/usr/bin/env python3

import argparse
import os
import os.path
import sys
import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import mango  # nopep8

parser = argparse.ArgumentParser(
    description="Shows the current funding rates for a perp market in a Mango Markets Group."
)

mango.ContextBuilder.add_command_line_parameters(parser)
'''
parser.add_argument(
    "--market",
    type=str,
    required=True,
    help="symbol of the market to look up, e.g. 'ETH-PERP'",
)
'''
args: argparse.Namespace = mango.parse_args(parser)


with mango.ContextBuilder.from_command_line_parameters(args) as context:
    #perp_market = mango.PerpMarket.ensure(mango.market(context, args.market))
    #mango.output(perp_market.fetch_funding(context))

    client = InfluxDBClient(url="http://localhost:8086", token="my-super-secret-auth-token", org="my-org")
    write_api = client.write_api(write_options=SYNCHRONOUS)
    bucket = "my-bucket"

    # GET PERP FUNDING RATES
    perps = []
    perps.append("SOL-PERP")
    perps.append("ETH-PERP")
    perps.append("BTC-PERP")
    perps.append("MNGO-PERP")
    perps.append("ADA-PERP")
    perps.append("BNB-PERP")
    perps.append("RAY-PERP")
    perps.append("SRM-PERP")
    perps.append("GMT-PERP")
    perps.append("FTT-PERP")
    perps.append("AVAX-PERP")

    perp_markets_list = []
    for perp_temp in perps:
        perp_market = mango.PerpMarket.ensure(mango.market(context, perp_temp))
        perp_markets_list.append(perp_market)

    while (True):
        try:
            time.sleep(5)
            for perpi in perp_markets_list:
                funding = perpi.fetch_funding(context)
                orderbook = perpi.fetch_orderbook(context)
                p = Point("funding-rates").tag("market", perpi.symbol)
                p.field("funding", funding.rate)
                p.field("open_interest", funding.open_interest)
                p.field("oracle_price", funding.oracle_price)
                p.field("mid_price", orderbook.mid_price)
                p.field("long_funding", perpi.underlying_perp_market.long_funding)
                p.field("short_funding", perpi.underlying_perp_market.short_funding)
                p.field("apr", funding.extrapolated_apr)
                p.field("apy", funding.extrapolated_apy)
                p.field("spread", orderbook.spread)
                print(perpi.symbol)
                '''
                p.field("borrow", rates.borrow)
                p.field("deposit", rates.deposit)
                p.field("optimal_rate", banka.loaded_root_bank.optimal_rate)
                p.field("max_rate", banka.loaded_root_bank.max_rate)
                p.field("optimal_util", banka.loaded_root_bank.optimal_util)
                '''
                write_api.write(bucket=bucket, record=p)
        except Exception as e:
                print("Oops!", e.__class__, "occurred.")
                #get restart logic in place
                time.sleep(10)
                for perp_temp in perps:
                    perp_market = mango.PerpMarket.ensure(mango.market(context, perp_temp))
                    perp_markets_list.append(perp_market)
        except:
            print("Something else went wrong")



