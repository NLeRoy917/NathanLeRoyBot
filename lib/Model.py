import gpt_2_simple as gpt2
from datetime import datetime

class Model():

    def __init__(self):
        self._sess = gpt2.start_tf_sess()
        return
    
    def load_model(self,run_name='run1'):
        gpt2.load_gpt2(self._sess, run_name=run_name)
    
    def generate(self,length=30, temperature=0.95, prefix=None, nsamples=1, batch_size=1):
        if prefix:
            tweet = gpt2.generate(
                  self._sess, 
                  length=length,
                  temperature=temperature,
                  prefix=prefix,
                  nsamples=nsamples,
                  batch_size=batch_size,
                  return_as_list=True
                  )[0]
        else:
            tweet = gpt2.generate(
                  self._sess, 
                  length=length,
                  temperature=temperature,
                  prefix=prefix,
                  nsamples=nsamples,
                  batch_size=batch_size,
                  return_as_list=True
                  )[0]

        
        return tweet