import numpy as np
import sys

import sys

from pathlib import Path
home = str(Path.home())

path = home+'/Platform/'

sys.path.insert (0, path)

from queue_req_resp import *
import time

RMQ = RabbitMQ()

l = ["Iris-Setosa", "Iris-Virginica", "Iris-Versicolor"]
for i in range(20):
    itr = np.random.randint(0, 3)
    RMQ.send('', "helper_test", str(l[itr]))
    time.sleep(2)

