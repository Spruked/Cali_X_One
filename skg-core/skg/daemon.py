import argparse, os, sys, time, threading
from .core import SKGService          # we expose this class below

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="cali_skg.db", help="sqlite file")
    parser.add_argument("--port", type=int, default=7777, help="grpc port")
    args = parser.parse_args()

    service = SKGService(db_path=args.db, port=args.port)
    print(f"[SKG] starting on port {args.port}, db={args.db}")
    service.start()        # blocks, handles KeyboardInterrupt

if __name__ == "__main__":
    main()