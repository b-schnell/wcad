
#!/usr/bin/env python2
#
# Copyright 2015 by Ss Cyril and Methodius University in Skopje, Macedonia
# Copyright 2015 by Idiap Research Institute in Martigny, Switzerland
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Branislav Gerazov, October 2015
#   Aleksandar Gjoreski, October 2015
#

from wcad import *
from optparse import OptionParser
import time
import shutil
import numpy as np

def compute(opts, args):
    print opts
    print args
    params = Params()
    paths = Paths(args, params)

    start_t = time.time()
    wave = WaveInput(paths.wav, params).read()
    pitch = PitchExtractor(wave, params, paths).compute()

    phrase = MultiphraseExtractor(pitch, wave, params, paths).compute()

    dictionary = DictionaryGenerator(params, paths).compute()
    atoms = AtomExtrator(wave, pitch, phrase, dictionary,
                         params, paths).compute()

    model = ModelCreator(phrase, atoms, pitch).compute()
    print 'Model created in %s seconds' % (time.time() - start_t)

    ModelSaver(model, params, paths).save()

    recon = model.reconstruction

    # recon_avg_err = np.sum(np.abs(phrase.curve - pitch.f0_log))/len(phrase.curve)
    # print len(model.atoms)
    # print recon_avg_err
    # if len(model.atoms) < 70 and recon_avg_err > 1:
    # ModelPlotterc(wave, model, pitch, params, paths).plot()

    # Convert log F0 to F0.
    # recon = np.exp(recon)
    # Print F0, so it can be retrieved by an sh script.
    # np.set_printoptions(threshold=np.inf)  # Prevent dots (...) in output.
    # print recon
    # print phrase.curve

    # clean up
    if params.overwrite_results_dir == 'none':
        shutil.rmtree(paths.res_dir)

    return model.atoms, phrase

def main():
    (opts, args) = OptionParser().parse_args()
    # args = ['audio/A01.wav', 'results']  # testing example
    # args = ['audio/A01E.wav', 'results']  # testing example
    # args = ['audio/A02.wav', 'results']  # testing example
    # args = ['audio/A02E.wav', 'results']  # testing example
    # args = ['audio/A03.wav', 'results']  # testing example
    # args = ['audio/A03E.wav', 'results']  # testing example
    # args = ['audio/A04.wav', 'results']  # testing example
    # args = ['audio/A04E.wav', 'results']  # testing example
    # args = ['audio/A05.wav', 'results']  # testing example
    # args = ['audio/A05E.wav', 'results']  # testing example
    atoms = compute(opts, args)
    if atoms is not None:
        # Return everything is alright.
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    print "wcad main"
    main()
