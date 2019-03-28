import argparse


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_topic', required=True,
        help=('Output PubSub topic of the form '
              '"projects/<PROJECT>/topic/<TOPIC>".'))
    # group = parser.add_mutually_exclusive_group(required=True)
    # group.add_argument(
    #     '--input_topic',
    #     help=('Input PubSub topic of the form '
    #           '"projects/<PROJECT>/topics/<TOPIC>".'))
    # group.add_argument(
    #     '--input_subscription',
    #     help=('Input PubSub subscription of the form '
    #           '"projects/<PROJECT>/subscriptions/<SUBSCRIPTION>."'))
    known_args, pipeline_args = parser.parse_known_args()

    print(known_args)
    # print(pipeline_args)


if __name__ == '__main__':
    run()
