import topsis.topsis as topsis
topsis.calculate("mydata.csv","output.csv",weights="1,1,1,1,1",impacts="+,+,-,+,+", verbose=True, overwrite=True)