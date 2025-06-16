
fp=open("all_data.tsv")
h=next(fp)
arr=h.strip().split("\t")
name_list=arr[4:]
n=len(name_list)
count=0
counter={name:[0,0,0] for name in name_list}
counter["non_ascii"]=[0,0,0]
counter["non_alphabet"]=[0,0,0]
for line in fp:
    count+=1
    arr=line.strip().split("\t")
    non_ascii=int(arr[2])
    non_alphabet=int(arr[3])
    counter["non_ascii"][non_ascii]+=1
    counter["non_alphabet"][non_alphabet]+=1
    for i,e in enumerate(arr[4:]):
        counter[name_list[i]][int(e)]+=1

with open("all_data.stat.tsv","w") as ofp:
    ofp.write("\t".join(["name", "count", "predicted", "sum","count_ratio","predicted_ratio","sum_ratio"]))    
    ofp.write("\n")
    for k,v in counter.items():
        ofp.write("\t".join([k, str(v[1]), str(v[2]),str(v[1]+v[2]),  str(v[1]/count),str(v[2]/count),str((v[1]+v[2])/count)]))    
        ofp.write("\n")
print(count)
