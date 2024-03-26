import sys
import argparse
# from chip_

def main():
    parser = argparse.ArgumentParser(description='Potentiostat Py')

    # Test program
    parser.add_argument('action', choices=["test"])

    args = parser.parse_args(sys.argv[1:])
    print(args.action)

    if args.action == "test":
        print("In cli interface: making potentiostat!+==============================================")
        potstat = Potentiostat()

        potstat.disconnect_all_electrodes()
        potstat.zero_all_voltages()
        pass
    else:
        raise NotImplementedError()

if __name__ == "__main__":
    main()

    
