# IbPy - Interactive Brokers Python API

## What is IbPy?

IbPy is a third-party implementation of the API used for accessing the
Interactive Brokers on-line trading system. IbPy implements
functionality that the Python programmer can use to connect to IB,
request stock ticker data, submit orders for stocks and futures, and
more.

IbPy was created prior the release of Interactive Brokers Python API. Accordingly,
this repository is about maintenance but not further development.

# Where can I get IbPy?

GitHub:

   https://gitlab.com/algorithmic-trading-library/ibpy3
   original ()

Original (older versions) of IbPy are available for download from:

   https://github.com/blampe/IbPy

Original authors
   IbPy library: Troy Melhase (troy@gci.net)
   Porting IbPy to python 3+: David Edwards (https://github.com/humdings)

# What are the requirements?

IbPy requires Python 3.x.
Previous python 2.5+ versions should work but no more tested.

TWS requires a web browser capable of executing Sun(R) Java(tm) applets.
TWS can also be started directly with Sun(R) Java(tm) and the
stand-alone package supplied by Interactive Brokers.

# What is Interactive Brokers?

From the page "About The Interactive Brokers Group":

> Interactive Brokers conducts its broker/dealer and proprietary trading
> businesses on 60 market centers worldwide. In its broker dealer agency
> business, IB provides direct access ("on line") trade execution and
clearing > services to institutional and professional traders for a wide
variety of > electronically traded products including options, futures,
stocks, forex, and > bonds worldwide. In its proprietary trading
business IB engages in market > making for its own account in about
6,500 different electronically traded > products. Interactive Brokers
Group and its affiliates now trade 19% of the > world’s exchange traded
equity options, and executes approximately 500,000 > trades per day.

# What Else?

IbPy is not a product of Interactive Brokers, nor is this project
affiliated with IB.

IbPy is installed with:

   $ pip install IbPy-lucidinvestor

The stand-alone TWS and other API software is available from IB:

   https://www.interactivebrokers.ca/en/trading/tws.php#tws-software

IbPy is distributed under the New BSD License. See the LICENSE file in
the release for details.
