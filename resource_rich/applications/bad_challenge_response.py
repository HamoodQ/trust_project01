#!/usr/bin/env python3

import logging
import random
import asyncio

from challenge_response import ChallengeResponseClient as ChallengeResponseClientGood, NAME
import client_common
from bad import PeriodicBad

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(f"app-{NAME}-bad")
logger.setLevel(logging.DEBUG)

MISBEHAVE_CHOICES = ["bad-response", "no-response"]

class ChallengeResponseClientBad(ChallengeResponseClientGood):
    def __init__(self, approach, duration):
        super().__init__()

        self.approach = approach

        self.bad = PeriodicBad(duration, NAME)

    async def start(self):
        await super().start()
        self.bad.start()

    async def shutdown(self):
        self.bad.shutdown()
        await super().shutdown()

    async def _send_result(self, dest, message_response):
        if self.bad.is_bad:
            await self._write_task_stats()

            if self.approach == "random":
                selected_approach = random.choice(MISBEHAVE_CHOICES)
            else:
                selected_approach = self.approach

            logger.debug(f"Currently bad, so behaving incorrectly with {selected_approach}")

            # Instead of sending a result, we pick one of two options
            # 1. Send a bad response
            # 2. Don't send any response

            if selected_approach == "bad-response":
                # A bad message response
                message_response = (b'', 0)
                await self._write_task_result(dest, message_response)

            elif selected_approach == "no-response":
                # Nothing to do
                pass

            else:
                logger.error(f"Unknown misbehaviour {selected_approach}")

        else:
            logger.debug(f"Currently good, so behaving correctly")
            await super()._send_result(dest, message_response)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='challenge-reponse always bad')
    parser.add_argument('--approach', type=str, choices=MISBEHAVE_CHOICES + ["random"], required=True, help='How will this application misbehave')
    parser.add_argument('--duration', type=float, required=True, help='How long will this application misbehave for in seconds')
    args = parser.parse_args()

    client = ChallengeResponseClientBad(args.approach, args.duration)

    client_common.main(NAME, client)
