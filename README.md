T-cell resilience model  

Prerequisite:  
1, ridge_significance: https://github.com/data2intelligence/ridge_significance    
Please read its README.md and run test to make sure the successful installation.    
  
2, CytoSig: https://github.com/data2intelligence/CytoSig  
Please read its README.md and run test to make sure the successful installation.  
  
3, pandas >= 1.1.4: You may install anaconda (https://www.anaconda.com) to include all required python packages.      
  
Usage:  
  
In the same folder of README.md    
python Tres.py -i single-cell data -o output -c <count threshold, default: 50>  
  
1, input: single-cell transcriptomic data matrix. The format could be a text file, gzip file, or pickle file. Please see "Melanoma.GSE115978.post_Ipi.CD8.pickle.gz" as an example.  
  
Column: Cell ID in the format of Cell_Type.Patient_ID.Cell_Barcode (or any sample ID).  
Row: Human gene symbols.  
Value: Gene expression value. We suggest log2(TPM/10 + 1) normalized by subtracting the mean from all conditions.      
  
2, output: results from the interaction test.  
  
Column: Condition ID in the format of Value_Type.Cell_Type.Patient_ID.Signal_ID  
  -Value_Type: t: t-value from the student t-test on the interaction term in regression, p: p-value of the associated t-value  
  -Cell_Type: the same as input  
  -Patient_ID: the same as input  
  -Signal_ID: TGFB1 or TRAIL, representing two immunosuppressive signals in the tumor microenvironment  
  
Row: Gene ID  
  
3, count threshold: the minimum number of cells in a sample to be analyzed. For example, with the default value 50, Tres will ignore all combinations of cell type and patient with less than 50 single cells sequenced.  
  
Example:  
In the directory of README.md, please type: python Tres.py -i Melanoma.GSE115978.post_Ipi.CD8.pickle.gz -o output  
  