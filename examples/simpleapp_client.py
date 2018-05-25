
import json
import click
from tendermint import Transaction
from tendermint.client import RpcClient
from tendermint.utils import from_hex, to_hex, big_endian_to_int, str_to_bytes
from tendermint.keys import Key
from tendermint.accounts import Account

rpc = RpcClient()

@click.group()
def cli():
    pass

@cli.command()
def check_status():
    """Check Tendermint status"""
    print(rpc.status())

@cli.command()
@click.argument('value')
def send_count(value):

    # sender_key = Key.fromPrivateKey('0x5e9dc3f088827719eed25d7424059b9f584f84070d4022eb08933d28a562de6a')

    sender_key = Key.generate(b'584f84070d4022eb08933d28a562de6a')
    print( sender_key.publickey() )

    # sender_acct = Account.create_account(sender_key.publickey())
    # print( to_hex(sender_acct.address()) )

    # TODO: BROKEN! The Tx must be signed with the correct nonce
    t = Transaction()
    t.call = 'counter'
    t.value = int(value)
    t.sign(sender_key)
    raw = t.encode()

    result = rpc.send_tx_commit(raw)
    print(result)

@cli.command()
def view_count():
    result = rpc.query('/data','current_count')
    result = json.loads(result)
    v = result.get('response').get('value')
    print(v)
    print(big_endian_to_int(str_to_bytes(v)))

if __name__ == '__main__':
    cli()
