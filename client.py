import requests
import logging

def main():
    logging.basicConfig(filename='client_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Localhost ile çalışan sunucu URL'si
    destination_url = "http://127.0.0.1:5000/customers"

    # Sunucudan müşterileri çeker
    try:
        response = requests.get(destination_url)
        response.raise_for_status()  # Hata durumunda exception fırlatacak
        customers = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve customers: {str(e)}")
        logging.error(f"Failed to retrieve customers: {str(e)}")
        return    

    success_count = 0
    failure_count = 0
    failure_details = []

    # Gönderilecek veriler
    for customer in customers:  # Burada 'customers.values()' yerine sadece 'customers' kullanıyoruz.
        key = customer["key"]
        payload = {
            "key": customer["key"],
            "name": customer["name"], 
            "variables": {
                "customerCity": customer["customerCity"],
                "email": customer["email"]
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            put_response = requests.put(f"{destination_url}/{key}", headers=headers, json=payload)
            if put_response.ok:
                success_count += 1
                logging.info(f"Transaction stored successfully for customer {key}. Response: {put_response.json()}")
            else:
                failure_count += 1
                logging.error(f"Failed to store transaction for customer {key}. Status Code: {put_response.status_code}. Response: {put_response.text}")
                failure_details.append({
                    "customer_key": key,
                    "status_code": put_response.status_code,
                    "response": put_response.text
                })
        except requests.exceptions.RequestException as e:
            failure_count += 1
            failure_details.append({
                "customer_key": key,
                "error": str(e)
            })
            logging.error(f"An error occurred: {str(e)}")

        # Yanıtı yazdırın
        print(put_response.text)

    # Sonuç özetini logla
    logging.info(f"{success_count} data successfully transferred, {failure_count} data failed to transfer.")
    if failure_details:
        logging.info("Failed data details:")
        for detail in failure_details:
            logging.info(detail)

if __name__ == "__main__":
    main()
