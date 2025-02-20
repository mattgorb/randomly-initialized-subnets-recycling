import argparse
import sys
import yaml

from configs import parser as _parser

args = None


def parse_arguments():
    parser = argparse.ArgumentParser(description="PyTorch ImageNet Training")

    # General Config
    parser.add_argument(
        "--data", help="path to dataset base directory", default="/s/luffy/b/nobackup/mgorb/data"
    )
    parser.add_argument("--optimizer", help="Which optimizer to use", default="sgd")
    parser.add_argument("--set", help="name of dataset", type=str, default="ImageNet")
    parser.add_argument(
        "-a", "--arch", metavar="ARCH", default="ResNet18", help="model architecture"
    )
    parser.add_argument(
        "--config", help="Config file to use (see configs dir)", default=None
    )
    parser.add_argument(
        "--log-dir", help="Where to save the runs. If None use ./runs", default=None
    )
    parser.add_argument(
        "-j",
        "--workers",
        default=20,
        type=int,
        metavar="N",
        help="number of data loading workers (default: 20)",
    )
    parser.add_argument(
        "--epochs",
        default=90,
        type=int,
        metavar="N",
        help="number of epochs to run with learning rate adjustment. ",
    )
    parser.add_argument(
        "--total_epochs",
        default=None,
        type=int,
        metavar="N",
        help="number of total epochs to run",
    )


    parser.add_argument(
        "--start-epoch",
        default=None,
        type=int,
        metavar="N",
        help="manual epoch number (useful on restarts)",
    )
    parser.add_argument(
        "-b",
        "--batch-size",
        default=256,
        type=int,
        metavar="N",
        help="mini-batch size (default: 256), this is the total "
        "batch size of all GPUs on the current node when "
        "using Data Parallel or Distributed Data Parallel",
    )
    parser.add_argument(
        "--lr",
        "--learning-rate",
        default=0.1,
        type=float,
        metavar="LR",
        help="initial learning rate",
        dest="lr",
    )
    parser.add_argument(
        "--warmup_length", default=0, type=int, help="Number of warmup iterations"
    )
    parser.add_argument(
        "--momentum", default=0.9, type=float, metavar="M", help="momentum"
    )
    parser.add_argument(
        "--wd",
        "--weight-decay",
        default=1e-4,
        type=float,
        metavar="W",
        help="weight decay (default: 1e-4)",
        dest="weight_decay",
    )
    parser.add_argument(
        "-p",
        "--print-freq",
        default=50,
        type=int,
        metavar="N",
        help="print frequency (default: 10)",
    )
    parser.add_argument("--num-classes", default=10, type=int)
    parser.add_argument(
        "--resume",
        default="",
        type=str,
        metavar="PATH",
        help="path to latest checkpoint (default: none)",
    )
    parser.add_argument(
        "-e",
        "--evaluate",
        dest="evaluate",
        action="store_true",
        help="evaluate model on validation set",
    )
    parser.add_argument(
        "--pretrained",
        dest="pretrained",
        default=None,
        type=str,
        help="use pre-trained model",
    )
    parser.add_argument(
        "--pretrained2",
        dest="pretrained2",
        default=None,
        type=str,
        help="use pre-trained model",
    )
    parser.add_argument("--local_rank", type=int, default=0)
    parser.add_argument("--rank", type=int, default=0)
    parser.add_argument("--world_size", type=int, default=1)
    parser.add_argument("--ngpus_per_node", type=int, default=0)

    # This needs to be explicitly passed in
    parser.add_argument("--local_world_size", type=int, default=1)


    parser.add_argument(
        "--gpu", default=1, type=int, help="gpu id"
    )

    # Learning Rate Policy Specific
    parser.add_argument(
        "--lr-policy", default="constant_lr", help="Policy for the learning rate."
    )
    parser.add_argument(
        "--multistep-lr-adjust", default=30, type=int, help="Interval to drop lr"
    )
    parser.add_argument(
        "--multistep-lr-gamma", default=0.1, type=int, help="Multistep multiplier"
    )
    parser.add_argument(
        "--name", default=None, type=str, help="Experiment name to append to filepath"
    )
    parser.add_argument(
        "--save_every", default=-1, type=int, help="Save every ___ epochs"
    )
    parser.add_argument(
        "--prune_rate",
        default=0.0,
        help="Amount of pruning to do during sparse training",
        type=float,
    )
    parser.add_argument(
        "--low-data", default=1, help="Amount of data to use", type=float
    )
    parser.add_argument(
        "--width_mult",
        default=1.0,
        help="How much to vary the width of the network.",
        type=float,
    )
    parser.add_argument(
        "--nesterov",
        default=False,
        action="store_true",
        help="Whether or not to use nesterov for SGD",
    )
    parser.add_argument(
        "--random-subnet",
        action="store_true",
        help="Whether or not to use a random subnet when fine tuning for lottery experiments",
    )
    parser.add_argument(
        "--one-batch",
        action="store_true",
        help="One batch train set for debugging purposes (test overfitting)",
    )
    parser.add_argument(
        "--layer_type", type=str, default=None, 
    )
    parser.add_argument(
        "--freeze-weights",
        action="store_true",
        help="Whether or not to train only subnet (this freezes weights)",
    )
    parser.add_argument("--mode", default="fan_in", help="Weight initialization mode")

    parser.add_argument(
        "--nonlinearity", default="relu", help="Nonlinearity used by initialization"
    )
    parser.add_argument("--bn-type", default=None, help="BatchNorm type")


    parser.add_argument(
        "--no-bn-decay", action="store_true", default=False, help="No batchnorm decay"
    )
    parser.add_argument(
        "--scale-fan", action="store_true", default=False, help="scale fan"
    )
    parser.add_argument(
        "--first-layer-dense", action="store_true", help="First layer dense or sparse"
    )
    parser.add_argument(
        "--last-layer-dense", action="store_true", help="Last layer dense or sparse"
    )
    parser.add_argument(
        "--label-smoothing",
        type=float,
        help="Label smoothing to use, default 0.0",
        default=None,
    )
    parser.add_argument(
        "--first-layer-type", type=str, default=None, help="Conv type of first layer"
    )
    parser.add_argument(
        "--trainer", type=str, default="default", help="cs, ss, or standard training"
    )

    parser.add_argument(
        "--threshold", default=None, help="Weight initialization modifications"
    )

    parser.add_argument(
        "--weight_init", default=None, help="Weight initialization modifications"
    )
    parser.add_argument(
        "--score_init", default=None, help="Weight initialization modifications"
    )

    parser.add_argument(
        "--rerand_iter_freq", default=None, help="Weight randomization frequency"
    )
    parser.add_argument(
        "--rerand_epoch_freq", default=None, help="Weight randomization frequency"
    )
    parser.add_argument(
        "--rerand_type", default=None, help="rerand type, iterand or recycle"
    )
    parser.add_argument(
        "--rerand_warmup", default=1, help="rerand warmup, iterand or recycle"
    )
    parser.add_argument(
        "--rerand_rate", default=None, help="rerand rate, iterand"
    )

    parser.add_argument(
        "--weight_seed", default=0, help="Weight initialization modifications"
    )
    parser.add_argument(
        "--score_seed", default=0, help="Weight initialization modifications"
    )
    parser.add_argument(
        "--seed", default=0, type=int, help="seed for initializing training. "
    )
    parser.add_argument(
        "--ablation", default='none', type=str, help=" "
    )
    parser.add_argument(
        "--alpha_param", default='weight', type=str, help=" "
    )
    parser.add_argument(
        "--multigpu", default=None, type=str,
        #type=lambda x: [int(a) for a in x.split(",")], 
    )

    parser.add_argument('--global_compression_factor', type=int, default=None, help='factor of 2')
    parser.add_argument('--compression_factor', type=int, default=None, help='factor of 2')

    parser.add_argument('--weight_tile_size', type=int, default=None,)
    parser.add_argument('--data_type', type=str, default=None,)
    parser.add_argument('--layer_compression_factors', type=str, default=None, help='factor of 2')

    parser.add_argument('--model_type', type=str, default='binarize', help='prune or binarize')
    parser.add_argument('--alpha_type', type=str, default=None, help='single or multiple alphas per layer')
    parser.add_argument('--min_compress_size', default=64000)

    #performance arguments
    parser.add_argument('--kernel', type=str, default=None)
    parser.add_argument('--log_perf', type=bool, default=None)
    parser.add_argument('--perf_speed', type=bool, default=None)

    args = parser.parse_args()

    # Allow for use from notebook without config file
    if len(sys.argv) > 1:
        get_config(args)

    return args


def get_config(args):
    # get commands from command line
    override_args = _parser.argv_to_vars(sys.argv)

    # load yaml file
    yaml_txt = open(args.config).read()

    # override args
    loaded_yaml = yaml.load(yaml_txt, Loader=yaml.FullLoader)
    for v in override_args:
        loaded_yaml[v] = getattr(args, v)

    print(f"=> Reading YAML config from {args.config}")
    args.__dict__.update(loaded_yaml)


def run_args():
    global args
    if args is None:
        args = parse_arguments()


run_args()
