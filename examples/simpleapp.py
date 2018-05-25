
from tendermint import TendermintApp
from tendermint.utils import (
    home_dir,
    int_to_big_endian,
    big_endian_to_int,
    to_hex
)
from tendermint.keys import Key
from tendermint.accounts import Account

## NOTE: THIS IS BROKEN - needs updated

# Some constants for the app
DATA_KEY=b'current_count'
INITIAL_COUNT = int_to_big_endian(1)

# Setup the application. Pointing it to the same root dir used by Tendermint.
# In this example, we are using ~/.pytendermint, which means we set a different
# root_dir when running 'init':  'tendermint init --home ~/.pytendermint'
app = TendermintApp(home_dir('.pytendermint'))
app.debug = True

# Called only once on the first initialization of the application
# this is a good place to put stuff in state like default accounts, storage, etc...
@app.on_initialize()
def create_count(db):
    app.log.debug('create count')
    db.put_data(DATA_KEY, INITIAL_COUNT)

    # create default accounts
    sender_key = Key.generate(b'584f84070d4022eb08933d28a562de6a')
    sender_acct = Account.create_account(sender_key.publickey(),0,100)
    app.log.debug( to_hex(sender_acct.address()) )
    db.update_account(sender_acct)

# Add more or more of these.  This is your business logic to change state.
# In this example, Txs with a 'call' of 'counter' will increment the count
# in state.
@app.on_transaction('counter')
def increment_the_count(tx, db):
    stored_value = db.get_data(DATA_KEY)
    v = big_endian_to_int(stored_value)
    v += 1
    db.put_data(DATA_KEY,int_to_big_endian(v))
    return True

# Queries to state.  Add 1 or more of these.
# In this example, the a call to the path '/data' with a given key
# from the client will call this handler
@app.on_query('/data')
def handle_nonce(key, db):
    return db.get_data(key)

# Fire it up - it'll connect to Tendermint
app.run()
