#!/usr/bin/env python

f = open('sample.xcm','w')
cmd  = 'data 1 sample/xis_1mCrabFeLine_80ks_bin.pha\n'
#cmd += 'none\n'
#cmd += 'none\n'
cmd += 'backgrnd sample/xis_1mCrabFeLine_80ks_bkg.fak\n'
cmd += 'resp 1 sample/ae_2FI_xisnom_ao10.rsp\n'
cmd += 'ignore **-0.5 10.0-**\n'
cmd += '@sample/fake_model_1mCrabFeLine.xcm\n'
cmd += 'freeze 7 \n'
cmd += 'fit\n'
f.write(cmd)
f.close()

cmd  = 'xspec<<EOF\n'
cmd += '@sample/sample.xcm\n'
cmd += 'fmakexspecfitlog.py sample/param.yaml sample/get_error.xcm\n'
cmd += '@sample/get_error.xcm\n'
cmd += './freadxspecfitlog.py sample/param.yaml fit.log\n'
print cmd