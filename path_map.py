
from scipy import io as io
import numpy as np
import pylab as pl


def find_k(array,value):
    k = (np.abs(array-value)).argmin()
    return k

def path_map(pos,spk):

    posx = pos["posx"].flatten()
    posy = pos["posy"].flatten()
    spkt = spk["cellTS"].flatten()

    spkx = posx[[find_k(pos["post"],t) for t in spkt]]
    spky = posy[[find_k(pos["post"],t) for t in spkt]]

    from matplotlib import rc

    rc('text', usetex=True)
    pl.rcParams['text.latex.preamble'] = [
        r'\usepackage{tgheros}',    # helvetica font
        r'\usepackage{sansmath}',   # math-font matching  helvetica
        r'\sansmath'                # actually tell tex to use it!
        r'\usepackage{siunitx}',    # micro symbols
        r'\sisetup{detect-all}',    # force siunitx to use the fonts
    ]  

    fig = pl.figure(figsize=(4.1,4.1))
    pl.plot(posx,posy, 'k', lw=0.5)
    pl.plot(spkx,spky, '.', color='red')
    # pl.colorbar(label="Hz")
    pl.gca().set_aspect('equal', adjustable='box')
    pl.xlim(-50,50)
    pl.ylim(-50,50)
    pl.xticks([-50,-25,0,25,50])
    pl.yticks([-50,-25,0,25,50])
    # pl.xticks(np.linspace(0,len(im),nlabels)-0.5,
    #           np.linspace(-50,50,nlabels).astype('int'))
    # pl.yticks(np.linspace(0,len(im),nlabels)-0.5,
    #           np.linspace(-50,50,nlabels).astype('int'))
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
        
    fig = path_map(pos,spk)
    fig.savefig("img/path_map.png", dpi=600, bbox_inches='tight')
