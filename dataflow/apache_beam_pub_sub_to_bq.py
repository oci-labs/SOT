from __future__ import absolute_import

import argparse
import logging

from past.builtins import unicode

import apache_beam as beam
import apache_beam.transforms.window as window
from apache_beam.examples.wordcount import WordExtractingDoFn
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions


def run(argv=None):
    """Build and run the pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_topic',
                        default='projects/securityofthings/topics/gateway-telemetry')
    parser.add_argument('--input_subscription',
                        default='new-subscription')
    parser.add_argument('--output_path',
                        default='gs://pub_sub_temp/temp/')
    known_args, pipeline_args = parser.parse_known_args(argv)

    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '--input_topic', required=True,
    #     help=('Output PubSub topic of the form '
    #           '"projects/<PROJECT>/topic/<TOPIC>".'))
    # group = parser.add_mutually_exclusive_group(required=True)
    # group.add_argument(
    #     '--input_topic',
    #     help=('Input PubSub topic of the form '
    #           '"projects/<PROJECT>/topics/<TOPIC>".'))
    # group.add_argument(
    #     '--input_subscription',
    #     help=('Input PubSub subscription of the form '
    #           '"projects/<PROJECT>/subscriptions/<SUBSCRIPTION>."'))
    # known_args, pipeline_args = parser.parse_args(argv)

    # We use the save_main_session option because one or more DoFn's in this
    # workflow rely on global context (e.g., a module imported at module level).
    options = PipelineOptions(flags=argv)
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = 'securityofthings'
    google_cloud_options.job_name = 'mk-dataflow-51'
    google_cloud_options.staging_location = 'gs://pub_sub_staging/'
    google_cloud_options.temp_location = 'gs://pub_sub_temp/temp'
    options.view_as(StandardOptions).runner = 'DataflowRunner'
    options.view_as(StandardOptions).streaming = True
    # options.view_as(SetupOptions).save_main_session = True
    p = beam.Pipeline(argv=pipeline_args, options=options)

    def print_row(row):
        # print row
        return row

    # Read from PubSub into a PCollection.
    # if known_args.input_subscription:
    #     messages = (p
    #                 | beam.io.ReadFromPubSub(subscription=known_args.input_subscription)
    #                 .with_output_types(bytes))
    output = (p | 'read' >> beam.io.ReadFromPubSub(topic=known_args.input_topic)) #.with_output_types(bytes))

    # outpu_2 = (output | 'decode' >> beam.Map(lambda x: x.decode('utf-8')))

    output | 'print' >> beam.Map(lambda x: x)
              # .with_output_types(bytes)
              # | 'window' >> beam.WindowInto(window.FixedWindows(15, 0))
              # | 'decode' >> beam.Map(lambda x: x.decode('utf-8'))

    # else:
    # with beam.Pipeline(argv=pipeline_args, options=options) as p:
    # | 'add_window' >> beam.WindowInto(window.FixedWindows(10, 5)))

    p.run().wait_until_finish()
    # result = p.run()
    # result.wait_until_finish()

    #    --experiments=allow_non_updatable_job \
    # print(r)
    # | "print" >> beam.Map(print_row))
    # .with_output_types(bytes))

    # bq_input = telemetry | 'decode' >> beam.Map(lambda x: x.decode('utf-8'))

    # telemetry | "print" >> beam.Map(print_row)

    # bq_input | 'WriteToText' >> beam.io.WriteToText(known_args.output_path,
    #                                                 file_name_suffix='sdasgdasg')

    # Count the occurrences of each word.
    # def count_ones(word_ones):
    #     (word, ones) = word_ones
    #     return (word, sum(ones))
    #
    # counts = (lines
    #           | 'split' >> (beam.ParDo(WordExtractingDoFn())
    #                         .with_output_types(unicode))
    #           | 'pair_with_one' >> beam.Map(lambda x: (x, 1))
    #           | beam.WindowInto(window.FixedWindows(15, 0))
    #           | 'group' >> beam.GroupByKey()
    #           | 'count' >> beam.Map(count_ones))

    # Format the counts into a PCollection of strings.
    # def format_result(word_count):
    #     (word, count) = word_count
    #     return '%s: %d' % (word, count)
    #
    # output = (counts
    #           | 'format' >> beam.Map(format_result)
    #           | 'encode' >> beam.Map(lambda x: x.encode('utf-8'))
    #           .with_output_types(bytes))
    #
    # # Write to PubSub.
    # # pylint: disable=expression-not-assigned
    # output | beam.io.WriteToPubSub(known_args.output_topic)
    #
    # result = p.run()
    # result.wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
