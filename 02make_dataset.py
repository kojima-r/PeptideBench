from Bio import SeqIO
import sys
import glob
import os
all_data={}
all_seq={}
name_list=[]
for filename in glob.glob("data/*.fasta"):
    name,_=os.path.splitext(os.path.basename(filename))
    name_list.append(name)
    for record in SeqIO.parse(filename, 'fasta'):
        id_part = record.id
        desc_part = record.description
        seq = record.seq
        label=""
        if "|" in id_part:
            arr=id_part.split("|")
            id_part=arr[0]
            label=arr[1]
            #print('id:', id_part)
            #print('desc:', desc_part)
            #print('seq:', seq)
        key=str(id_part)
        if key not in all_data:
            all_data[key]=[]
        all_data[key].append((name,label))
        non_ascii=0
        try:
            seq_s=str(seq)
        except UnicodeDecodeError:
            print("[WARN]",name,id_part, "contains non-ascii characters")
            seq_s=bytes(seq).decode('utf-8')
            non_ascii=1
        if seq_s.isalpha():
            non_alphabet=0
        else:
            non_alphabet=1
        all_seq[key]=(seq_s,non_ascii,non_alphabet)

print(len(all_data))
with open("all_data.tsv","w") as ofp:
    ofp.write("\t".join(["id","seq","non_ascii","non_alphabet"]+name_list))
    ofp.write("\n")
    for key,val in all_data.items():
        seq,non_ascii,non_alphabet=all_seq[key]
        line=[key,seq,str(non_ascii), str(non_alphabet)]
        for name in name_list:
            el="0"
            if (name,"") in val:
                el="1"
            elif (name,"predicted") in val:
                el="2"
            line.append(el)
        ofp.write("\t".join(line))
        ofp.write("\n")



