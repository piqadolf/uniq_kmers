def kmer_uniq(path, k):

    import os
    from Bio.Seq import Seq as Seq


    f = open(f'{path}')
    filtered_kmers = open(f'./{path[:-3]}_filtered.fas', 'w')
    filtered_list = []
    k_list = []
    kmer_names = []
    lines = f.readlines()
    n = 0

    max = 0
    for line in lines:
        if '>' in line:
            if int(line.strip()[1:]) > max:
                max = int(line.strip()[1:])
    print(path)
    print('max', max)
    f.seek(0)
    lines = f.readlines()
    for line in lines:
        if '>' in line:
            if int(line.strip()[1:]) > max//2:
                filtered_list.append(line.strip())
                switch = True
            else:
                switch = False
        else:
            if switch:
                filtered_list.append(line.strip())
    filtered_kmers.write('\n'.join(filtered_list))
    filtered_kmers.close()
    f.close()

    filtered_kmers = open(f'./{path[:-3]}_filtered.fas')
    cluster = open(f'../clades/{path}sta')
    lines = filtered_kmers.readlines()
    # clines = cluster.readlines()
    m = 0
    for line in lines:
        n=0
        m+=1
        if m%5000 == 0:
            print(m)
        if '>' not in line:
            kmer = line.strip()
            kmer_names.append(line.strip())
            rev_kmer = Seq(kmer)
            rev_kmer = rev_kmer.reverse_complement()
            n = os.system(f"grep -e '{kmer}' -e '{rev_kmer}'../clades/{path}sta | wc -l")
            # clines = cluster.readlines()
            # for cline in clines:
            #     rev_seq = Seq(cline.strip())
            #     rev_seq = rev_seq.reverse_complement()
            #     # if '>' not in cline:
            #     if kmer in cline or kmer in rev_seq:
            #         n+=1
            if m%5000 == 0:
                print(kmer, n)
            k_list.append(n)
            # cluster.seek(0)
    data = {'kmer':kmer_names, 'count':k_list}
    uniq_doc_list = []
    for c, v in enumerate(kmer_names):
        count_value = f'>{k_list[c]}'
        uniq_doc_list.append(count_value, v)
    path_uniq = open(f'{path[:-3]}_uniq.fasta', 'w')
    path_uniq.write('\n'.join(uniq_doc_list))
    path_uniq.close()
    os.system(f'rm {path}')
    os.system(f'rm ./{path[:-3]}_filtered.fas')
    # df = pd.DataFrame.from_dict(data)
    filtered_kmers.close()
    cluster.close()

    print('end')