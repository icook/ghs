import pymetrics
from PyMetrics.compute import ComputeMetrics
from PyMetrics.lexer import Lexer
from PyMetrics.PyMetrics import __instantiateMetric, __importMetricModules
import glob
import os
import fnmatch
import sys
import pymongo

client = pymongo.MongoClient('localhost')
db = client.metric_db
db.authenticate('guest', 'guest')

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

runMetrics = {} # metrics for whole run
metrics = {}    # metrics for this module
context = {}    # context in which token was used

# import all the needed metric modules
pa = Bunch(includeMetrics=[('simple', 'SimpleMetric'),
                            ('mccabe', 'McCabeMetric'),
                            ('sloc', 'SLOCMetric')],
           quietSw=False,
           verbose=0)
metricModules = __importMetricModules(pa.includeMetrics)

db.packages.insert({"name": "yota"})
for root, dirnames, filenames in os.walk("/home/isaac/programming/yota/"):
    for filename in fnmatch.filter(filenames, '*.py'):
        f = os.path.join(root, filename)

        metrics.clear()
        context.clear()
        context['inFile'] = f

        metricInstance = {}
        inclIndx = -1
        for m,n in pa.includeMetrics:
            inclIndx += 1
            try:
                metricInstance[m] = None        # default value if metric class does not exist.
                metricInstance[m] = metricModules[m].__dict__[n]( context, runMetrics, metrics, {} )
            except KeyError:
                pass

        cm = ComputeMetrics( metricInstance, context, runMetrics, metrics, pa, None, None )

        # define lexographical scanner to use for this run
        # later, this may vary with file and language.
        lex = Lexer()

        if not pa.quietSw:
            print "=== File: %s ===" % f

        try:
            lex.parse(f)  # parse input file

            metrics["numCharacters"] = len(lex.srcLines)
            metrics["numLines"] = lex.lineCount                  # lines of code

            metrics = cm( lex )
        except IOError, e:
            sys.stderr.writelines( str(e) + " -- Skipping input file.\n\n")
        else:
            db.packages.update({"name": "yota"},
                               {"push":
                                    {"filename": f,
                                     "characters": metrics['numCharacters'],
                                     "comments": metrics['numComments'],
                                     "func_count": metrics['numFunction']}
                                })
            import pprint
            pprint.pprint( metrics )
