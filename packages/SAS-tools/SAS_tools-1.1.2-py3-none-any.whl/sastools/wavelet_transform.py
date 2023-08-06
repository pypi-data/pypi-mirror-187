from scipy import signal

import pandas as pd

class WaveletTransformer():

    def __init__(self, experimental_data : pd.DataFrame):

        self.exp_data = experimental_data
        self.x = self.exp_data.iloc[:,0].values.tolist()
        self.y = self.exp_data.iloc[:,1].values.tolist()


    def transform(self):
        
        cwt = signal.cwd(self.y,)
        print(cwt)