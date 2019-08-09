#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse       import OptionParser
from dynamicloader  import DynamicLoader
import os

def main():
    parser = OptionParser()
    parser.add_option('-n','--network',
                      action='store',
                      dest='net',
                      default='',
                      help='Give a valid network filename')
    parser.add_option('-d', '--data',
                      action='store',
                      dest='data',
                      default='',
                      help='Give a valid data fileneme')
    parser.add_option('-s', '--settings',
                      action='store',
                      dest='settings',
                      default='',
                      help='Give a valid settings fileneme')
    (options, args) = parser.parse_args()

    if  os.path.exists(options.net)     and \
        os.path.exists(options.data)    and \
        os.path.exists(options.settings):

        loader = DynamicLoader()
        plugin = loader.getPluginByName('MLP')

        trainer = None
        if plugin is not None:
            trainer = plugin.mlGetTrainer(options.net, options.data)

        if trainer is not None:
            trainer.mlConfigureTrainer(options.settings)

            while True:
                trainer.mlTrainerRun()
                if trainer.mlIsTrainerRunning():
                    progress = trainer.mlGetTrainerProgress()
                    error    = trainer.mlGetTrainerError()
                    print >>sys.stdout, 'Progress:%(prog)f, Error:%(err)f' % {'prog':progress, 'err':error}


if __name__ == '__main__':
    main()
