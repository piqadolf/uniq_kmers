def dtcsv():
    import os
    import pandas as pd
    from collections import defaultdict

    # creating a dictionary with k-mer counts for every cluster
    work = os.getcwd()
    if not os.path.exists('./real_dumps/'):
        os.mkdir('./real_dumps/')
    files = os.listdir(f'{work}/real_dumps')
    os.chdir(f'{work}/real_dumps')
    cluster_dict = dict()
    n = 0
    for i in files:
        n+=1
        if n%5000==0:
            print(n)
        count_dict = defaultdict(list)
        f = open(i,'r')
        counts = []
        for line in f.readlines():
            if '>' in line:
                counts.append(int(line.strip()[1:]))
                current = int(line.strip()[1:])
            else:
                count_dict[current].append(line.strip())
        counts.sort()
        #  only top-5 counts
        counts = counts[-5:]
        # all counts
        # counts = counts
        list_keys = list(count_dict.keys())
        for key in list_keys:
            if int(key) not in counts:
                del count_dict[key]
        cluster_dict[i[:-3]] = count_dict

        if n%5000==0:
            print(f'name of cluster - {i}')
    print(len(cluster_dict))

    # creating additional dictionary with cluster size value for each cluster
    os.chdir(f'{work}')
    seqs = open('all_clades.fasta')
    cluster_size = dict()
    for i in seqs.readlines():
        if '>' in i:
            header = (i.strip().split('|')[-2])
            cluster_size[header] = (i.strip().split('|')[-1]) ### размеры клад добавить

    # transforming jellyfish output for all clusters to a dictionary with k-mer counts for all clusters at once
    os.chdir(f'{work}')
    cl = open('k_dump_uniq.fasta','r')
    all_kmers = dict()
    n = 0
    for i in cl.readlines():
        n+=1
        if n%1000000==0:
            print(n)
        if '>' in i:
            current = int(i.strip()[1:])
        else:
            all_kmers[i.strip()] = current
    print('all kmers', len(all_kmers))

    # counting statistics and generating output 
    cluster_pd = []
    kmer_pd = []
    error_rate_pd = []
    sensitivity_pd = []
    sizes = []
    TP = []
    FP = []
    quality = []
    print(cluster_size.keys())
    print(len(cluster_size))
    
    for clustername, cluster in cluster_dict.items():
        for count, kmers in cluster.items():
            for kmer in kmers:
                error_rate = (int(all_kmers[kmer])-int(count))/int(all_kmers[kmer])
                sensitivity = int(count)/int(cluster_size[clustername])
                cluster_pd.append(clustername)
                kmer_pd.append(kmer)
                error_rate_pd.append(error_rate)
                sensitivity_pd.append(sensitivity)
                sizes.append(int(cluster_size[clustername]))
                TP.append(int(count))
                FP.append((int(all_kmers[kmer])-int(count)))
                quality.append(sensitivity*(1-error_rate))
    unique_kmers = pd.DataFrame({'cluster':cluster_pd, 'kmer':kmer_pd, 'sensitivity':sensitivity_pd,\
                                 'error_rate':error_rate_pd, 'quality':quality, 'cluster_size':sizes, 'TP':TP, 'FP':FP})
    unique_kmers.to_csv('unique_kmers.csv', sep = ',', index = False)
