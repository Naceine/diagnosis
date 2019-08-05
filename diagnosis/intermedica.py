"""Testing the Intermedica Python API.

   @author
     Victor I. Afolabi
     Artificial Intelligence Expert & Researcher.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: intermedica.py
     Created on 08 June, 2019 @ 12:51 PM.

   @license
     Apache 2.0 License
     Copyright (c) 2019. Victor I. Afolabi. All rights reserved.
"""
import sys
sys.path.append('..')

import argparse
import infermedica_api

from config.util import Log

args = None


def conditions(api: infermedica_api.API):
    Log.info('Conditions list:')
    Log.pretty(api.conditions_list())

    Log.info('Conditions details:')
    Log.pretty(api.condition_details('c_221'))

    Log.warn('Conditions details (Fail Test)')
    Log.pretty(api.condition_details('fail'))


def diagnosis(api: infermedica_api.API):
    request = infermedica_api.Diagnosis(sex='female', age=35)
    request.add_symptom('s_21', 'present', initial=True)
    request.add_symptom('s_98', 'present', initial=True)
    request.add_symptom('s_107', 'absent')

    # call diagnosis
    request = api.diagnosis(request)

    Log.pretty(request)

    # ask patient the questions returned by diagnosis and update request with patient answers
    request.add_symptom('s_99', 'present')
    request.add_symptom('s_8', 'absent')
    request.add_symptom('s_25', 'present')
    # ... and so on until you decided that enough question have been asked
    # or you have sufficient results in request.conditions

    # call diagnosis again with updated request
    request = api.diagnosis(request)

    # repeat the process
    Log.pretty(request)


def explain(api: infermedica_api.API):
    # Prepare diagnosis request it need to have sufficient amount of evidences
    # The most appropriate way to get a request way for explain method is to
    # use the one which has been created while interacting with diagnosis.
    # For the example purpose a new one is created.
    request = infermedica_api.Diagnosis(sex='female', age=35)

    request.add_symptom('s_10', 'present')
    request.add_symptom('s_608', 'present')
    request.add_symptom('s_1394', 'absent')
    request.add_symptom('s_216', 'present')
    request.add_symptom('s_9', 'present')
    request.add_symptom('s_188', 'present')

    # call the explain method
    request = api.explain(request, target_id='c_62')

    # and see the results

    Log.pretty(request)


def lab_tests(api: infermedica_api.API):
    pass


def parse(api: infermedica_api.API):
    pass


def risk_factors(api: infermedica_api.API):
    pass


def search(api: infermedica_api.API):
    pass


def suggest(api: infermedica_api.API):
    pass


def symptoms(api: infermedica_api.API):
    pass


def triage(api: infermedica_api.API):
    pass


def main():
    infermedica_api.configure({
        'app_id': args.id,
        'app_key': args.key,
        'dev_mode': args.mode,
    })

    api = infermedica_api.get_api()
    # resp = api.parse('I feel stomach pain but no coughing today.')
    # Log.debug(resp)


if __name__ == '__main__':
    FLAGS = argparse.ArgumentParser(
        epilog='Infermedica diagnosis API.\n',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Test infermedica API'
    )
    FLAGS.add_argument('-id', '--id', type=str, default='',
                       help='Your infermedica APP ID.')
    FLAGS.add_argument('-k', '--key', type=str, default='',
                       help='Your infermedica API Key.')
    FLAGS.add_argument('-m', '--mode', type=bool, default=True,
                       help='Make requests in development mode (Only during development).')

    args = FLAGS.parse_args()

    # Display command-line arguments & their values.
    Log.info('\n{0}\n{1:^55}\n{0}'
             .format('-' * 55, 'Command Line Arguments'))
    for k, v in vars(args).items():
        Log.info('{:<20} = {!s:>20}'.format(k, v))
    Log.info('\n{}\n'.format('-' * 55))

    main()
