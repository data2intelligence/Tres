#!/usr/bin/env python
import os
import sys
import numpy
import pandas
import getopt

from scipy import io


def load_mtx(barcodes, genes, matrix, cell_map, min_count):
    title = os.path.basename(matrix)
    
    # quality check of input data first
    cell_map = pandas.read_csv(cell_map, sep='\t', index_col=0)
    
    for v in ['Cell Type', 'Sample']:
        if v not in cell_map.columns:
            sys.stderr.write('Error: %s cannot find %s in cell_map.\n' % (title, v))
            sys.exit(1)
    
    matrix = io.mmread(matrix)
    matrix = pandas.DataFrame.sparse.from_spmatrix(matrix)
    
    # assume first column of barcodes
    barcodes = pandas.read_csv(barcodes, sep='\t', header=None).iloc[:,0]
    
    # assume last column of genes is symbols
    genes = pandas.read_csv(genes, sep='\t', header=None).iloc[:, -1]
    
    assert matrix.shape[0] == genes.shape[0]
    assert matrix.shape[1] == barcodes.shape[0]
    
    matrix.index = genes
    matrix.columns = barcodes
    assert matrix.columns.value_counts().max() == 1
    
    # only focus on annotated cell barcodes
    common = matrix.columns.intersection(cell_map.index)
    if common.shape[0] == 0:
        sys.stderr.write('Error: %s no barcode annotated.\n' % title)
        sys.exit(1)
    
    matrix = matrix.loc[:, common]
    
    # jump bad cells, if any
    barcode_cnt = matrix.sum()
    if barcode_cnt.min() < min_count:
        matrix = matrix.loc[:, matrix.sum() >= min_count]

    # jump ambiguous genes, if any
    cnt_map = matrix.index.value_counts()
    if cnt_map.max() > 1:
        matrix = matrix.loc[cnt_map.loc[matrix.index] == 1]
    
    assert matrix.index.value_counts().max() == 1
    
    # remove empty genes
    matrix = matrix.loc[(matrix == 0).mean(axis=1) < 1]
    
    # make the column to CytoSig format
    matrix.columns = cell_map.loc[matrix.columns, 'Cell Type'] + '.' + cell_map.loc[matrix.columns, 'Sample'] + '.' + matrix.columns
    return matrix



def main():
    min_count = 1000
    min_ratio = 0.95
    
    input_lst = included = output = None
    
    prompt_msg = 'Usage:\nconvert_mtx.py -i <input list, separated by ,> -o <output prefix> -c <barcode count threshold, default: %d> -f <gene non-zero fraction threshold, default: %f> -s <cell subsets, default: leave empty>\n' % (min_count, min_ratio)
    
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hi:o:c:f:s:", [])
    
    except getopt.GetoptError:
        sys.stderr.write('Error input\n' + prompt_msg)
        sys.exit(2)
    
    if len(opts) == 0:
        sys.stderr.write('Please input some parameters or try: convert_mtx.py -h\n')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print(prompt_msg)
            sys.exit()
        
        elif opt in ("-i"):
            input_lst = arg.split(',')
        
        elif opt in ("-s"):
            included = arg.split(',')
        
        elif opt in ("-o"):
            output = arg
        
        elif opt in ("-c"):
            try:
                min_count = int(arg)
            except:
                sys.stderr.write('count threshold %s is not a valid integer number.\n' % arg)
                sys.exit(1)
            
            if min_count < 100:
                sys.stderr.write('count threshold %d < 100. Please input a number >= 100\n' % min_count)
                sys.exit(2)
        
        elif opt in ("-f"):
            try:
                min_ratio = float(arg)
            except:
                sys.stderr.write('gene non-zero frequency threshold %s is not a valid float number.\n' % arg)
                sys.exit(1)
            
            if min_ratio > 1 or min_ratio <= 0:
                sys.stderr.write('count threshold %d < 100. Please input a number in (0, 1]\n' % min_count)
                sys.exit(2)
    
    
    if input_lst is None:
        sys.stderr.write('Please provide a input file list\n')
        sys.exit(2)
    
    if output is None:
        sys.stderr.write('Please provide an output prefix\n')
        sys.exit(2)        
    
    
    # only look at commonly profiled frequent genes across all subsets
    merge = []
    
    for fprefix in input_lst:
        barcodes = fprefix + 'barcodes.tsv.gz'
        genes = fprefix + 'genes.tsv.gz'
        matrix = fprefix + 'matrix.mtx.gz'
        cell_map = fprefix + 'cell_map.gz'
        
        for f in [barcodes, genes, matrix, cell_map]:
            if not os.path.exists(f):
                sys.stderr.write('Error: cannot find %s\n' % f)
                break
        
        matrix = load_mtx(barcodes, genes, matrix, cell_map, min_count)
        
        print(os.path.basename(fprefix), matrix.shape)
        
        merge.append(matrix)

    data = pandas.concat(merge, axis=1, join='inner')
    data = data.loc[(data == 0).mean(axis=1) < min_ratio]
    data = data.loc[:, data.sum() >= min_count]
    
    size_factor = 1E5/data.sum()
    data *= size_factor
    data = numpy.log2(data + 1)
    
    # always centralize on all cells, instead of included cells
    background = data.mean(axis=1)
    data = data.subtract(background, axis=0)

    if included is not None:
        data = data.loc[:, [v.split('.')[0] in included for v in data.columns]]
        
        if data.shape[0] == 0:
            sys.stderr.write('No cells included in %s.\n' % ','.join(included))
            sys.exit(2)
    
    print('data shape', data.shape)
    
    data.sparse.to_dense().to_pickle(output + '.pickle.gz', compression='gzip')
    
    return 0


if __name__ == '__main__':
    main()
