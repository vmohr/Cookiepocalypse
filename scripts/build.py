import sys
src=open(sys.argv[1]).read(); calc=open(sys.argv[2]).read()
open(sys.argv[3],'w').write(src.replace('/*CALC*/',calc))
