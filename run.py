import argparse
import glob

import subprocess
import os

from tqdm import tqdm


RPLAN_PATH = "rplan_dataset/floorplan_dataset"

def paths_to_ids(paths):
    return [int(path.split("/")[-1].split(".")[0]) for path in paths]



def main(limit: int | None, max_processes: int):

    os.makedirs("rplan_json", exist_ok=True)
    os.makedirs("failed_rplan_json", exist_ok=True)

    ids = paths_to_ids(glob.glob(f"{RPLAN_PATH}/*.png"))

    if limit is not None:
        ids = ids[:limit]

    done_ids = paths_to_ids(glob.glob("rplan_json/*.json"))
    failed_ids = paths_to_ids(glob.glob("failed_rplan_json/*"))

    todo_ids = list(set(ids) - set(done_ids) - set(failed_ids))

    print(f"{len(todo_ids)=}")


    # subprocess loop from: https://stackoverflow.com/a/4992640
    processes = set()

    for rplan_id in tqdm(todo_ids, smoothing=50/len(todo_ids)):
        command = f'python raster_to_json.py --path rplan_dataset/floorplan_dataset/{rplan_id}.png || (touch failed_rplan_json/{rplan_id} && false)'

        processes.add(subprocess.Popen(command, shell=True))
        if len(processes) >= max_processes:
            os.wait()
            processes.difference_update([
                p for p in processes if p.poll() is not None])


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()

    argparser.add_argument("--limit", type=int, default=None)
    argparser.add_argument("--max_processes", type=int, default=8)

    args = argparser.parse_args()
    
    main(limit=args.limit, max_processes=args.max_processes)
