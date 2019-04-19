import os

commonpath = os.path.dirname(__file__)
genpath = os.path.dirname(commonpath)
datapath = os.path.join(genpath, "data")

datafilepath = os.path.join(datapath, "test_data_zentao_login.xlsx")
print(datafilepath)