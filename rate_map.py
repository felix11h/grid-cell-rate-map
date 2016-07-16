

from scipy import io as io
import numpy as np
import pylab as pl

data = io.loadmat(pth)



def load_data(animal,session,data_type):
    dstring="%s-%s_%s.mat" %(animal,session,data_type)
    pth = os.path.join(base_pth,dstring)
    data = io.loadmat(pth)
    return data


def find_id(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx


def rate_map(pos,spk,k=10):

    bin_edges = np.linspace(-50,50,k)

    posx = pos["posx"].flatten()
    posy = pos["posy"].flatten()
    
    indx = [find_id(pos["post"],t) for t in spk["cellTS"].flatten()]
    indy = [find_id(pos["post"],t) for t in spk["cellTS"].flatten()]    

    im_s = np.histogram2d(posx[indx],posy[indy], bins=(bin_edges,bin_edges))[0]
    im_all = np.histogram2d(posx, posy, bins=(bin_edges,bin_edges))[0]*0.02
    
    im = im_s/im_all
    return im
   

def plot_rate_map(im, nlabels=5):

    rc('text', usetex=True)
    pl.rcParams['text.latex.preamble'] = [
        r'\usepackage{tgheros}',    # helvetica font
        r'\usepackage{sansmath}',   # math-font matching  helvetica
        r'\sansmath'                # actually tell tex to use it!
        r'\usepackage{siunitx}',    # micro symbols
        r'\sisetup{detect-all}',    # force siunitx to use the fonts
    ]  


    fig = pl.figure(figsize=(6,4))
    pl.imshow(im, interpolation='none')
    pl.colorbar(label="Hz")
    pl.xticks(np.linspace(0,len(im),nlabels)-0.5,
              np.linspace(-50,50,nlabels).astype('int'))
    pl.yticks(np.linspace(0,len(im),nlabels)-0.5,
              np.linspace(-50,50,nlabels).astype('int'))
    return fig


def save_figure(fig, animal, session, cell):
    
    fig.suptitle(cell, fontweight='bold')
    fig.savefig("img/%s_%s-%s.pdf" %(animal, session, "T1C1"), dpi=600,
                bbox_inches='tight')

    
    

if __name__ == "__main__":

    base_pth = "../data/8F6BE356-3277-475C-87B1-C7A977632DA7/all_data/"

    animal = "10704"
    session = "07070407"
    cell = "T2C3"
    
    pos = load_data(animal, session ,"POS")
    spk = load_data(animal, session, cell)
    
    im = rate_map(pos,spk,15)

    fig = plot_rate_map(im)
