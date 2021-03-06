# Copyright 2020 Max Planck Institute for Software Systems

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from imgntWrapper import *
from Bandits import *
from pickle import dump,load
from sys import argv
import sys
from tqdm import tqdm
from datetime import datetime
from os import mkdir
from os.path import exists
if not exists("Bandits"):
    mkdir("Bandits")
path="Bandits/"+str(datetime.now())+"/"
mkdir(path)
sys.stdout=open(path+"log.txt","w")
tile=4
Data={}
Batch_size=40
succ=0
tot=0
for j in tqdm(range(0,1000,Batch_size)):
    tot+=Batch_size
    print("Starting attack on batch", j//Batch_size)
    corr=np.argmax(mymodel.predict(x_test[j:j+Batch_size]),1)==y_test.reshape(-1)[j:j+Batch_size]
    ret=attack(mymodel,x_test[j:j+Batch_size],1.0,0.1,tile,1,0.0001,8/255,corr,10000)
    dump(ret[0].reshape(Batch_size,256,256,3),open(path+"image_"+str(j)+"_to_"+str(j+Batch_size-1)+".pkl","wb"))
    for k in range(Batch_size):
        Data[j+k]=(ret[2][k],ret[1][k])
    succ+=sum(ret[2])
    print("Success rate is",100*succ/tot)
    dump(Data,open(path+"data.pkl","wb"))
