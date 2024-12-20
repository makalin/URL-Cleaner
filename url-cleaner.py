#!/usr/bin/env python3

import re
import sys
import argparse
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from typing import Set, List, Optional
import pyperclip  # For clipboard operations
import logging
from pathlib import Path

class URLCleaner:
    # Common tracking parameters to remove
    TRACKING_PARAMS: Set[str] = {
        # Google Analytics & Ads
        'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
        'gclid', 'gclsrc',
        # Facebook
        'fbclid',
        # Microsoft/Bing
        'msclkid',
        # Other common tracking parameters
        '_hsenc', '_hsmi', 'mc_cid', 'mc_eid', 'zanpid',
        # Amazon
        'ref', 'tag',
        # General
        'source', 'affiliate', 'campaign', 'track'
    }

    # Patterns that suggest tracking parameters
    TRACKING_PATTERNS = [
        r'^_.*id$',           # Parameters ending with 'id' with leading underscore
        r'^ref_?.*$',         # Parameters starting with 'ref'
        r'^track(ing)?_?.*$', # Parameters starting with 'track' or 'tracking'
        r'^affiliate_?.*$',   # Parameters starting with 'affiliate'
        r'^camp(aign)?_?.*$'  # Parameters starting with 'camp' or 'campaign'
    ]

    @classmethod
    def looks_like_tracking_param(cls, param: str) -> bool:
        """Check if a parameter name matches common tracking parameter patterns."""
        return any(re.match(pattern, param, re.IGNORECASE) for pattern in cls.TRACKING_PATTERNS)

    @classmethod
    def clean(cls, url: str) -> str:
        """
        Clean a URL by removing tracking parameters.
        
        Args:
            url (str): The URL to clean
            
        Returns:
            str: The cleaned URL
        """
        try:
            # Parse the URL
            parsed = urlparse(url)
            
            # Parse query parameters
            params = parse_qs(parsed.query, keep_blank_values=True)
            
            # Filter out tracking parameters
            filtered_params = {
                k: v for k, v in params.items()
                if k.lower() not in cls.TRACKING_PARAMS
                and not cls.looks_like_tracking_param(k)
            }
            
            # Reconstruct the URL
            clean_query = urlencode(filtered_params, doseq=True)
            cleaned_url = urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                clean_query,
                parsed.fragment
            ))
            
            return cleaned_url
            
        except Exception as e:
            logging.error(f"Error cleaning URL {url}: {str(e)}")
            return url

    @classmethod
    def clean_batch(cls, urls: List[str]) -> List[str]:
        """Clean multiple URLs at once."""
        return [cls.clean(url) for url in urls]

def setup_logging(debug: bool = False):
    """Configure logging settings."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def process_file(file_path: Path) -> List[str]:
    """Process a file containing URLs (one per line)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {str(e)}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Clean tracking parameters from URLs')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url', help='URL to clean')
    group.add_argument('-f', '--file', type=Path, help='File containing URLs (one per line)')
    group.add_argument('-c', '--clipboard', action='store_true', help='Clean URL from clipboard')
    
    parser.add_argument('-o', '--output', type=Path, help='Output file for results')
    parser.add_argument('--copy', action='store_true', help='Copy result to clipboard')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    setup_logging(args.debug)

    # Process input
    if args.url:
        urls = [args.url]
    elif args.file:
        urls = process_file(args.file)
    else:  # clipboard
        try:
            urls = [pyperclip.paste()]
        except Exception as e:
            logging.error(f"Error reading from clipboard: {str(e)}")
            return 1

    # Clean URLs
    cleaned_urls = URLCleaner.clean_batch(urls)
    
    # Handle output
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                for url in cleaned_urls:
                    f.write(f"{url}\n")
        except Exception as e:
            logging.error(f"Error writing to output file: {str(e)}")
            return 1
    else:
        for original, cleaned in zip(urls, cleaned_urls):
            if original != cleaned:
                print(f"Original: {original}")
                print(f"Cleaned:  {cleaned}\n")
            else:
                print(f"No tracking parameters found: {original}\n")

    # Copy to clipboard if requested
    if args.copy and cleaned_urls:
        try:
            pyperclip.copy(cleaned_urls[0] if len(cleaned_urls) == 1 else '\n'.join(cleaned_urls))
            print("Result copied to clipboard!")
        except Exception as e:
            logging.error(f"Error copying to clipboard: {str(e)}")
            return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
