seqs = open('Copia.complete.all_clasters.clades.fasta')
clustername = ''
text = []
n=0

# separating whole file to file per cluster
for i in seqs.readlines():
    if '>' in i:
        i = i.strip()
        if i.split('|')[-1]!=clustername:
            if clustername:
                f.writelines('\n'.join(text))
                f.close()
                n+=1
                if n%10==0:
                    print(n)
                text = []
                clustername = i.split('|')[-1]
                f = open(f'./clusters/{clustername}.fasta','w')
            else:
                clustername = i.split('|')[-1]
                f = open(f'./clusters/{clustername}.fasta','w')
    text.append(i.strip())
f.writelines('\n'.join(text))
f.close()
