#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import pandas as pd

# Edit the two paths to vanorder and vaninterest csv files
vanorder_path = 'vanorder.csv'
vaninterest_path = 'vaninterest.csv'

# Read the two csv into pandas DataFrame, parsing the datetime columns
vanorder = pd.read_csv(vanorder_path, parse_dates=['order_datetime', 'txCreate'])
vaninterest = pd.read_csv(vaninterest_path, parse_dates=['txCreate'])
