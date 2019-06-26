import sys
import asyncio
import syndicate.mini.core as S

_ = S.Discard()

BME280 = S.Record.makeConstructor('BME280', 'host timestamp temperature pressure humidity')

argv = sys.argv
conn = S.Connection.from_url(argv[1] if len(argv) == 2 else 'unix:/var/run/syndicate.sock#test')

with conn.turn() as t:
    with conn.actor().react(t) as facet:
        facet.add(S.Observe(S.Capture(BME280(_, _, _, _, _))),
                  on_add=lambda t, b: print('+', b),
                  on_del=lambda t, b: print('-', b))

loop = asyncio.get_event_loop()
loop.run_until_complete(conn.reconnecting_main(loop))
