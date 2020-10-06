import sys
import argparse
from genomepy.functions import Genome, install_genome


def parse_genome(auto_install=False, genomes_dir=None):
    """argparse action for command-line genome option.

    Parameters
    ----------
        auto_install : bool, optional
            Install a genome if it's not found locally.

        genomes_dir : str, optional
            Directory to look for and/or insall genomes.
    """

    class GenomeAction(argparse.Action):
        def __call__(self, parser, args, name, option_string=None):
            try:
                genome = Genome(name, genomes_dir=genomes_dir)
            except FileNotFoundError:
                print(f"Genome {name} not found!")
                if auto_install:
                    print("Trying to install it automatically using genomepy...")
                    install_genome(name, annotation=True, genomes_dir=genomes_dir)
                    genome = Genome(name)
                else:
                    print("You can install it using `genomepy install`.")
                    sys.exit(1)
            setattr(args, self.dest, genome)

    return GenomeAction
