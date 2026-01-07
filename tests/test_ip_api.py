import logging

from src.api.ip_api import IPStackAPI

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main():
    try:
        logger.info("Starting IP API test")

        ip_api = IPStackAPI()
        test_ips = ["72.229.28.185", "110.174.165.78", "invalid_ip_test"]

        results = ip_api.get_ip_info(test_ips)

        logger.info("Results:")
        for result in results:
            print(f"\nIP: {result.get('ip', 'N/A')}")
            print(f"Country: {result.get('country_name', 'N/A')}")
            print(f"City: {result.get('city', 'N/A')}")
            if "error" in result:
                print(f"Error: {result['error']}")

        logger.info("Test completed successfully")

    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()
