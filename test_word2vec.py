import gensim
model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)  
 
sentences = ['this', 'is', 'the', 'good', 'machine', 'learning', 'book',
            'this', 'is',  'another', 'book']
           
 
vocab = model.vocab.keys()
wordsInVocab = len(vocab)
 
import numpy as np
 
def sent_vectorizer(sent, model):
    sent_vec = np.zeros(50)
    numw = 0
    for w in sent:
        try:
            vc=model[w]
            vc=vc[0:50]
            
            sent_vec = np.add(sent_vec, vc) 
            numw+=1
        except:
            pass
    return sent_vec / np.sqrt(sent_vec.dot(sent_vec))
 
V=[]
for sentence in sentences:
    V.append(sent_vectorizer(sentence, model))
from numpy.linalg import norm
results = [[0 for i in range(len(V))] for j in range(len(V))] 
 
for i in range (len(V) - 1):
    for j in range(i+1, len(V)):
            
       NVI=norm(V[i])
       NVJ=norm(V[j])
            
       dotVij =0
       NVI=0
       for x in range(50):
           NVI=NVI +  V[i][x]*V[i][x]
            
       NVJ=0
       for x in range(50):
           NVJ=NVJ +  V[j][x]*V[j][x]
             
       for x in range(50):
       
               dotVij = dotVij + V[i][x] * V[j][x]
          
       
       results[i][j] = dotVij / (NVI*NVJ) 
 
print (results)