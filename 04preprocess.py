import pandas as pd

threshold_len=150

# 閾値の設定（必要に応じて調整）
# 条件に合致するnameを抽出（count_ratio または predicted_ratio が閾値以上）
def get_namelist(threshold=0.05):
    df = pd.read_csv("all_data.stat.tsv", sep="\t")
    filtered_names = df[
        df['sum_ratio'] >= threshold
    ]['name'].tolist()
    return filtered_names

filtered_name_list=get_namelist()
print(filtered_name_list)
print(len(filtered_name_list))


with open("all_data_preprocessed.tsv","w") as ofp:
    fp=open("all_data.tsv")
    h=next(fp)
    arr=h.strip().split("\t")
    name_list=arr[4:]
    new_name_list=[]
    new_name_idx=[]
    for i,e in enumerate(name_list):
        if e in filtered_name_list:
            new_name_list.append(e)
            new_name_idx.append(i+4)
    ###
    ofp.write("\t".join(["id","seq"] + new_name_list))
    ofp.write("\n")
    count=0
    success_cnt=0
    for line in fp:
        arr=line.strip().split("\t")
        seq=arr[1]
        non_ascii=arr[2]
        non_alphabet=arr[3]
        label_y=[1 if int(arr[i])>0 else 0 for i in new_name_idx]
        if sum(label_y)>0: # 一つ以上がpositive label
            if non_ascii=="0" and non_alphabet=="0"  \
                    and "X" not in seq and "x" not in seq \
                    and "B" not in seq and "b" not in seq \
                    and "J" not in seq and "j" not in seq \
                    and "Z" not in seq and "z" not in seq:
                if len(seq) <= threshold_len:
                    # standard fasta
                    success_cnt+=1
                    line_arr=[arr[0],seq] + list(map(str,label_y))
                    ofp.write("\t".join(line_arr))
                    ofp.write("\n")
        count+=1
    print(success_cnt,"/",count)
