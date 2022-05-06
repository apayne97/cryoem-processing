import argparse
import os.path
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("cs_star_file")
parser.add_argument("-r", "--relion_movie_path", help="If you only have one dataset, this should be the path to the relion movies.star file")
parser.add_argument("-m", "--movie_yaml_path", help="If you have multiple datasets, use a yaml file to distinguish the different movies.star files")
parser.add_argument("-n", "--only_get_dataset_names", dest='only_get_names', help="Use this flag if you just want to see what datasets are in the cs file",
                    action="store_true")
parser.add_argument("-w", "--write_micrographs", dest='write_mics', help="Use this flag if you want the script to write out a file containing the selected micrographs",
                    action="store_true")
parser.add_argument("--cs_header_cutoff", dest='cs_header_cutoff', help="Number of characters to use to distinguish between header and data in cs particle star files", default=33, type=int)
parser.add_argument("--relion_header_cutoff", dest='relion_header_cutoff', help="Number of characters to use to distinguish between header and data in relion movies.star files", default=22, type=int)
args = parser.parse_args()

cs_star_file = args.cs_star_file
assert os.path.exists(cs_star_file), f'Path to "cs_star_file" not found: "{cs_star_file}" '

## I'll start from the csparc star file here:
print(f'Loading {cs_star_file}...')
with open(cs_star_file, 'r') as f:
    data = f.readlines()
    header = [line.rstrip() for line in data[:args.cs_header_cutoff] if line.rstrip() != '']
    micrographs_only = [line.split(' ')[1] + '\n' for line in data[args.cs_header_cutoff:]]
    print("Removing these lines as header:")
    for line in header:
        print("\t", line)
    print(f'{len(micrographs_only)} particles found')
    set_of_micrographs = set(micrographs_only)
    print(f'{len(set_of_micrographs)} unique micrographs found')

if args.write_mics:
    print(f'Writing mrc_paths.txt...')
    with open('mrc_paths.txt', 'w') as f:
        f.writelines(set_of_micrographs)

## get only the name of the micrograph split by field
data = [line.rstrip().split('/')[-1].split('_') for line in set_of_micrographs]

print("Printing first line after being processed...")
print(data[0])
## get unique list of datasets, which we will need to treat separately
data_sets = set([info[0] for info in data])
print("Found these datasets:")
for data_set in data_sets:
    print(data_set)

if args.only_get_names:
    exit(0)

## Making sure we have a path to the relion movies.star file
if len(data_sets) > 1:
    assert args.movie_yaml_path, "Multiple datasets were found but you have no movies.yaml path provided. Please create one to proceed."
    with open(args.movie_yaml_path, 'r') as f:
        movie_dict = yaml.safe_load(f)

    assert data_sets == set(movie_dict.keys()), f'It does not look like the list of datasets in your movies file matches the datasets found:\ndatasets found: {data_sets}\ndatasets provided: {set(movie_dict.keys())}'

    for path in movie_dict.values():
        assert os.path.exists(path), f'Relion movies.star path not found: {path}'

elif len(data_sets) == 1:
    assert args.relion_movie_path, "Only one dataset was found, but you have not provided a path to the relion movies.star file"
    assert os.path.exists(args.relion_movie_path), f'Relion movies.star path not found: {args.relion_movie_path}'
    movie_dict = {list(data_sets)[0]: args.relion_movie_path} ## set object is not subscriptable

print("Successfully found paths to relion movies for these datasets:")
for dataset, movies_star in movie_dict.items():
    print(f'{dataset}:\t{movies_star}')


data_dict = {data_set: [] for data_set in data_sets}


for data_set, data_list in data_dict.items():
    ## if the file is from this data_set, join the first three fields to create the file name from the og tif
    data_subset = ['_'.join(info[:3]) for info in data if info[0] == data_set]

    ## add the necessary text to make a real file out of this
    data_subset_str = [f'{micrograph}.tif\n' for micrograph in data_subset]
    data_dict[data_set] = data_subset_str

    ## write out to a new file for each dataset
    if args.write_mics:
        with open(f'{data_set}_tif_paths.txt', 'w') as f:
            f.writelines(data_subset_str)

## for each dataset
removed_mgraphs = 0
for data_set, data_subset in data_dict.items():
    print(f'Selecting micrographs from {data_set}')

    ## original movies file
    movies_file = movie_dict[data_set]

    ## movies subset file to be created
    movies_subset_file = f'{data_set}_movies_subset.star'

    print(f'Loading data from "{movies_file}" to be filtered into "{movies_subset_file}"...')

    ## read in movies file
    with open(movies_file, 'r') as f:
        data = f.readlines()

    ## keep track of header data to copy and paste into new file
    header = data[:args.relion_header_cutoff]
    full_data = data[args.relion_header_cutoff:]

    print("Copying these lines as header:")
    for line in header:
        if line.rstrip() != '':
            print("\t", line.rstrip())

    ## this is horrible to read, but basically checks to make sure the the file is found in the data_subset
    ## , skipping the header
    ## we want to leave the line as is because there might be other info we don't want to mess up
    mgraph_data = [line for line in full_data if f'{line.rstrip().split("/")[-1].split(" ")[0]}\n' in data_subset]

    n_old = len(full_data)
    n_new = len(mgraph_data)
    n_removed = n_old - n_new

    print(f'{data_set}: {n_old} --> {n_new} micrographs, {n_removed} removed')

    removed_mgraphs += n_removed


    ## write out new movies subset file
    with open(movies_subset_file, 'w') as f:
        f.writelines(header)
        f.writelines(mgraph_data)

print(f'\nCongratulations! You have removed a total of {removed_mgraphs} micrographs from your dataset.')

print("\nIMPORTANT: Make sure to check that the numbers line up, and make sure that the headers are correctly parsed.\n"
      "You may have to adjust the header cutoffs.\n"
      "Run this function with only the flag '-h' to see how.\n")

