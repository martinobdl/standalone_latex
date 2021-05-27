import argparse
import subprocess
import os


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


parser = argparse.ArgumentParser()

parser.add_argument('-i', metavar='in-file', type=argparse.FileType('rt'), required=True)
parser.add_argument('-c', metavar='config-file', type=argparse.FileType('rt'))
parser.add_argument('-o', metavar='out-dir', type=dir_path, required=True)


args = parser.parse_args()

with open("standalone.tex", "rt") as f:
    first_part = f.readlines()[:-2]

file = "".join(first_part) + "\\input{" + args.i.name + "}\n" + "\\end{document}"

with open("/tmp/tmp.tex", "w") as f:
    f.writelines(file)

basename = os.path.splitext(os.path.basename(args.i.name))[0]
outfile = os.path.join(args.o, basename+'.pdf')

if __name__ == "__main__":
    subprocess.run(['pdflatex', '--enable-write18', '--extra-mem-top=100000000',
                    '--synctex=1', '-output-directory=/tmp', '-jobname=foo',
                    '/tmp/tmp.tex', ],
                   check=True, text=True)

    subprocess.run(['mv', '/tmp/foo.pdf', outfile],
                   check=True, text=True)

    print("Saved in {}".format(outfile))
