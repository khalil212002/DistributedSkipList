import env
from distributed_skip_list import DistributedSkipList


def main():
    env.load()
    print("starting " + env.NAME)
    dsl = DistributedSkipList(env.MAX_LIST_HEIGHT, env.PORT)
    dsl.serveAndConnect(env.PEERS)
    dsl.server.wait()


if __name__ == "__main__":
    main()
