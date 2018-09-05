# This file is part of the Trezor project.
#
# Copyright (C) 2012-2018 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import binascii
import time

import pytest

from trezorlib import messages
from trezorlib.cardano import create_input, create_output

from .common import TrezorTest


@pytest.mark.cardano
@pytest.mark.skip_t1  # T1 support is not planned
class TestMsgCardanoSignTx(TrezorTest):
    def test_cardano_sign_tx(self):
        self.setup_mnemonic_nopin_nopassphrase()

        transaction = {
            "inputs": [
                {
                    "path": "m/44'/1815'/0'/0/0",
                    "prev_hash": "ca074369a7a0ce8011786185b85126ba1bd2cd5914e4a58a7f4da31b962956b8",
                    "prev_index": 0,
                    "type": 0,
                },
                {
                    "path": "m/44'/1815'/0'/0/0",
                    "prev_hash": "60d7f2cf6505f05737b25c2d22ecdc4fbbe077cfecf1e90e881e8bce94a2a604",
                    "prev_index": 0,
                    "type": 0,
                },
            ],
            "outputs": [
                {
                    "address": "DdzFFzCqrhsjQzXZ7gho1o6ZZhizeQxKJX2wvVVUgpa4hks7bEQAjt4JSzg2BAUoBjQ9tk7cB6k7wTWAL2V1BkMK7gLEML1JHhsRTSUe",
                    "amount": "1000000",
                },
                {"path": "m/44'/1815'/0'/0/6", "amount": "820712"},
            ],
            "transactions": [
                "839f8200d8185824825820e93771c56e9e177c28497ae17f1ecfc56a00a7ac0653da2fa7240307f193dd4601ff9f8282d818584283581c2b103ebc45c7db3fc3808f7dafa8f3c34f0b149f7950f6ab3d442166a101581e581c2822588050088dbfe66e90209534952b1e414e376fcf04fc0f03dd10001a0de078971a000f42408282d818584283581c92b6528e73ebcefebe25b13f5e33e053aff9d09811fd7e810bda9a1ea101581e581c2822588050088dbfe66e9620aaf9509a0c9c8d8ed77d582eb9ccec6d001a3d355a311a0196a322ffa0",
                "839f8200d8185824825820ef190cea890ae778e5887ae1e9168ee8de6c4d5503f27f43e01793e8677ed07501ff9f8282d818584283581c2b103ebc45c7db3fc3808f7dafa8f3c34f0b149f7950f6ab3d442166a101581e581c2822588050088dbfe66e90209534952b1e414e376fcf04fc0f03dd10001a0de078971a000f42408282d818584283581ccad2fdca5a7e591afe9775f9edad110628f8d7b63c2a89a8e622a943a101581e581c2822588050088dbfe66e92209ccbd3a56d5f6354e75ecb0cf3f08cda001ae9e6086c1a0386dd2affa0",
            ],
        }

        inputs = [create_input(input) for input in transaction["inputs"]]
        outputs = [create_output(output) for output in transaction["outputs"]]
        transactions = transaction["transactions"]

        self.client.transport.write(
            messages.CardanoSignTx(
                inputs=inputs, outputs=outputs, transactions_count=len(transactions)
            )
        )
        response = self.client.transport.read()

        assert isinstance(response, messages.CardanoTxRequest)
        assert response.tx_index == 0

        # Upload first transaction
        transaction_data = binascii.unhexlify(transactions[0])
        ack_message = messages.CardanoTxAck(transaction=transaction_data)
        self.client.transport.write(ack_message)

        response = self.client.transport.read()
        assert isinstance(response, messages.CardanoTxRequest)
        assert response.tx_index == 1

        # Upload second transaction
        transaction_data = binascii.unhexlify(transactions[1])
        ack_message = messages.CardanoTxAck(transaction=transaction_data)
        self.client.transport.write(ack_message)

        # Confirm fee
        response = self.client.transport.read()
        assert isinstance(response, messages.ButtonRequest)
        assert response.code == messages.ButtonRequestType.Other

        self.client.debug.press_yes()
        self.client.transport.write(messages.ButtonAck())
        time.sleep(1)

        # Confirm Output
        response = self.client.transport.read()
        assert isinstance(response, messages.ButtonRequest)
        assert response.code == messages.ButtonRequestType.Other

        self.client.debug.press_yes()
        self.client.transport.write(messages.ButtonAck())
        time.sleep(1)
        self.client.debug.swipe_down()
        time.sleep(1)

        # Confirm amount
        response = self.client.transport.read()
        assert isinstance(response, messages.ButtonRequest)
        assert response.code == messages.ButtonRequestType.Other

        self.client.debug.press_yes()
        self.client.transport.write(messages.ButtonAck())

        # Confirm change path
        response = self.client.transport.read()
        assert isinstance(response, messages.ButtonRequest)
        assert response.code == messages.ButtonRequestType.Other

        self.client.debug.press_yes()
        self.client.transport.write(messages.ButtonAck())
        time.sleep(1)
        self.client.debug.swipe_down()
        time.sleep(1)

        # Confirm change amount
        response = self.client.transport.read()
        assert isinstance(response, messages.ButtonRequest)
        assert response.code == messages.ButtonRequestType.Other

        self.client.debug.press_yes()
        self.client.transport.write(messages.ButtonAck())
        time.sleep(1)

        response = self.client.transport.read()
        assert isinstance(response, messages.CardanoSignedTx)

        assert (
            binascii.hexlify(response.tx_hash)
            == b"5a91b9b66bdd6a980a7a3a10101f9c6874f4fd51440b21aec9f51692c887ccf1"
        )
        assert (
            binascii.hexlify(response.tx_body)
            == b"82839f8200d8185824825820ca074369a7a0ce8011786185b85126ba1bd2cd5914e4a58a7f4da31b962956b8008200d818582482582060d7f2cf6505f05737b25c2d22ecdc4fbbe077cfecf1e90e881e8bce94a2a60400ff9f8282d818584283581c2b103ebc45c7db3fc3808f7dafa8f3c34f0b149f7950f6ab3d442166a101581e581c2822588050088dbfe66e90209534952b1e414e376fcf04fc0f03dd10001a0de078971a000f42408282d818583e83581cb91467966cdf7c832aeaf95da90d0d4ea115b9ad33f0b4927840c417a101581a581868c5491437fcb4db145afc6e39f71354ab14a622096c0a1e001aa55a3cc01a000c85e8ffa0828200d8185885825840901fe8901937674e1536e5b0068d032bd2dc88e442e608b0438784be3c36c67fc5bf86092fb4aff15cb40606808d74ad71b33b6399e2da2811f98c105f154ecf5840b3ffe68be32985a0caee8449e0787586b2d057a21d1a0795805586b402e4fb45ccc4e3d8ff6561592113447cd7092644d73886a62a18dc296614e2f30153810f8200d8185885825840901fe8901937674e1536e5b0068d032bd2dc88e442e608b0438784be3c36c67fc5bf86092fb4aff15cb40606808d74ad71b33b6399e2da2811f98c105f154ecf5840b3ffe68be32985a0caee8449e0787586b2d057a21d1a0795805586b402e4fb45ccc4e3d8ff6561592113447cd7092644d73886a62a18dc296614e2f30153810f"
        )
