Tumor-resilient T-cell model  

**Prerequisite**:  
1, ridge\_significance: https://github.com/data2intelligence/ridge_significance    
Please read its README.md and run test to make sure the successful installation.    
  
2, CytoSig: https://github.com/data2intelligence/CytoSig  
Please read its README.md and run test to make sure the successful installation.  
  
3, pandas >= 1.1.4: You may install anaconda (https://www.anaconda.com) to include all required python packages.  


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
