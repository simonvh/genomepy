import os.path
import re
import subprocess as sp

from genomepy.plugin import Plugin
from genomepy.utils import mkdir_p, cmd_ok, run_index_cmd


class GmapPlugin(Plugin):
    def after_genome_download(self, genome, force=False):
        if not cmd_ok("gmap_build"):
            return

        # Create index dir
        index_dir = genome.props["gmap"]["index_dir"]
        index_name = genome.props["gmap"]["index_name"]
        mkdir_p(index_dir)

        if (
            not os.path.exists(index_name)
            or any(fname.endswith(".iit") for fname in os.listdir(index_name))
            or force is True
        ):
            # If the genome is bgzipped it needs to be unzipped first
            fname = genome.filename
            bgzip = False
            if fname.endswith(".gz"):
                ret = sp.check_call(["gunzip", fname])
                if ret != 0:
                    raise Exception("Error gunzipping genome {}".format(fname))
                fname = re.sub(".gz$", "", fname)
                bgzip = True

            # remove old files in index dir if force-overwrite is requested
            gmap_files = os.listdir(index_name)
            if force and len(gmap_files) > 0:
                for f in gmap_files:
                    fpath = os.path.join(index_name, f)
                    if os.path.isfile(fpath):
                        os.unlink(fpath)

            # Create index
            cmd = "gmap_build -D {} -d {} {}".format(index_dir, genome.name, fname)
            run_index_cmd("gmap", cmd)

            if bgzip:
                ret = sp.check_call(["bgzip", fname])
                if ret != 0:
                    raise Exception(
                        "Error bgzipping genome {}. ".format(fname)
                        + "Is tabix installed?"
                    )

    def get_properties(self, genome):
        props = {
            "index_dir": os.path.join(
                os.path.dirname(genome.filename), "index", "gmap"
            ),
            "index_name": os.path.join(
                os.path.dirname(genome.filename), "index", "gmap", genome.name
            ),
        }
        return props
