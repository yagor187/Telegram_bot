import get_data

def start_main():
    try:
        get_data.start()
    except ConnectionError:
        print("No connection")

if __name__ == "__main__":
    start_main()



