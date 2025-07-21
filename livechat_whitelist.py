import logging
import time
import requests

logger = logging.getLogger(__name__)

LIVECHAT_API_TOKEN = "your_token_here"  # Replace with your LiveChat API token

def add_domains_to_livechat_api(domains: list[str], retries: int = 3):
    """
    Automatically adds a list of domains to the LiveChat whitelist using the API.

    Args:
        domains (list[str]): A list of domains to whitelist.
        retries (int): Number of retry attempts on failure.
    """
    if not domains:
        return

    base64_token = LIVECHAT_API_TOKEN
    headers = {
        "Authorization": f"Basic {base64_token}",
        "Content-Type": "application/json",
    }
    url = "https://api.livechatinc.com/v2/domain_whitelist"

    for domain in domains:
        payload = {"domain": domain}
        attempt = 0
        success = False
        while attempt < retries and not success:
            try:
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code in (200, 201):
                    logger.info(f"Domain '{domain}' successfully added to the LiveChat whitelist.")
                    success = True
                elif response.status_code == 409:
                    logger.warning(f"Domain '{domain}' is already whitelisted.")
                    success = True
                else:
                    logger.error(
                        f"Failed to add domain '{domain}': {response.status_code} - {response.text}"
                    )
                    attempt += 1
                    time.sleep(2 ** attempt)
            except Exception as e:
                logger.error(f"Exception occurred while adding domain '{domain}': {str(e)}")
                attempt += 1
                time.sleep(2 ** attempt)

        if not success:
            raise Exception(
                f"Failed to add domain '{domain}' to the LiveChat whitelist after {retries} attempts."
            )

def remove_domain_from_livechat_api(domain: str, retries: int = 3):
    """
    Automatically removes a domain from the LiveChat whitelist using the API.

    Args:
        domain (str): The domain to remove from the whitelist.
        retries (int): Number of retry attempts on failure.
    """
    base64_token = LIVECHAT_API_TOKEN
    headers = {
        "Authorization": f"Basic {base64_token}",
    }
    url = f"https://api.livechatinc.com/v2/domain_whitelist/{domain}"

    attempt = 0
    success = False
    while attempt < retries and not success:
        try:
            response = requests.delete(url, headers=headers)
            if response.status_code in (200, 204):
                logger.info(f"Domain '{domain}' successfully removed from the LiveChat whitelist.")
                success = True
            else:
                logger.error(
                    f"Failed to remove domain '{domain}': {response.status_code} - {response.text}"
                )
                attempt += 1
                time.sleep(2 ** attempt)
        except Exception as e:
            logger.error(f"Exception occurred while removing domain '{domain}': {str(e)}")
            attempt += 1
            time.sleep(2 ** attempt)

    if not success:
        logger.warning(f"Failed to remove domain '{domain}' after {retries} attempts.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test: list of domains to add
    test_domains = ["yourdomain.com"]
    add_domains_to_livechat_api(test_domains)

    # Test: domain to remove
    test_remove_domain = "yourdomain.com"
    remove_domain_from_livechat_api(test_remove_domain)
