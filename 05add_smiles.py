import pandas as pd

# PyPept modules
from pyPept.sequence import Sequence
from pyPept.sequence import correct_pdb_atoms
from pyPept.molecule import Molecule
from pyPept.converter import Converter
from pyPept.conformer import Conformer
from pyPept.conformer import SecStructPredictor

# RDKit modules
from rdkit import Chem
from rdkit.Chem import Draw
from multiprocessing import Pool,TimeoutError

# プロセス数
n_jobs=32

def get_timeout(p,args):
    try:
        return p.get(timeout=60*60)
    except TimeoutError:
        print("timeout:",args)
        return None
    except:
        print("error:",args)
        return None

def fasta2smiles(seq):
    seq=seq.upper()
    blin = "-".join(seq)
    bseq = Sequence(blin)#BLIN
    mol = Molecule(bseq)
    romol = mol.get_molecule(fmt='ROMol')
    s=Chem.MolToSmiles(romol)
    return s

def get_seq_list(filename):
    fp=open(filename)
    h=next(fp)
    arr=h.strip().split("\t")
    seq_list=[]
    for line in fp:
        arr=line.strip().split("\t")
        seq=(arr[0],arr[1])
        seq_list.append(seq)
    return seq_list

def run(argv):
    seq_id, seq = argv
    try:
        smi=fasta2smiles(seq)
    except:
        print("error:",argv)
        return None
    return smi
seq_list=get_seq_list("all_data_preprocessed.tsv")
pool = Pool(n_jobs) 
pids=[(pool.apply_async(run, (argv,)),argv) for argv in seq_list]
results=[get_timeout(p,args) for p,args in pids]


with open("all_data_preprocessed_smi.tsv","w") as ofp:
    fp=open("all_data_preprocessed.tsv")
    h=next(fp)
    arr=h.strip().split("\t")
    name_list=arr[3:]
    ###
    ofp.write("\t".join(["id","seq","smi"] + name_list))
    ofp.write("\n")
    count=0
    success_cnt=0
    for line in fp:
        arr=line.strip().split("\t")
        seq=arr[1]
        label_y=arr[2:]
        if results[count] is not None:
            success_cnt+=1
            smi=results[count]
            line_arr=[arr[0],seq,smi] + label_y
            ofp.write("\t".join(line_arr))
            ofp.write("\n")
        count+=1
    print(success_cnt,"/",count)
