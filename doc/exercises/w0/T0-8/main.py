import httpx

def main():
    print("Hello from t0-8!")
    response = httpx.get("https://httpbin.org/get")
    print(response.json())

if __name__ == "__main__":
    main()
