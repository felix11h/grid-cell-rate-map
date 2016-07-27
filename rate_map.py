
from scipy import io as io
import numpy as np
import pylab as pl


def find_k(array,value):
    k = (np.abs(array-value)).argmin()
    return k

def rate_map(pos,spk,k=10):

    bin_edges = np.linspace(-50,50,k)

    posx = pos["posx"].flatten()
    posy = pos["posy"].flatten()
    spkt = spk["cellTS"].flatten()
    
    indx = [find_k(pos["post"],t) for t in spkt]
    indy = [find_k(pos["post"],t) for t in spkt]

    occup_m = np.histogram2d(posx, posy,
                            bins=(bin_edges,bin_edges))[0]*0.02
    activ_m = np.histogram2d(posx[indx],posy[indy],
                            bins=(bin_edges,bin_edges))[0]
  
    rate_map = activ_m/occup_m

    return rate_map
   

def plot_rate_map(rm, nlabels=5):

    from matplotlib import rc

    rc('text', usetex=True)
    pl.rcParams['text.latex.preamble'] = [
        r'\usepackage{tgheros}',    # helvetica font
        r'\usepackage{sansmath}',   # math-font matching  helvetica
        r'\sansmath'                # actually tell tex to use it!
        r'\usepackage{siunitx}',    # micro symbols
        r'\sisetup{detect-all}',    # force siunitx to use the fonts
    ]  

    fig = pl.figure(figsize=(6,4))
    pl.imshow(rm, interpolation='none')
    pl.colorbar(label="Hz")
    pl.xticks(np.linspace(0,len(rm),nlabels)-0.5,
              np.linspace(-50,50,nlabels).astype('int'))
    pl.yticks(np.linspace(0,len(rm),nlabels)-0.5,
              np.linspace(-50,50,nlabels).astype('int'))
    return fig


   
    

if __name__ == "__main__":

    # from http://www.ntnu.edu/kavli/research/grid-cell-data
    pos = io.loadmat('10704-07070407_POS.mat')
    spk = io.loadmat('10704-07070407_T2C3.mat')

    '''
    pos["post"]: times at which positions were recorded
    pos["posx"]: x positions
    pos["posy"]: y positions
    ---
    spk["cellTS"]: spike times
    '''
        
    rm = rate_map(pos,spk,15)
    fig = plot_rate_map(rm)
    fig.savefig("img/rate_map.png", dpi=600, bbox_inches='tight')
