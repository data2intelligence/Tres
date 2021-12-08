#Tumor-resilient T-cell model  

**Prerequisite**:  
1, [ridge_significance](https://github.com/data2intelligence/ridge_significance)    
Please read its README.md and run test to make sure the successful installation.    
  
2, [CytoSig](https://github.com/data2intelligence/CytoSig)  
Please read its README.md and run test to make sure the successful installation.  
  
3, pandas >= 1.1.4: You may install [anaconda](https://www.anaconda.com) to include all required python packages.  


**Install**:
python setup.py install  


**Test**:  
1, Run the Tres model to compute signatures of tumor-resilient T cells  
python -m unittest tests.run  

2, Run the T-cell efficacy prediction using a pre-computed Tres signature  
python -m unittest tests.predict  


**Usage 1: compute Tres gene scores**:      
Tres.py -i <single-cell data> -o output -c <count threshold, default: 100> -n <mean-normalization, default: 0>
  
1, input: single-cell transcriptomic data matrix. The format could be a text file, gzip file, or pickle file. Please see "Melanoma.GSE115978.post\_Ipi.CD8.gz" as an example.  
  
Column: Cell ID in the format of Cell\_Type.Patient\_ID.Cell\_Barcode (or any sample ID).  
Row: Human gene symbols.  
Value: Gene expression value. We suggest log2(TPM/10 + 1) normalized by subtracting the mean from all conditions.      
  
Note: For 10x genomics data, we also included a command line tool **convert_mtx.py** to convert cell ranger output format to Tres input format. Please read the usage section at the end.  

2, output: results from the interaction test.  
  
Column: Condition ID in the format of Value\_Type.Cell\_Type.Patient\_ID.Signal\_ID  
  -Value\_Type: t: t-value from the student t-test on the interaction term in regression, p: p-value of the associated t-value  
  -Cell\_Type: the same as input  
  -Patient\_ID: the same as input  
  -Signal\_ID: TGFB1, TRAIL, PGE2, representing immunosuppressive signals in the tumor microenvironment  
  
Row: Gene ID  
  
3, count threshold: the minimum number of cells in a sample to be analyzed. For example, with the default value 100, Tres will ignore all combinations of cell type and patient with less than 100 single cells sequenced.  

4, mean-normalization: whether normalize input gene expression values by subtracting the mean value across all conditions. We assume the users should do similar normalization before using Tres, thus the default value is 0. Otherwise, please activate this option.   
  
Example:  
In the directory of README.md, please type: Tres.py -i tests/Melanoma.GSE115978.post\_Ipi.CD8.gz -o output  


**Usage 2: compute sample-wise correlations with pre-computed Tres signature**:      
Tres.py -m predict -i <sample data> -o output -c <count threshold, default: 100> -n <mean-normalization, default: 0>  
  
1, input: sample transcriptomic data matrix. The format could be a text file, gzip file, or pickle file. Please see "Sample\_Melanoma\_GSE120575\_Tex.gz" as an example.  
  
Column: Sample ID.  
Row: Human gene symbols.  
Value: Gene expression value. We suggest log2(TPM + 1) normalized by subtracting the mean from all conditions.      
  
2, output: correlation and p-values for each sample.  
  
Column:   
  r: Pearson correlation  
  p: p-value from two-sided student t-test    
  
Row: Sample ID  
  
3, count threshold: the minimum number of genes in overlap between input gene expression matrix and the pre-computed Tres signature.  

4, mean-normalization: whether normalize input gene expression values by subtracting the mean value across all conditions. We assume the users should do similar normalization before using Tres, thus the default value is 0. Otherwise, please activate this option.  
  
Example:  
In the directory of README.md, please type: Tres.py -m predict -i tests/Sample\_Melanoma\_GSE120575\_Tex.gz -o output  

---  
  
#Convert cellranger output to Tres input format:  
The input to Tres is a dense matrix file. However, the 10x cellranger output is a feature-barcode matrix in sparse format. Thus, we provide a command line tool for format conversation.  
The converter will merge all files with prefix provided after removing cell barcodes and genes with low read counts, transforming read count to log2(TPM/10+1), and subtracting the average value for each gene across all cell barcodes.  

**Prerequisite**:    
scipy >= 1.7.1, pandas >= 1.1.4: You may install [anaconda](https://www.anaconda.com) to include all required python packages.  

**Install**:  
This command line tool will be installed together with Tres.  
  
**Test**:  
First, download some sample cellranger output files:  
wget [https://hpc.nih.gov/~Jiang_Lab/Tres/GSE139829_sample.tar.gz](https://hpc.nih.gov/~Jiang_Lab/Tres/GSE139829_sample.tar.gz)  
tar xvf GSE139829_sample.tar.gz  
  
Second, cd into the extracted folder and type:  
convert\_mtx.py -i GSM4147093\_UMM059\_,GSM4147096\_UMM063\_,GSM4147099\_UMM066\_ -o GSE139829_density -s Cytotoxic\ CD8

Then, you can see a converted file "GSE139829_density.pickle.gz", on which you can apply Tres by:  
Tres.py -i GSE139829\_density.pickle.gz -o GSE139829\_sample\_Tres  

**Usage**:  
convert_mtx.py -i <input list, separated by ,> -o <output prefix> -c <barcode count threshold, default: 1000> -f <gene non-zero fraction threshold, default: 0.95> -s <cell subsets, default: leave empty>  

1, input list:  
Please input a list of file prefix of cell ranger output separated by ",". For example, f1,f2, .... For each prefix, we assume barcode, gene, and sparse matrix files as: fprefix + 'barcodes.tsv.gz', fprefix + 'genes.tsv.gz', fprefix + 'matrix.mtx.gz'.  
To generate Tres input file, we also need a cell annotation file named as fprefix + 'cell_map.gz'.  
The first column should contain cell barcodes in the barcode file.  
The second column should has a name "Sample", representing the patient sample ID.  
The third column should has a name "Cell Type", representing the cell type annotation.  
  
2, output: Converted file in python pickle format.  

3, barcode count threshold:  
The minimum number of read count for a cell barcode. If a cell barcode contains very few read counts below the threshold, the converter will drop the cell barcode.  

4, gene non-zero fraction:  
The maximum fraction of zero read count (dropout) for a gene. If a gene gets zero read count (dropout) in most cell barcodes, the converter will drop the gene.  

5, cell subset:  
The T-cell labels to be analyzed in Tres. If nothing is provided, Tres will analyze all cell types.   
