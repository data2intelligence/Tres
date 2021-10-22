import unittest, os, pandas, pathlib, subprocess

fpath = pathlib.Path(__file__).parent.absolute()

output = os.path.join(fpath, 'output')

class TestPredict(unittest.TestCase):
    def max_difference(self, A, B):
        self.assertTrue(A.shape == B.shape)
        self.assertTrue((A-B).abs().max().max() < 1e-8)

    def test_predict(self):
        data = os.path.join(fpath, 'Sample_Melanoma_GSE120575_Tex.gz')
        result_expected = pandas.read_csv(output + '.predict.gz', sep='\t', index_col=0)
        
        # run command line as usage 1
        cmd = ['Tres.py', '-m', 'predict', '-i', data, '-o', output]
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()
        
        result = pandas.read_csv(output, sep='\t', index_col=0)
        os.remove(output)
        
        # make sure the two usages get the same result   
        self.max_difference(result, result_expected)

if __name__ == '__main__': unittest.main()
