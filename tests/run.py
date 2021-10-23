import unittest, os, pandas, pathlib, subprocess

fpath = pathlib.Path(__file__).parent.absolute()

output = os.path.join(fpath, 'output')

class TestRun(unittest.TestCase):
    def max_difference(self, A, B, ratio_thres):
        self.assertTrue(A.shape == B.shape)
        
        # weak similarity test because different machines really give different results.
        self.assertTrue((A-B).abs().median().max() < 1-ratio_thres)

    def test_run(self):
        data = os.path.join(fpath, 'Melanoma.GSE115978.post_Ipi.CD8.gz')
        result_expected = pandas.read_csv(output + '.run.gz', sep='\t', index_col=0)
        
        # run command line as usage 1
        cmd = ['Tres.py', '-i', data, '-o', output]
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()
        
        result = pandas.read_csv(output, sep='\t', index_col=0)
        os.remove(output)
        
        # a known issue: depending on the computer, passed gene will be slightly different
        common = result.index.intersection(result_expected.index)
        
        ratio_thres = 0.95
        self.assertTrue(common.shape[0]/result.shape[0] > ratio_thres)
        self.assertTrue(common.shape[0]/result_expected.shape[0] > ratio_thres)
        
        # make sure the two usages get the same result   
        self.max_difference(result.loc[common], result_expected.loc[common], ratio_thres)

if __name__ == '__main__': unittest.main()
