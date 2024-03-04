import numpy as np
import os
from matplotlib import pyplot as plt
import seaborn as sns

from Xana import Xana

import pandas
import pickle

  
def load_xana(database_id):
    """Loads setup and arrays from database.
    
    Args:
        databse_id (ind): index of the database.
        
    Returns:
        ana: Xana instance.
        nq (int): number of unique q-bins.
        nangles (int): number of unique angles.
        qv_phi (np.ndarray): array containing the q-values (qv_phi[:,0]) and angles
            (qv_phi[:,1]) of each q-ROI.
        qv, phi: the columns of qv_phi.
    """
    #
    d = Xana()
    d.load_db('../05-analysis-phis/analysis_database.pkl')
        
    if not database_id in d.db.index:
        raise ValueError(f'Index {database_id} not in database.')
    
    setupfile = d.db.loc[database_id, 'setupfile']
    d = Xana(setupfile=setupfile)
    d.load_db('../05-analysis-phis/analysis_database.pkl')
    
    
    phi = d.setup.phiv
    #print(f'angles array: {phi}')
    phi = phi[:,0] + phi[:,1]/2
    #print(f'angles vector: {phi}')
    qv = d.setup.qv
    #print(f'q-vector: {qv}')

    qv_phi = np.zeros((len(qv), 2))
    qv_phi[:,0] = qv
    i0 = 0
    for i1 in np.unique(qv, return_counts=True)[1]:
        qv_phi[i0:i0+i1,1] = phi[:i1]
        i0 += i1

    nangles = len(phi) # number of unqiue angles
    nq = len(np.unique(qv)) # number of unique q-values
    
    return d, nq, nangles, qv_phi, qv, phi